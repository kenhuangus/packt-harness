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
    assert "Harness Engineering" in raw_res

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
    result = asyncio.run(pipeline.execute_deep_research("Autonomous Harness Engineering"))

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


def test_hp_07_github_search_no_api():
    """HP-07: Public GitHub code and repository search without API key."""
    from deep_research_agent.engine.mcp_research_server import search_github_code
    res_raw = search_github_code("Harness Engineering", limit=2)
    import json
    data = json.loads(res_raw)
    assert data["status"] == "SUCCESS"
    assert len(data["repositories"]) >= 1
    assert any("github.com" in r["url"] for r in data["repositories"])


def test_hp_08_youtube_search_no_api():
    """HP-08: Public YouTube video talk search without API key."""
    from deep_research_agent.engine.mcp_research_server import search_youtube_videos
    res_raw = search_youtube_videos("Autonomous Coding Agents", limit=2)
    import json
    data = json.loads(res_raw)
    assert data["status"] == "SUCCESS"
    assert len(data["videos"]) >= 1
    assert any("youtube.com" in v["url"] for v in data["videos"])


def test_hp_09_hackernews_and_openalex_no_api():
    """HP-09: HackerNews Algolia discussions and OpenAlex scholarly citations without API key."""
    from deep_research_agent.engine.mcp_research_server import search_hackernews, fetch_live_openalex
    import json
    hn_raw = search_hackernews("Agentic AI", limit=2)
    hn_data = json.loads(hn_raw)
    assert hn_data["status"] == "SUCCESS"
    assert len(hn_data["discussions"]) >= 1

    alex_docs = fetch_live_openalex("Autonomous Agents", limit=2)
    assert len(alex_docs) >= 1
    assert any("openalex.org" in d["domain"] for d in alex_docs)


def test_hp_10_aisuite_llm_client():
    """HP-10: aisuite LLM Client multi-provider configuration & fallback."""
    from deep_research_agent.engine.llm_client import ResearchLLMClient
    client = ResearchLLMClient()
    assert client.provider in ["openai", "anthropic", "google", "ollama"]
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


