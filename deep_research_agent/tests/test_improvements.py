"""Regression tests for the 10 capstone improvements."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import pytest

from deep_research_agent.engine.evidence_utils import (
    clean_youtube_author,
    drop_synthetic_evidence,
    rank_and_filter_evidence,
    repair_evidence_structure,
)
from deep_research_agent.engine.five_step_pipeline import FiveStepResearchPipeline, PipelineCancelled
from deep_research_agent.engine.readiness_auditor import ProductionReadinessAuditor
from deep_research_agent.engine.tda_reliability import TdaReliabilityPipeline

WORKSPACE = Path(__file__).resolve().parents[1] / "output" / "test_workspace_improvements"


def test_imp_01_no_synthetic_guaranteed_fillers():
    """Improvement 1: synthetic / guaranteed docs are dropped."""
    evidence = [
        {"doc_id": "yt_guaranteed_01_1", "title": "Fake", "provenance": "synthetic"},
        {"doc_id": "arxiv_1", "title": "Real", "provenance": "live", "text": "harness engineering agents"},
        {"doc_id": "openalex_fallback_9", "title": "Stub"},
        {"doc_id": "doc_general_01", "title": "Generic"},
    ]
    kept, n = drop_synthetic_evidence(evidence)
    assert n >= 3
    assert all("guaranteed" not in e["doc_id"] for e in kept)
    assert all("fallback" not in e["doc_id"] for e in kept)
    assert all(not e["doc_id"].startswith("doc_general_") for e in kept)


def test_imp_02_tda_repair_does_not_inflate_confidence():
    """Improvement 2: structural repair never sets all scores to 0.95."""
    raw = [
        {"doc_id": "a", "title": "Harness Engineering", "confidence_score": 0.2, "text": "harness"},
        {"doc_id": "", "title": "", "confidence_score": "bad", "url": "https://example.com"},
    ]
    repaired = repair_evidence_structure(raw, "Harness Engineering")
    assert repaired[0]["confidence_score"] == 0.30  # clamped floor, not 0.95
    assert all(item.get("confidence_score", 0) < 0.95 for item in repaired)
    assert repaired[1]["doc_id"]
    assert repaired[1]["title"]


def test_imp_03_progress_callback_emits_steps():
    """Improvement 3: pipeline emits real step progress events."""
    events: list[str] = []

    def cb(event_type: str, details: dict) -> None:
        events.append(event_type)

    pipeline = FiveStepResearchPipeline(WORKSPACE / "progress")
    result = pipeline.execute_deep_research(
        "Harness Engineering for AI Agents",
        days_back=30,
        depth="quick-scan",
        progress_cb=cb,
    )
    assert result["status"] in {"SUCCESS", "PARTIAL"}
    assert any(e.startswith("STEP_1") for e in events)
    assert any(e.startswith("STEP_2") for e in events)
    assert "PIPELINE_COMPLETE" in events


def test_imp_04_evidence_ranking_prefers_relevant():
    """Improvement 4: relevant docs rank above off-topic ones."""
    query = "Harness Engineering for Agentic AI"
    evidence = [
        {"doc_id": "1", "title": "Elliptic PDE estimates", "text": "Sobolev spaces", "confidence_score": 0.9},
        {"doc_id": "2", "title": "Harness Engineering for Agents", "text": "agentic harness scaffolding", "confidence_score": 0.5},
    ]
    ranked, _ = rank_and_filter_evidence(query, evidence, min_score=0.0, keep_at_least=2)
    assert ranked[0]["doc_id"] == "2"
    assert ranked[0]["relevance_score"] > ranked[1]["relevance_score"]


def test_imp_05_youtube_author_cleanup():
    """Improvement 5: duplicated channel + view metadata stripped."""
    assert clean_youtube_author("IBM Technology IBM Technology (181K 1mo ago)") == "IBM Technology"
    assert clean_youtube_author("Aishwarya Srinivasan Aishwarya Srinivasan") == "Aishwarya Srinivasan"


def test_imp_06_warnings_and_llm_fields_present():
    """Improvement 6: warnings + llm status returned."""
    pipeline = FiveStepResearchPipeline(WORKSPACE / "warn")
    result = pipeline.execute_deep_research("Harness Engineering", days_back=7, depth="quick-scan")
    assert "warnings" in result
    assert isinstance(result["warnings"], list)
    assert "llm_live" in result
    assert "llm_provider" in result


def test_imp_07_quick_scan_skips_browser():
    """Improvement 7: quick-scan disables Playwright sources."""
    pipeline = FiveStepResearchPipeline(WORKSPACE / "quick")
    result = pipeline.execute_deep_research("Harness Engineering MCP", days_back=30, depth="quick-scan")
    assert result["include_browser_sources"] is False
    assert all(e.get("source_type") not in {"github", "youtube"} for e in result["evidence"])
    assert any("quick-scan" in w.lower() or "skipped" in w.lower() for w in result["warnings"])


def test_imp_08_flat_workspace_and_cancel():
    """Improvement 8: no nested output/output; cancel raises PipelineCancelled."""
    root = WORKSPACE / "flat_ws"
    pipeline = FiveStepResearchPipeline(root)
    assert pipeline.output_dir == root.resolve()
    assert not str(pipeline.output_dir).endswith(str(Path("output") / "output"))

    cancel = threading.Event()
    cancel.set()
    with pytest.raises(PipelineCancelled):
        pipeline.execute_deep_research("x", depth="quick-scan", cancel_event=cancel)


def test_imp_09_run_aware_audit():
    """Improvement 9: auditor scores latest run artifacts when provided."""
    repo = Path(__file__).parents[2]
    auditor = ProductionReadinessAuditor(repo)
    static = auditor.run_full_audit()
    assert static["passed_gates"] == "5/5"

    good = auditor.run_full_audit(
        run_context={
            "evidence": [
                {"doc_id": "a", "provenance": "live"},
                {"doc_id": "b", "provenance": "live"},
                {"doc_id": "c", "provenance": "live"},
            ],
            "dossier_markdown": "x" * 250,
            "pytest_passed": True,
            "depth": "multi-source",
        }
    )
    assert good["passed_gates"] == "6/6"
    assert good["is_production_ready"] is True

    bad = auditor.run_full_audit(
        run_context={
            "evidence": [],
            "dossier_markdown": "short",
            "pytest_passed": False,
            "depth": "multi-source",
        }
    )
    assert bad["is_production_ready"] is False


def test_imp_10_depth_aware_tda_suite(tmp_path: Path):
    """Improvement 10 helper: quick-scan suite does not require YT/GH."""
    tda = TdaReliabilityPipeline(tmp_path)
    cites = tmp_path / "citations.json"
    cites.write_text(
        json.dumps(
            [
                {
                    "doc_id": "w1",
                    "title": "Wiki",
                    "source_type": "wikipedia",
                    "confidence_score": 0.4,
                    "provenance": "live",
                },
                {
                    "doc_id": "a1",
                    "title": "Paper",
                    "source_type": "arxiv",
                    "confidence_score": 0.5,
                    "provenance": "live",
                },
            ]
        ),
        encoding="utf-8",
    )
    suite = tda.write_citation_test_suite(cites, depth="quick-scan")
    text = suite.read_text(encoding="utf-8")
    assert "REQUIRE_YOUTUBE = 0" in text
    assert "REQUIRE_GITHUB = 0" in text
    passed, out, code = tda.run_pytest(suite)
    assert passed, out
