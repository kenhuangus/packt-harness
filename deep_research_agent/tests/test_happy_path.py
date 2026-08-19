"""
Happy Path Test Suite for Deep Research Agent (HP-01 to HP-06).
"""

import asyncio
from pathlib import Path
import pytest

from deep_research_agent.engine.five_step_pipeline import FiveStepResearchPipeline
from deep_research_agent.engine.harness_stack import ContextTokenBudgeter, PathSanitizer
from deep_research_agent.engine.mcp_research_server import query_web_index, verify_citation_claim
from deep_research_agent.engine.readiness_auditor import ProductionReadinessAuditor
from deep_research_agent.engine.research_team import MultiAgentResearchTeam
from deep_research_agent.engine.spec_verifier import SpecVerifier

WORKSPACE_DIR = Path(__file__).parent / "test_workspace"


def _require_playwright_live_crawl(test_name: str) -> None:
    """Skips tests that require a real browser crawl when Playwright runtime is unavailable."""
    sync_api = pytest.importorskip(
        "playwright.sync_api",
        reason=f"{test_name} requires Playwright for a real live crawl.",
    )
    try:
        with sync_api.sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            browser.close()
    except Exception as exc:
        pytest.skip(f"{test_name} requires Playwright Chromium runtime: {exc}")


def _skip_if_crawl_returned_nothing(test_name: str, source: str, items: list, warn_output: str) -> None:
    """A live crawl can legitimately return zero documents (rate limiting, bot
    detection, or the machine being offline). That is not a code failure, so the
    test must skip rather than fail or fabricate a pass."""
    if items:
        return
    warn_line = next((line for line in warn_output.splitlines() if line.startswith("[WARN]")), "")
    cause = warn_line or "no [WARN] diagnostic was captured for this run"
    pytest.skip(f"{test_name} skipped: live {source} crawl returned zero documents this run ({cause}).")


def test_hp_01_spec_parsing():
    """HP-01: Spec formulation & whitelist extraction."""
    spec_text = """# RESEARCH SPECIFICATION: Deep Learning Benchmarks
## 1. Objective
- Primary Question: Benchmark comparison
## 2. Allowed Scope
- In-Scope Files: output/reports/*.md, output/citations/*.json
## 3. Explicit Non-Goals
- Blocked: database writes, promotional marketing
## 4. Acceptance Criteria
- AC-01: Citations >= 3
"""
    verifier = SpecVerifier(spec_text)
    assert verifier.is_file_allowed("output/reports/dossier.md")
    assert verifier.is_file_allowed("output/citations/citations.json")
    assert not verifier.is_file_allowed("secret_keys/api.key")
    violations = verifier.validate_non_goals("Let us connect_db and execute_sql now.")
    assert len(violations) >= 1


def test_hp_02_mcp_search_and_citation_verify():
    """HP-02 & HP-04: MCP search and citation claim validation."""
    raw_res = query_web_index("Harness Engineering 5 pillars", max_results=3)
    assert '"status": "SUCCESS"' in raw_res
    assert '"results":' in raw_res

    claim_res = verify_citation_claim("Harness Engineering eliminates execution loops", "doc_001")
    assert "verified\": true" in claim_res.lower()


def test_hp_03_multi_agent_planner():
    """HP-03: Multi-agent planner sub-query decomposition."""
    team = MultiAgentResearchTeam(WORKSPACE_DIR, WORKSPACE_DIR / "telemetry.jsonl")
    subs = team.run_planner("Autonomous Agent Governance")
    assert len(subs) == 4
    assert all("query" in s for s in subs)


def test_hp_05_five_step_pipeline_execution():
    """HP-05: 5-Step SOP Pipeline execution end-to-end."""
    pipeline = FiveStepResearchPipeline(WORKSPACE_DIR)
    result = pipeline.execute_deep_research("Autonomous Harness Engineering")

    assert result["status"] == "SUCCESS"
    assert len(result["pipeline_steps"]) == 5
    assert len(result["evidence"]) >= 2
    assert Path(result["dossier_file"]).exists()
    assert Path(result["diff_file"]).exists()


def test_hp_06_production_readiness_audit():
    """HP-06: 10-Module 5-Gate Production Readiness Audit."""
    repo_root = Path(__file__).parents[2]
    auditor = ProductionReadinessAuditor(repo_root)
    audit_res = auditor.run_full_audit()

    assert audit_res["is_production_ready"] is True
    assert audit_res["score_pct"] == 100.0
    assert audit_res["passed_gates"] == "5/5"


def test_hp_07_github_search_no_api(capsys):
    """HP-07: Public GitHub code and repository search without API key."""
    _require_playwright_live_crawl("HP-07")
    from deep_research_agent.engine.mcp_research_server import search_github_code
    res_raw = search_github_code("Harness Engineering", limit=2)
    warn_output = capsys.readouterr().out
    import json
    data = json.loads(res_raw)
    repos = data.get("repositories", [])
    _skip_if_crawl_returned_nothing("HP-07", "GitHub", repos, warn_output)
    assert len(repos) >= 1
    assert "url" in repos[0]


def test_hp_08_youtube_search_no_api(capsys):
    """HP-08: Public YouTube video search without API key."""
    _require_playwright_live_crawl("HP-08")
    from deep_research_agent.engine.mcp_research_server import search_youtube_videos
    res_raw = search_youtube_videos("Model Context Protocol", limit=2)
    warn_output = capsys.readouterr().out
    import json
    data = json.loads(res_raw)
    videos = data.get("videos", [])
    _skip_if_crawl_returned_nothing("HP-08", "YouTube", videos, warn_output)
    assert len(videos) >= 1
    assert "youtube.com" in videos[0]["url"]


def test_hp_09_hackernews_and_openalex_no_api():
    """HP-09: HackerNews Algolia and OpenAlex scientific paper search."""
    from deep_research_agent.engine.mcp_research_server import fetch_live_hackernews, fetch_live_openalex
    hn_posts = fetch_live_hackernews("Claude Code MCP", limit=2)
    assert isinstance(hn_posts, list)
    if hn_posts:
        assert hn_posts[0]["source_type"] == "hackernews"
        assert "http" in hn_posts[0]["url"]

    oa_papers = fetch_live_openalex("Autonomous Agents", limit=2)
    assert isinstance(oa_papers, list)
    if oa_papers:
        assert oa_papers[0]["domain"] == "openalex.org"


def test_hp_10_aisuite_llm_client():
    """HP-10: aisuite LLM Client multi-provider configuration & fallback."""
    from deep_research_agent.engine.llm_client import ResearchLLMClient
    client = ResearchLLMClient()
    assert client.provider in ["openai", "anthropic", "google", "ollama", "openrouter", "deepseek"]
    assert client.model is not None
    # Client initialize must not crash
    out = client.generate("Test prompt")
    assert isinstance(out, str)


def test_hp_11_two_turn_self_reflection():
    """HP-11: Two-turn self-reflection and in-depth review workflow."""
    from deep_research_agent.engine.research_team import MultiAgentResearchTeam
    team = MultiAgentResearchTeam(WORKSPACE_DIR, WORKSPACE_DIR / "telemetry.jsonl")
    evidence = [
        {"doc_id": "d1", "title": "Paper 1", "domain": "arxiv.org", "snippet": "Theorem on convergence", "source_type": "arxiv"},
        {"doc_id": "d2", "title": "Repo 2", "domain": "github.com", "snippet": "Implementation patterns", "source_type": "github"},
    ]
    t1 = team.run_reflection_turn_1("Test Query", evidence)
    assert t1["turn"] == 1
    assert t1["status"] == "APPROVED"
    assert "reflection_analysis" in t1

    t2 = team.run_reflection_turn_2("Test Query", evidence, t1)
    assert t2["turn"] == 2
    assert t2["status"] == "FINALIZED"
    assert "reflection_analysis" in t2

    dossier = team.run_synthesizer("Test Query", evidence, t1, t2)
    assert "Multi-Turn Agentic Self-Reflection" in dossier
    assert "Turn 1 Self-Reflection" in dossier
    assert "Turn 2 Self-Reflection" in dossier


