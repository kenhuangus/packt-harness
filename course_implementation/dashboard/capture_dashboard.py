import os
from playwright.sync_api import sync_playwright

html_path = r"C:\Users\kenhu\packt\harness\course_implementation\dashboard\index.html"
file_url = "file:///" + html_path.replace("\\", "/")
out_img = r"C:\Users\kenhu\packt\harness\course_implementation\dashboard\dashboard_screenshot.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto(file_url)
    page.wait_for_timeout(1000)
    page.screenshot(path=out_img)
    browser.close()

print(f"SUCCESS! Screenshot captured to: {out_img}")
