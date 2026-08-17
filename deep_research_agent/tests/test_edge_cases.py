"""
Edge Case & Failure Defense Test Suite for Deep Research Agent (EC-01 to EC-08).
"""

from pathlib import Path
import pytest
import sys

from deep_research_agent.engine.escalation_gateway import PermissionEscalationGateway, RiskTier
from deep_research_agent.engine.guardrails import GuardrailsEngine
from deep_research_agent.engine.harness_stack import (
    ContextTokenBudgeter,
    LoopDetector,
    PathSanitizer,
)
from deep_research_agent.engine.tda_reliability import TdaReliabilityPipeline

WORKSPACE_DIR = Path(__file__).parent / "test_workspace"


def test_ec_01_loop_interception():
    """EC-01: Loop detector catches repeated identical queries."""
    detector = LoopDetector(threshold=2)
    allowed1, _ = detector.record_call("query_web_index", query="same query")
    allowed2, _ = detector.record_call("query_web_index", query="same query")

    assert allowed1 is True
    assert allowed2 is False, "Second identical query must be intercepted by loop detector."


def test_ec_02_path_traversal_blocking():
    """EC-02: Path traversal attempts raise PermissionError."""
    sanitizer = PathSanitizer(WORKSPACE_DIR)
    with pytest.raises(PermissionError):
        sanitizer.validate_path("../../etc/passwd")


def test_ec_03_dangerous_command_filtering():
    """EC-03: PreToolUse hook blocks --dangerously-skip-permissions and rm -rf."""
    guardrails = GuardrailsEngine()
    hook_input = {
        "hookName": "PreToolUse",
        "toolName": "bash",
        "toolInput": {"command": "claude --dangerously-skip-permissions run"},
    }
    decision = guardrails.intercept_pre_tool_use(hook_input)
    assert decision["status"] == "DENIED"
    assert decision["hookSpecificOutput"]["permissionDecision"] == "deny"


def test_ec_04_secret_scanning():
    """EC-04: High-entropy API keys are intercepted and flagged."""
    guardrails = GuardrailsEngine()
    bad_content = "Here is the key: sk-ant-api03-abcdef1234567890abcdef1234567890 for testing."
    findings = guardrails.scan_content_for_secrets(bad_content)
    assert len(findings) >= 1
    assert "Anthropic API Key" in findings[0]


def test_ec_05_critical_permission_escalation():
    """EC-05: Critical operations fail without valid cryptographic approval signature."""
    ledger_path = WORKSPACE_DIR / "test_approvals.json"
    if ledger_path.exists():
        ledger_path.unlink()

    gateway = PermissionEscalationGateway(ledger_path)
    assert gateway.evaluate_risk("export_production_dossier") == RiskTier.CRITICAL

    # Attempt without approval
    authorized, reason = gateway.authorize_operation("REQ-1234", "export_production_dossier")
    assert authorized is False
    assert "PERMISSION BLOCKED" in reason

    # Record valid signed approval
    gateway.record_approval("REQ-1234", "export_production_dossier", "lead_admin")
    authorized, _ = gateway.authorize_operation("REQ-1234", "export_production_dossier")
    assert authorized is True


def test_ec_06_context_token_compaction():
    """EC-06: Excessive evidence text is safely compacted with head/tail preservation."""
    budgeter = ContextTokenBudgeter(max_tokens=8000)
    huge_text = "HEAD_FACTS: " + ("evidence " * 1000) + " TAIL_FACTS"
    compacted = budgeter.compact_evidence(huge_text, max_chars=400)

    assert len(compacted) < len(huge_text)
    assert "HEAD_FACTS" in compacted
    assert "TAIL_FACTS" in compacted
    assert "OMITTED" in compacted


def test_ec_07_browser_crawlers_return_empty_without_playwright(monkeypatch):
    """EC-07: Browser-based crawlers must return empty results when Playwright is unavailable."""
    from deep_research_agent.engine import mcp_research_server as research_server

    monkeypatch.delitem(sys.modules, "playwright.sync_api", raising=False)

    real_import = __import__

    def guarded_import(name, *args, **kwargs):
        if name == "playwright.sync_api":
            raise ModuleNotFoundError("No module named 'playwright'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", guarded_import)

    assert research_server.fetch_live_github_sync("Harness Engineering", limit=2) == []
    assert research_server.fetch_live_youtube_sync("Autonomous Coding Agents", limit=2) == []
