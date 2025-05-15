# ArticleScraper_Agent.py
# Scrapes readable content from article URLs and saves to /Raw/ for Vault ingestion

import os
import datetime
import json
import requests
from bs4 import BeautifulSoup

SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Raw"))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119 Safari/537.36"
}

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    for script in soup(["script", "style", "noscript", "footer", "header", "form", "nav", "aside"]):
        script.extract()
    text = soup.get_text(separator=' ')
    return ' '.join(text.split())

def scrape_article(url):
    try:
        print(f"[FETCHING] {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        content = clean_html(response.text)
        return content
    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None

def save_article(content, url):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    slug = url.replace("https://", "").replace("http://", "").replace("/", "_").split("?")[0][:60]
    base_name = f"article_{slug}_{timestamp}"

    os.makedirs(SAVE_DIR, exist_ok=True)
    txt_path = os.path.join(SAVE_DIR, f"{base_name}.txt")
    md_path = os.path.join(SAVE_DIR, f"{base_name}.md")
    json_path = os.path.join(SAVE_DIR, f"{base_name}.json")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Article Content\n\n{content}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"url": url, "content": content}, f, indent=2)

    print(f"[SAVED] {txt_path}\n[SAVED] {md_path}\n[SAVED] {json_path}")
    return base_name

def run_scraper(urls):
    for url in urls:
        content = scrape_article(url)
        if content:
            save_article(content, url)

if __name__ == "__main__":
    # 🔁 Example usage
    urls = [
        "https://blog.samaltman.com/ai-the-most-important-questions",
        "https://www.navalmanack.com/"
    ]
    run_scraper(urls)
    print("✅ Article scrape complete.")

import subprocess
subprocess.run(["python", "VaultProcessor_AI.py"], cwd=os.path.dirname(__file__))
