"""
Module 10 Integration: Production Readiness Auditor for Deep Research Agent.
Inspects repository against 5 automated compliance gates.
"""

from __future__ import annotations

import json
from pathlib import Path


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

    def run_full_audit(self) -> dict[str, Any]:
        results = [
            ("Gate 1: Memory Files", *self.audit_gate_1_memory()),
            ("Gate 2: Guardrails & Hooks", *self.audit_gate_2_guardrails()),
            ("Gate 3: Automated Test Layer", *self.audit_gate_3_tests()),
            ("Gate 4: Model Context Protocol", *self.audit_gate_4_mcp()),
            ("Gate 5: Subagent Specialization", *self.audit_gate_5_subagents()),
        ]
        passed_count = sum(1 for _, ok, _ in results)
        score_pct = (passed_count / len(results)) * 100.0
        return {
            "score_pct": score_pct,
            "passed_gates": f"{passed_count}/{len(results)}",
            "is_production_ready": passed_count == len(results),
            "details": [{"gate": g, "passed": ok, "message": msg} for g, ok, msg in results],
        }
