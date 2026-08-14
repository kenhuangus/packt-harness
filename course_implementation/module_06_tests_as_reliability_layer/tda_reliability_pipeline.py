"""
Module 6: Test-Driven Agent (TDA) & Anti-Regression Pipeline
Runs real pytest subprocesses and feeds their captured output into the repair loop.
"""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


sys.stdout.reconfigure(encoding="utf-8")

MODULE_DIR = Path(__file__).resolve().parent
BASE_TEST = """\
from calculator import divide


def test_divide_by_zero():
    assert divide(10, 0) == 0
"""


def check_pytest_availability():
    """
    Prove pytest is importable for *this* interpreter before claiming a run.

    The course uses the same sys.executable for the availability check
    and the later test suite so a different Python on PATH cannot fake
    a pass. Missing pytest prints [SKIPPED] and exits 0.
    """
    command = [sys.executable, "-m", "pytest", "--version"]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    version_output = (result.stdout or result.stderr).strip()
    if result.returncode != 0:
        print(
            f"[SKIPPED] pytest is not available for {sys.executable}. "
            f"Install it with: {sys.executable} -m pip install pytest"
        )
        if version_output:
            print(version_output)
        return False

    print(f"[PASS] pytest availability check: {version_output}")
    return True


class TDAReliabilityPipeline:
    """
    Three-stage Test-Driven Agent loop against a real pytest subprocess.

    Stage 1 writes a divide() that raises ZeroDivisionError and captures
    the traceback. Stage 2 writes the known-good repair and reruns.
    Stage 3 appends a permanent regression test and reruns again.

    All files live in a TemporaryDirectory under this module and are
    deleted before the process exits. Nothing is left in the git tree.
    """

    def __init__(self):
        self.regression_suite = []
        # Scratch dir is next to this file so a leftover is visible if
        # cleanup fails; the finally block removes it on success.
        self._scratch = tempfile.TemporaryDirectory(
            prefix="tda_reliability_", dir=MODULE_DIR
        )
        self.scratch_dir = Path(self._scratch.name)
        self.code_file = self.scratch_dir / "calculator.py"
        self.test_file = self.scratch_dir / "test_calculator.py"
        self.test_file.write_text(BASE_TEST, encoding="utf-8")

    @staticmethod
    def _combined_output(result):
        output = result.stdout
        if result.stderr:
            if output and not output.endswith("\n"):
                output += "\n"
            output += result.stderr
        return output

    @staticmethod
    def _summary_line(output):
        for line in reversed(output.splitlines()):
            stripped = line.strip()
            if re.search(
                r"\b(passed|failed|error|errors|skipped|xfailed|xpassed)\b",
                stripped,
                re.IGNORECASE,
            ):
                return stripped
        return None

    def _run_pytest(self):
        """Run pytest as a subprocess in the scratch dir and return the CompletedProcess."""
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                self.test_file.name,
                "-q",
                "--tb=short",
                "-p",
                "no:cacheprovider",
            ],
            cwd=self.scratch_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
        )

    def run_test_suite(self, code_under_test):
        """Write calculator.py, run pytest, and return pass/fail plus captured output."""
        print("\n[TDA Pipeline] Running real pytest suite against proposed code...")
        self.code_file.write_text(code_under_test, encoding="utf-8")

        result = self._run_pytest()
        captured_output = self._combined_output(result)
        summary = self._summary_line(captured_output)

        if result.returncode != 0:
            print(
                f"[FAIL] pytest exited with return code {result.returncode}; "
                "captured failure output follows:"
            )
            print(captured_output.rstrip())
            return {
                "passed": False,
                "traceback": captured_output,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "summary": summary,
            }

        if summary is None:
            print(
                "[FAIL] pytest returned code 0, but no pytest summary line was "
                "captured."
            )
            return {
                "passed": False,
                "traceback": captured_output,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "summary": None,
            }

        print(f"[PASS] pytest summary: {summary}")
        return {
            "passed": True,
            "traceback": None,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "summary": summary,
        }

    def format_fix_prompt(self, traceback_str):
        """Turn captured pytest stdout/stderr into the repair prompt an agent would see."""
        print("\n[TDA Pipeline] Formatting real pytest failure into repair prompt:")
        prompt = (
            "System Instruction: Fix the following pytest failure output:\n"
            f"```\n{traceback_str}\n```"
        )
        print("--- REPAIR PROMPT GENERATED ---")
        print(prompt)
        return prompt

    def register_anti_regression_test(self, bug_name, test_code):
        """Append a new test to the live file, rerun pytest, and keep it only if it passes."""
        print(
            "\n[Anti-Regression Pipeline] Writing regression safeguard "
            f"'{bug_name}' to the real pytest file..."
        )
        with self.test_file.open("a", encoding="utf-8") as test_handle:
            test_handle.write(f"\n\n{test_code.rstrip()}\n")

        result = self._run_pytest()
        captured_output = self._combined_output(result)
        summary = self._summary_line(captured_output)

        if result.returncode != 0 or summary is None:
            print(
                f"[FAIL] Regression safeguard pytest run exited with return "
                f"code {result.returncode}."
            )
            print(captured_output.rstrip())
            return {
                "passed": False,
                "traceback": captured_output,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "summary": summary,
            }

        self.regression_suite.append({"name": bug_name, "code": test_code})
        print(f"[PASS] Regression safeguard enforced. pytest summary: {summary}")
        print(
            f"[Anti-Regression Pipeline] Total enforced safeguards: "
            f"{len(self.regression_suite)}"
        )
        return {
            "passed": True,
            "traceback": None,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "summary": summary,
        }

    def cleanup(self):
        scratch_path = self.scratch_dir
        self._scratch.cleanup()
        return not scratch_path.exists()


def main():
    print("=" * 60)
    print("MODULE 6 DEMO: TEST-DRIVEN AGENT (TDA) & ANTI-REGRESSION PIPELINE")
    print("=" * 60)

    if not check_pytest_availability():
        print("\n" + "=" * 60)
        print("MODULE 6 DEMO SKIPPED: pytest is required for real verification.")
        print("=" * 60)
        return 0

    tda = TDAReliabilityPipeline()
    demo_passed = False
    try:
        print("\n[TDA Stage 1] Prove the proposed implementation fails a real test.")
        failing_code = "def divide(a, b):\n    return a / b\n"
        result = tda.run_test_suite(failing_code)

        if result["passed"]:
            print("[FAIL] Stage 1 unexpectedly passed; repair loop was not proven.")
        else:
            tda.format_fix_prompt(result["traceback"])

            print(
                "\n[TDA Stage 2] Apply the known-good offline repair and rerun "
                "pytest."
            )
            fixed_code = (
                "def divide(a, b):\n"
                "    if b == 0:\n"
                "        return 0\n"
                "    return a / b\n"
            )
            fixed_result = tda.run_test_suite(fixed_code)

            if fixed_result["passed"]:
                print(
                    "\n[TDA Stage 3] Persist the bug as a regression test and "
                    "rerun pytest."
                )
                regression_result = tda.register_anti_regression_test(
                    "test_divide_zero_guard",
                    (
                        "def test_divide_zero_guard():\n"
                        "    assert divide(10, 0) == 0"
                    ),
                )
                demo_passed = regression_result["passed"]
    finally:
        cleaned = tda.cleanup()

    if cleaned:
        print("[PASS] Temporary pytest scratch directory cleaned up.")
    else:
        print("[FAIL] Temporary pytest scratch directory was not cleaned up.")

    print("\n" + "=" * 60)
    if demo_passed and cleaned:
        print("MODULE 6 DEMO COMPLETE: REAL TDA FEEDBACK LOOP VERIFIED!")
        exit_code = 0
    else:
        print("MODULE 6 DEMO FAILED: REAL TDA FEEDBACK LOOP NOT VERIFIED.")
        exit_code = 1
    print("=" * 60)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
