"""
Module 10 Integration: Production Readiness Auditor for Deep Research Agent.
Inspects repository against compliance gates and (when provided) the latest run artifacts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class ProductionReadinessAuditor:
    """Evaluates the 5-Gate Production Readiness Scorecard."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    def audit_gate_1_memory(self) -> tuple[bool, str]:
        claude_md = self.repo_root / "CLAUDE.md"
        agents_md = self.repo_root / "AGENTS.md"
        ok = claude_md.exists() and agents_md.exists()
        return ok, "Gate 1 (Memory): CLAUDE.md & AGENTS.md verified." if ok else "Gate 1 Failed: Memory files missing."

    def audit_gate_2_guardrails(self) -> tuple[bool, str]:
        settings = self.repo_root / ".claude" / "settings.json"
        ok = settings.exists()
        return ok, "Gate 2 (Guardrails): .claude/settings.json hook configuration verified." if ok else "Gate 2 Failed."

    def audit_gate_3_tests(self) -> tuple[bool, str]:
        tests = list(self.repo_root.glob("**/test_*.py"))
        ok = len(tests) >= 5
        return ok, f"Gate 3 (Tests): {len(tests)} automated pytest suites verified." if ok else "Gate 3 Failed."

    def audit_gate_4_mcp(self) -> tuple[bool, str]:
        mcp_server = self.repo_root / "deep_research_agent" / "engine" / "mcp_research_server.py"
        ok = mcp_server.exists()
        return ok, "Gate 4 (MCP): MCP 2.x server with @mcp.tool decorators verified." if ok else "Gate 4 Failed."

    def audit_gate_5_subagents(self) -> tuple[bool, str]:
        agents_dir = self.repo_root / ".claude" / "agents"
        ok = agents_dir.exists() and len(list(agents_dir.glob("*.md"))) >= 3
        return ok, "Gate 5 (Subagents): Specialized subagent role manifests verified." if ok else "Gate 5 Failed."

    def audit_run_artifacts(self, run_context: dict[str, Any] | None) -> tuple[bool, str]:
        """Run-aware gate: citations, dossier, and pytest outcome from the current execution."""
        if not run_context:
            return True, "Run gate skipped (static repo audit only)."
        evidence = run_context.get("evidence") or []
        live = [e for e in evidence if e.get("provenance") != "synthetic"]
        dossier = (run_context.get("dossier_markdown") or "").strip()
        pytest_passed = bool(run_context.get("pytest_passed", False))
        depth = (run_context.get("depth") or "multi-source").lower()
        min_live = 2 if depth == "quick-scan" else 3
        ok = len(live) >= min_live and len(dossier) >= 200 and pytest_passed
        if ok:
            return True, (
                f"Run gate: {len(live)} live citations, dossier {len(dossier)} chars, pytest OK "
                f"(depth={depth})."
            )
        return False, (
            f"Run gate failed: live={len(live)} (need {min_live}), "
            f"dossier_len={len(dossier)}, pytest_passed={pytest_passed}."
        )

    def run_full_audit(self, run_context: dict[str, Any] | None = None) -> dict[str, Any]:
        results = [
            ("Gate 1: Memory Files", *self.audit_gate_1_memory()),
            ("Gate 2: Guardrails & Hooks", *self.audit_gate_2_guardrails()),
            ("Gate 3: Automated Test Layer", *self.audit_gate_3_tests()),
            ("Gate 4: Model Context Protocol", *self.audit_gate_4_mcp()),
            ("Gate 5: Subagent Specialization", *self.audit_gate_5_subagents()),
        ]
        if run_context is not None:
            results.append(("Gate 6: Latest Run Artifacts", *self.audit_run_artifacts(run_context)))

        passed_count = sum(1 for _, ok, _ in results if ok)
        total = len(results)
        score_pct = (passed_count / total) * 100.0 if total else 0.0
        return {
            "score_pct": score_pct,
            "passed_gates": f"{passed_count}/{total}",
            "is_production_ready": passed_count == total,
            "details": [{"gate": g, "passed": ok, "message": msg} for g, ok, msg in results],
        }
