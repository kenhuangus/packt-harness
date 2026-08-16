"""
Live End-to-End Validation of Deep Research Agent on Multiple Arbitrary Topics.
Tests live search, spec generation, guardrails, TDA pytest verification, and dossier synthesis.
"""

import asyncio
from pathlib import Path
import sys
import time

from deep_research_agent.engine.five_step_pipeline import FiveStepResearchPipeline

WORKSPACE_DIR = Path("deep_research_agent/output/live_test_workspace")

TEST_QUERIES = [
    "Quantum Error Correction in Topological Qubits",
    "CRISPR-Cas9 Prime Editing and Epigenetic Modifications in 2026",
    "Rust vs Go Concurrency Models in High-Throughput Cloud Microservices",
    "Zero Trust Cybersecurity Architecture in Kubernetes Clusters",
]

async def run_live_tests():
    print("=" * 80)
    print("EXECUTING LIVE DEEP RESEARCH ON 4 DIVERSE ARBITRARY TOPICS")
    print("=" * 80)
    
    pipeline = FiveStepResearchPipeline(WORKSPACE_DIR)
    
    for i, q in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/4] RUNNING DEEP RESEARCH ON: '{q}'...")
        t0 = time.time()
        
        result = await pipeline.execute_deep_research(q)
        elapsed = time.time() - t0
        
        print(f"  [STATUS]: {result['status']}")
        print(f"  [DURATION]: {elapsed:.2f}s")
        print(f"  [PIPELINE STEPS]: {len(result['pipeline_steps'])}/5 steps completed")
        print(f"  [EVIDENCE SOURCES]: {len(result['evidence'])} verified sources")
        
        # Display top 2 citations
        for c in result['evidence'][:2]:
            print(f"     * [{c.get('domain')}]: {c.get('title')[:60]}... (Trust: {c.get('confidence_score')*100:.0f}%)")
            
        print(f"  [DOSSIER LENGTH]: {len(result['dossier_markdown'])} chars generated")
        print(f"  [DOSSIER FILE]: {result['dossier_file']}")
        
        assert result["status"] == "SUCCESS"
        assert len(result["pipeline_steps"]) == 5
        assert len(result["evidence"]) >= 2
        assert Path(result["dossier_file"]).exists()
        
    print("\n" + "=" * 80)
    print(">>> ALL 4 DIVERSE TOPICS SUCCESSFULLY RESEARCHED & VERIFIED! <<<")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    asyncio.run(run_live_tests())
