"""
Generates actual live Web UI screenshots for multiple real-world search terms,
tabs (Dossier, Diff, Audit), and theme modes using Playwright.
"""

import asyncio
from pathlib import Path
import time
from playwright.async_api import async_playwright

SCREENSHOTS_DIR = Path("deep_research_agent/demo/actual_ui_screens")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

TOPICS = [
    {
        "id": "harness_ai",
        "query": "Harness Engineering for Agentic AI Systems",
        "label": "Harness Engineering for Agentic AI",
    },
    {
        "id": "quantum_qec",
        "query": "Quantum Error Correction in Topological Qubits",
        "label": "Quantum Error Correction & Topological Qubits",
    },
    {
        "id": "zero_trust_k8s",
        "query": "Zero Trust Cybersecurity Architecture in Kubernetes",
        "label": "Zero Trust Architecture in Kubernetes",
    },
    {
        "id": "crispr_editing",
        "query": "CRISPR-Cas9 Prime Editing and Epigenetic Modifications",
        "label": "CRISPR-Cas9 Prime Editing in 2026",
    },
]


async def capture_all_ui_screens():
    print("=" * 80)
    print("CAPTURING ACTUAL LIVE WEB UI SCREENSHOTS FOR DIVERSE SEARCH TERMS")
    print("=" * 80)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        # 1. Initial Empty State
        print("[*] Capturing Initial Empty State...")
        await page.goto("http://localhost:8090/", wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(SCREENSHOTS_DIR / "01_initial_dashboard_empty.png"))

        # Loop through diverse topics
        for idx, topic in enumerate(TOPICS, 2):
            print(f"[*] Executing live research for '{topic['query']}'...")
            await page.fill("#queryInput", topic["query"])
            await page.click("#startBtn")

            # Wait for results to render
            await page.wait_for_selector(".citation-card", timeout=40000)
            await page.wait_for_timeout(2000)

            # Capture main results dashboard
            main_path = SCREENSHOTS_DIR / f"{idx:02d}_{topic['id']}_results.png"
            await page.screenshot(path=str(main_path))
            print(f"  [OK] Saved {main_path.name}")

            # If first topic, capture Diff and Audit tabs and light theme
            if topic["id"] == "harness_ai":
                # Tab: Unified Diff
                await page.click("#tabDiff")
                await page.wait_for_timeout(1000)
                diff_path = SCREENSHOTS_DIR / "03_harness_unified_diff_tab.png"
                await page.screenshot(path=str(diff_path))
                print(f"  [OK] Saved {diff_path.name}")

                # Tab: Audit Scorecard
                await page.click("#tabAudit")
                await page.wait_for_timeout(1000)
                audit_path = SCREENSHOTS_DIR / "04_harness_audit_scorecard_tab.png"
                await page.screenshot(path=str(audit_path))
                print(f"  [OK] Saved {audit_path.name}")

                # Switch back to Dossier tab
                await page.click("#tabDossier")
                await page.wait_for_timeout(500)

        # Toggle Light Theme Mode
        print("[*] Toggling Light Theme Mode...")
        await page.click("#themeToggle")
        await page.wait_for_timeout(1000)
        light_path = SCREENSHOTS_DIR / "08_light_theme_mode.png"
        await page.screenshot(path=str(light_path))
        print(f"  [OK] Saved {light_path.name}")

        await browser.close()

    print("\n" + "=" * 80)
    print(f">>> CAPTURED ALL ACTUAL LIVE UI SCREENSHOTS IN {SCREENSHOTS_DIR} <<<")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(capture_all_ui_screens())
