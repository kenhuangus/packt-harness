"""
Module 6 Integration: Test-Driven Agent (TDA) Reliability Pipeline for Deep Research Agent.
Executes Red-Repair-Green automated test loops, captures subprocess tracebacks,
and persists anti-regression validation safeguards.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


class TdaReliabilityPipeline:
    """Manages the Red-Repair-Green test-driven verification loop."""

    def __init__(self, workspace_path: Path):
        self.workspace = workspace_path
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.tests_dir = self.workspace / "tests"
        self.tests_dir.mkdir(parents=True, exist_ok=True)

    def write_citation_test_suite(self, citations_path: Path) -> Path:
        """Writes pytest suite to verify citation structural integrity and claim scores."""
        test_file = self.tests_dir / "test_citations_integrity.py"
        test_code = f"""import json
import pytest
from pathlib import Path

def test_citation_integrity():
    cit_path = Path(r"{citations_path.resolve()}")
    assert cit_path.exists(), "Citations JSON file must exist on disk."
    data = json.loads(cit_path.read_text(encoding="utf-8"))
    assert len(data) >= 2, "Report must contain at least 2 verified citations."
    for item in data:
        assert "doc_id" in item, "Each citation item must contain 'doc_id'."
        assert "title" in item, "Each citation item must contain 'title'."
        assert item.get("confidence_score", 0) >= 0.30, "Citation confidence score must be >= 0.30."
"""
        test_file.write_text(test_code, encoding="utf-8")
        return test_file

    def run_pytest(self, test_file: Path) -> tuple[bool, str, int]:
        """Runs pytest on the test file, returning (passed, output_traceback, exit_code)."""
        cmd = [sys.executable, "-m", "pytest", str(test_file), "-q"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace)
        passed = (res.returncode == 0)
        output = res.stdout + "\n" + res.stderr
        return passed, output.strip(), res.returncode

    def append_anti_regression_guard(self, test_file: Path, guard_name: str, assertion_code: str) -> None:
        """Persists a new regression test guard to prevent repeating failures."""
        guard_fn = f"\n\ndef {guard_name}():\n    {assertion_code}\n"
        with open(test_file, "a", encoding="utf-8") as f:
            f.write(guard_fn)
