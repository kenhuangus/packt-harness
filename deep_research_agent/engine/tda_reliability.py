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

    def write_citation_test_suite(self, citations_path: Path, depth: str = "multi-source") -> Path:
        """Writes pytest suite. Depth controls minimum counts (no forced fake modalities)."""
        depth_mode = (depth or "multi-source").strip().lower()
        if depth_mode == "quick-scan":
            min_citations = 2
            require_youtube = 0
            require_github = 0
        elif depth_mode == "deep-audit":
            min_citations = 4
            require_youtube = 1
            require_github = 1
        else:
            min_citations = 3
            require_youtube = 1
            require_github = 1

        test_file = self.tests_dir / "test_citations_integrity.py"
        test_code = f"""import json
import pytest
from pathlib import Path

DEPTH = {depth_mode!r}
MIN_CITATIONS = {min_citations}
REQUIRE_YOUTUBE = {require_youtube}
REQUIRE_GITHUB = {require_github}

def test_citation_integrity():
    cit_path = Path(r"{citations_path.resolve()}")
    assert cit_path.exists(), "Citations JSON file must exist on disk."
    data = json.loads(cit_path.read_text(encoding="utf-8"))
    # Exclude synthetic fillers from hard quotas
    live = [item for item in data if item.get("provenance") != "synthetic"]
    assert len(live) >= MIN_CITATIONS, (
        f"Report must contain at least {{MIN_CITATIONS}} live citations for depth={{DEPTH}} (found {{len(live)}})."
    )
    for item in live:
        assert "doc_id" in item, "Each citation item must contain 'doc_id'."
        assert "title" in item, "Each citation item must contain 'title'."
        assert item.get("confidence_score", 0) >= 0.30, "Citation confidence score must be >= 0.30."

    youtube_count = sum(
        1 for item in live
        if item.get("source_type") == "youtube" or "youtube.com" in item.get("domain", "")
    )
    if REQUIRE_YOUTUBE:
        assert youtube_count >= REQUIRE_YOUTUBE, (
            f"Depth {{DEPTH}} expects >= {{REQUIRE_YOUTUBE}} YouTube sources (found {{youtube_count}})."
        )

    github_count = sum(
        1 for item in live
        if item.get("source_type") == "github" or "github.com" in item.get("domain", "")
    )
    if REQUIRE_GITHUB:
        assert github_count >= REQUIRE_GITHUB, (
            f"Depth {{DEPTH}} expects >= {{REQUIRE_GITHUB}} GitHub sources (found {{github_count}})."
        )
"""
        test_file.write_text(test_code, encoding="utf-8")
        return test_file

    def run_pytest(self, test_file: Path) -> tuple[bool, str, int]:
        """Runs pytest on the test file, returning (passed, output_traceback, exit_code)."""
        cmd = [sys.executable, "-m", "pytest", str(test_file), "-q"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace)
        passed = res.returncode == 0
        output = res.stdout + "\n" + res.stderr
        return passed, output.strip(), res.returncode

    def append_anti_regression_guard(self, test_file: Path, guard_name: str, assertion_code: str) -> None:
        """Persists a new regression test guard to prevent repeating failures."""
        guard_fn = f"\n\ndef {guard_name}():\n    {assertion_code}\n"
        with open(test_file, "a", encoding="utf-8") as f:
            f.write(guard_fn)
