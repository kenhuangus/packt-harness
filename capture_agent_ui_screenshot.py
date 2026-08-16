"""
Captures high-resolution screenshots of the live Deep Research Agent Web UI
executing an end-to-end research session on:
'Harness Engineering for Agentic AI Systems'.
"""

import asyncio
from pathlib import Path
import shutil
import sys
from playwright.async_api import async_playwright

ARTIFACT_DIR = Path(r"C:\Users\kenhu\.gemini\antigravity-cli\brain\34f929e5-1335-4eeb-a7ac-dfb192af729a")
DEMO_DIR = Path("deep_research_agent/demo")
DEMO_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    print("=" * 80)
    print("CAPTURING HIGH-RESOLUTION LIVE WEB UI SCREENSHOTS VIA PLAYWRIGHT")
    print("=" * 80)

    async with async_playwright() as p:
        # Launch browser with 1920x1080 resolution
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        print("[1] Opening http://localhost:8090/...")
        await page.goto("http://localhost:8090/", wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        query = "Harness Engineering for Agentic AI Systems"
        print(f"[2] Entering research query: '{query}'...")
        await page.fill("#queryInput", query)

        print("[3] Clicking 'Execute Autonomous Research'...")
        await page.click("#startBtn")

        # Wait for the research results to populate
        print("[4] Waiting for research pipeline to complete...")
        await page.wait_for_selector(".citation-card", timeout=40000)
        await page.wait_for_timeout(2000)  # Allow SVG animations and citation cards to settle

        # 1. Full Dashboard Viewport (1920x1080)
        img_main = DEMO_DIR / "live_agent_ui_dashboard.png"
        await page.screenshot(path=str(img_main))
        print(f"  [OK] Saved main dashboard: {img_main} ({img_main.stat().st_size} bytes)")

        # 2. Entire Full Page Screenshot
        img_full = DEMO_DIR / "live_agent_ui_full_page.png"
        await page.screenshot(path=str(img_full), full_page=True)
        print(f"  [OK] Saved full page: {img_full} ({img_full.stat().st_size} bytes)")

        # 3. Interactive Research Graph & Citations Section
        center_elem = await page.query_selector(".center-col")
        if center_elem:
            img_center = DEMO_DIR / "live_agent_ui_graph_citations.png"
            await center_elem.screenshot(path=str(img_center))
            print(f"  [OK] Saved graph & citations: {img_center} ({img_center.stat().st_size} bytes)")

        # 4. Synthesized Dossier View Section
        right_elem = await page.query_selector(".right-col")
        if right_elem:
            img_right = DEMO_DIR / "live_agent_ui_dossier.png"
            await right_elem.screenshot(path=str(img_right))
            print(f"  [OK] Saved dossier view: {img_right} ({img_right.stat().st_size} bytes)")

        # Copy to artifact directory for embedding in agent response
        for f in [img_main, img_full, DEMO_DIR / "live_agent_ui_graph_citations.png", DEMO_DIR / "live_agent_ui_dossier.png"]:
            if f.exists():
                shutil.copy(f, ARTIFACT_DIR / f.name)
                print(f"  [OK] Copied {f.name} to artifact directory.")

        await browser.close()

    print("\n" + "=" * 80)
    print(">>> PLAYWRIGHT SCREENSHOT CAPTURE COMPLETED SUCCESSFULLY! <<<")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
