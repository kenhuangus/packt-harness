"""
Module 8: Compound engineering with a real git worktree and a real JWT.

Planner emits a file-scoped plan. Implementer writes HS256 auth code into
an isolated git worktree. Reviewer runs pytest and AST checks inside that
worktree. Telemetry is appended to this module's telemetry.jsonl.
"""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone


sys.stdout.reconfigure(encoding="utf-8")

MODULE_DIR = Path(__file__).resolve().parent
REPO_ROOT = MODULE_DIR.parents[1]
OUTPUT_DIR = MODULE_DIR / "output"
sys.path.append(str(MODULE_DIR.parent))
from common.jwt_tools import auth_validator_source, test_auth_source  # noqa: E402


class SubagentPromptIsolator:
    """Keep only spec lines that name the subtask, scope, or non-goals."""

    def extract_sub_spec(self, master_spec: str, subtask_name: str) -> str:
        lines = master_spec.splitlines()
        filtered = [
            line
            for line in lines
            if subtask_name.lower() in line.lower()
            or "allowed scope" in line.lower()
            or "non-goals" in line.lower()
        ]
        if not filtered:
            return f"SUB-SPEC FOR {subtask_name}: Execute task within strict scope limits."
        return "\n".join(filtered)


class WorktreeIsolation:
    """Create and destroy a real `git worktree` under a temp directory."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.path: Path | None = None
        self.branch: str | None = None

    def add(self) -> Path:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        self.branch = f"module08-agent-{os.getpid()}-{stamp}"
        self.path = Path(os.environ.get("TEMP", str(MODULE_DIR))) / self.branch
        if self.path.exists():
            shutil.rmtree(self.path)
        result = subprocess.run(
            [
                "git",
                "worktree",
                "add",
                "-b",
                self.branch,
                str(self.path),
                "HEAD",
            ],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            raise RuntimeError(
                "git worktree add failed: "
                + (result.stderr or result.stdout).strip()
            )
        return self.path

    def remove(self) -> None:
        if self.path is None or self.branch is None:
            return
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(self.path)],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "branch", "-D", self.branch],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
        )
        if self.path.exists():
            shutil.rmtree(self.path, ignore_errors=True)


class MultiAgentTeam:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.isolator = SubagentPromptIsolator()
        self.telemetry_log = MODULE_DIR / "telemetry.jsonl"

    def run_planner(self, spec_text: str) -> dict:
        """Derive subtasks from the spec text rather than a fixed slogan."""
        targets = []
        for line in spec_text.splitlines():
            if ":" in line and not line.lower().startswith("spec"):
                name, action = line.split(":", 1)
                name = name.strip()
                action = action.strip()
                if name in {"Allowed Scope", "Non-goals"}:
                    continue
                if name == "auth_component":
                    targets.append(
                        {
                            "name": name,
                            "target_file": "auth.py",
                            "action": action,
                        }
                    )
                elif name == "test_suite":
                    targets.append(
                        {
                            "name": name,
                            "target_file": "test_auth.py",
                            "action": action,
                        }
                    )
        if not targets:
            raise ValueError("Planner found no auth_component/test_suite lines.")
        return {"subtasks": targets}

    def run_implementer(self, subtask: dict, master_spec: str) -> Path:
        focused = self.isolator.extract_sub_spec(master_spec, subtask["name"])
        target = self.workspace_root / subtask["target_file"]
        if subtask["target_file"] == "auth.py":
            body = (
                f"# Implementer subtask: {subtask['name']}\n"
                f"# Focused spec:\n# {focused.replace(chr(10), chr(10) + '# ')}\n"
                + auth_validator_source()
            )
        elif subtask["target_file"] == "test_auth.py":
            body = test_auth_source().replace(
                "from auth_validator import", "from auth import"
            )
        else:
            raise ValueError(f"Implementer refuses unknown target {subtask['target_file']}")
        target.write_text(body, encoding="utf-8")
        return target

    def run_reviewer(self, target_file: str) -> dict:
        target = self.workspace_root / target_file
        source = target.read_text(encoding="utf-8")
        ast.parse(source, filename=str(target))
        has_jwt = "def validate_jwt" in source
        return {"syntax_ok": True, "defines_validate_jwt": has_jwt, "path": str(target)}


def run_pytest(workspace: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "test_auth.py",
            "-q",
            "--tb=short",
            "-p",
            "no:cacheprovider",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def main() -> int:
    print("=" * 72)
    print("MODULE 8 DEMO: COMPOUND ENGINEERING & MULTI-AGENT TEAMS")
    print("=" * 72)

    OUTPUT_DIR.mkdir(exist_ok=True)
    allowed_scope = {"auth.py", "test_auth.py"}
    master_spec = (
        "SPEC: JWT Auth System\n"
        "Allowed Scope: auth.py, test_auth.py\n"
        "auth_component: Implement JWT validation\n"
        "test_suite: Write unit tests for JWT\n"
        "Non-goals: network calls and dependency changes"
    )

    isolation = WorktreeIsolation(REPO_ROOT)
    try:
        worktree = isolation.add()
        print(f"[Isolation] git worktree created at {worktree}")
        print(f"[Isolation] branch {isolation.branch}")

        team = MultiAgentTeam(worktree)
        (worktree / "SPEC.md").write_text(master_spec, encoding="utf-8")

        print("[Planner Subagent (Architect)] Analyzing requirement...")
        plan = team.run_planner(master_spec)
        subtasks = plan["subtasks"]
        print(f"  [PASS] Plan Generated: {len(subtasks)} micro-subtasks allocated.")

        print("[Implementer Subagent (Coder)] Writing into the worktree...")
        written = []
        for subtask in subtasks:
            path = team.run_implementer(subtask, master_spec)
            written.append(path)
            print(f"  [PASS] Wrote {path} ({path.stat().st_size} bytes).")

        print("[Reviewer Subagent (Auditor)] AST + pytest in the worktree...")
        reviews = []
        for subtask in subtasks:
            review = team.run_reviewer(subtask["target_file"])
            reviews.append(review)
            print(f"  [PASS] Review {subtask['target_file']}: {review}")

        pytest_result = run_pytest(worktree)
        pytest_output = (pytest_result.stdout + pytest_result.stderr).strip()
        print(pytest_output)
        pytest_ok = pytest_result.returncode == 0 and "passed" in pytest_output
        if not pytest_ok:
            print(f"  [FAIL] pytest in worktree exited {pytest_result.returncode}")
            return 1
        print("  [PASS] pytest passed inside the isolated worktree.")

        produced = {path.name for path in written}
        if produced != allowed_scope:
            print(f"  [FAIL] produced {produced}, expected {allowed_scope}")
            return 1

        for name in allowed_scope:
            shutil.copy2(worktree / name, MODULE_DIR / name)
            shutil.copy2(worktree / name, OUTPUT_DIR / name)

        telemetry_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task": "jwt_auth_multi_agent_handoff",
            "worktree": str(worktree),
            "branch": isolation.branch,
            "subtasks": len(subtasks),
            "pytest_returncode": pytest_result.returncode,
            "pytest_output": pytest_output,
        }
        with team.telemetry_log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(telemetry_record) + "\n")
        (OUTPUT_DIR / "run_evidence.json").write_text(
            json.dumps(telemetry_record, indent=2), encoding="utf-8"
        )
        print(f"[Self-Improvement Telemetry] Appended to {team.telemetry_log}")
        print(f"[OUTPUT] {OUTPUT_DIR / 'run_evidence.json'}")
    finally:
        isolation.remove()
        print("[Isolation] git worktree removed.")

    print("\nMODULE 8 DEMO COMPLETE: Worktree implement + real JWT tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
