"""Playwright UI field exercise for Deep Research Agent at localhost:8090."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8090/"
OUT = Path(__file__).parent / "output" / "ui_field_test"
OUT.mkdir(parents=True, exist_ok=True)

findings: list[dict] = []


def note(kind: str, field: str, detail: str) -> None:
    findings.append({"kind": kind, "field": field, "detail": detail})
    print(f"[{kind}] {field}: {detail}")


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.on("pageerror", lambda err: note("BUG", "pageerror", str(err)))
        page.on("console", lambda msg: note("CONSOLE", msg.type, msg.text) if msg.type in ("error", "warning") else None)

        page.goto(BASE, wait_until="networkidle", timeout=30000)
        page.screenshot(path=str(OUT / "01_home.png"), full_page=True)
        note("OK", "load", f"title={page.title()}")

        # Theme toggle
        theme_btn = page.locator("#themeToggle")
        before = page.locator("html").get_attribute("data-theme")
        theme_btn.click()
        after = page.locator("html").get_attribute("data-theme")
        if before == after:
            note("BUG", "themeToggle", f"theme did not change ({before})")
        else:
            note("OK", "themeToggle", f"{before} -> {after}")
        theme_btn.click()  # restore light

        # Query input
        q = page.locator("#queryInput")
        q.fill("UI Field Test: Harness Engineering Capstone")
        if q.input_value() != "UI Field Test: Harness Engineering Capstone":
            note("BUG", "queryInput", "value not set")
        else:
            note("OK", "queryInput", "accepts typed text")

        # Depth select — verify options & whether wired to API
        depth = page.locator("#depthSelect")
        options = depth.locator("option").all_text_contents()
        note("OK", "depthSelect.options", f"{len(options)} options: {options}")
        for val in ("deep-audit", "quick-scan", "multi-source"):
            depth.select_option(val)
            if depth.input_value() != val:
                note("BUG", "depthSelect", f"failed to select {val}")
            else:
                note("OK", "depthSelect", f"selected {val}")

        # Time horizon
        horizon = page.locator("#timeHorizonSelect")
        for val in ("7", "30", "90", "180", "365", "0"):
            horizon.select_option(val)
            if horizon.input_value() != val:
                note("BUG", "timeHorizonSelect", f"failed to select {val}")
            else:
                note("OK", "timeHorizonSelect", f"selected {val}")
        horizon.select_option("30")

        # Presets (sample life + AI)
        presets = page.locator(".preset-chip")
        count = presets.count()
        note("OK", "presets", f"found {count} chips")
        if count < 20:
            note("BUG", "presets", f"expected >=20 presets, got {count}")
        # click first life science and first AI
        presets.nth(0).click()
        v1 = q.input_value()
        if not v1:
            note("BUG", "preset.life", "did not fill query")
        else:
            note("OK", "preset.life", v1[:80])
        presets.nth(10).click()
        v2 = q.input_value()
        if v2 == v1:
            note("BUG", "preset.ai", "second preset did not change query")
        else:
            note("OK", "preset.ai", v2[:80])

        # Tabs before research (should not crash)
        for tab_id, name in (
            ("tabDossier", "dossier"),
            ("tabReflection", "reflection"),
            ("tabDiff", "diff"),
            ("tabAudit", "audit"),
        ):
            page.locator(f"#{tab_id}").click()
            active = page.locator(f"#{tab_id}").evaluate("el => el.classList.contains('active')")
            if not active:
                note("BUG", f"tab.{name}", "not marked active after click")
            else:
                note("OK", f"tab.{name}", "activates")

        # Capture whether depthSelect is sent in network body
        depth.select_option("quick-scan")
        q.fill("Quick UI smoke: MCP and harness engineering")
        horizon.select_option("7")

        captured: dict = {}

        def on_request(req):
            if "/api/research" in req.url and req.method == "POST":
                try:
                    captured["body"] = req.post_data
                except Exception as exc:  # noqa: BLE001
                    captured["err"] = str(exc)

        page.on("request", on_request)

        page.locator("#startBtn").click()
        # Modal should appear
        page.wait_for_selector("#researchProgressModal", state="visible", timeout=10000)
        note("OK", "progressModal", "opens on submit")
        page.screenshot(path=str(OUT / "02_modal.png"))

        # Wait for API (research can take a while with live crawl + LLM)
        try:
            # Wait for success UI (latestResult uses `let` and is not on window).
            page.wait_for_selector("#modalViewDossierBtn", state="visible", timeout=420000)
            note("OK", "research", "modalViewDossierBtn visible (pipeline finished)")
        except Exception as exc:  # noqa: BLE001
            note("BUG", "research", f"timed out waiting for result: {exc}")
            page.locator("#modalMinimizeBtn").click()
            page.screenshot(path=str(OUT / "03_timeout.png"), full_page=True)
            browser.close()
            Path(OUT / "findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
            return 1

        # Inspect API payload
        body = captured.get("body") or ""
        note("INFO", "api.body", body[:300])
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {}
            note("BUG", "api.body", "not JSON")
        if "days_back" not in payload:
            note("BUG", "timeHorizonSelect", "days_back not sent to API")
        elif payload.get("days_back") != 7:
            note("BUG", "timeHorizonSelect", f"expected days_back=7 got {payload.get('days_back')}")
        else:
            note("OK", "timeHorizonSelect.api", "days_back=7 sent")
        if payload.get("depth") != "quick-scan":
            note("BUG", "depthSelect", f"expected depth=quick-scan got {payload.get('depth')}")
        else:
            note("OK", "depthSelect.api", f"sent depth={payload.get('depth')}")

        # Close modal if still open
        if page.locator("#researchProgressModal").is_visible():
            view_btn = page.locator("#modalViewDossierBtn")
            if view_btn.is_visible():
                view_btn.click()
            else:
                page.locator("#modalMinimizeBtn").click()

        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / "04_results.png"), full_page=True)

        # Citations / dossier content
        dossier = page.locator("#dossierContent").inner_text()
        if "Execute Autonomous Research" in dossier and len(dossier) < 120:
            note("BUG", "dossier", "still showing empty placeholder after success")
        else:
            note("OK", "dossier", f"len={len(dossier)} preview={dossier[:120]!r}")

        cite_count = page.locator(".citation-card").count()
        note("OK" if cite_count > 0 else "BUG", "citations", f"{cite_count} cards")

        badge = page.locator("#evidenceCountBadge").inner_text()
        note("INFO", "evidenceBadge", badge)

        # Tabs with data
        for tab_id, name in (
            ("tabReflection", "reflection"),
            ("tabDiff", "diff"),
            ("tabAudit", "audit"),
            ("tabDossier", "dossier"),
        ):
            page.locator(f"#{tab_id}").click()
            page.wait_for_timeout(200)
            text = page.locator("#dossierContent").inner_text()
            if len(text.strip()) < 20:
                note("BUG", f"tab.{name}.content", "empty after research")
            else:
                note("OK", f"tab.{name}.content", f"len={len(text)}")
            page.screenshot(path=str(OUT / f"05_tab_{name}.png"))

        # Theme again after results (dark mode SVG)
        theme_btn.click()
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUT / "06_dark.png"), full_page=True)
        note("OK", "theme.afterResults", page.locator("html").get_attribute("data-theme"))

        # Cancel control present after submit path (may be hidden after success)
        cancel = page.locator("#modalCancelBtn")
        note("OK" if cancel.count() else "BUG", "cancelBtn", f"count={cancel.count()}")

        # Result should expose warnings / llm fields when available
        latest = page.evaluate("() => window.getLatestResult ? window.getLatestResult() : null")
        if not latest:
            note("BUG", "latestResult", "getLatestResult returned null")
        else:
            if "warnings" not in latest:
                note("BUG", "warnings", "missing warnings array on result")
            else:
                note("OK", "warnings", f"n={len(latest.get('warnings') or [])}")
            note("OK", "llm_live", f"{latest.get('llm_live')}")
            note("INFO", "include_browser", f"{latest.get('include_browser_sources')}")

        # Empty query validation
        page.locator("#queryInput").fill("")
        page.locator("#startBtn").click()
        # HTML5 required should block; modal should not open if empty
        page.wait_for_timeout(400)
        modal_vis = page.locator("#researchProgressModal").evaluate(
            "el => getComputedStyle(el).display !== 'none'"
        )
        # If required works, modal stays closed. If JS bypasses, bug.
        # Note: after previous run button may still be disabled — check
        btn_disabled = page.locator("#startBtn").is_disabled()
        note("INFO", "emptySubmit", f"modal_visible={modal_vis} btn_disabled={btn_disabled}")

        browser.close()

    Path(OUT / "findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    bugs = [f for f in findings if f["kind"] == "BUG"]
    print(f"\nSUMMARY: {len(bugs)} bugs, {len(findings)} notes -> {OUT}")
    return 1 if bugs else 0


if __name__ == "__main__":
    sys.exit(main())
