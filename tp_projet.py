
# faire uv run tp_projet.py 
from playwright.sync_api import Page, expect, sync_playwright
import csv

url = 'https://www.youtube.com/watch?v=8hK732DrDU8'
nScrolls = 10

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    consentCss = 'ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > yt-button-shape:nth-child(1) > button:nth-child(1)'
    page.wait_for_selector(consentCss)
    page.click(consentCss)

# Attendre que la section commentaires existe
    page.wait_for_selector('#comments', timeout=15000)

    collected_comments = set()

    for i in range(nScrolls):
        page.keyboard.press('PageDown')
        page.wait_for_timeout(1000)
        #input('press enter')
        height = page.evaluate('document.documentElement.scrollHeight')
        comments = page.query_selector_all('#content-text > span')
        for el in comments:
            text = el.inner_text().strip()
            if text:
                collected_comments.add(text)

        print(f"Scroll {i+1} → {len(collected_comments)} commentaires uniques")

    browser.close()

with open("comments.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["comment"])
    for c in collected_comments:
        writer.writerow([c])