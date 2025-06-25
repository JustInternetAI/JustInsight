import feedparser
import json
import os
import re
import time
import datetime
from playwright.sync_api import sync_playwright

INTERVAL = 3600  # seconds (1 hour)

os.makedirs('./data/raw/ap/', exist_ok=True)

def fetch_feed():
    # Download and parse the feed
    return feedparser.parse('https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en')

def slugify(text):
    # Convert title to a filesystem-friendly slug
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def format_date(entry):
    # Extract and format the published date
    try:
        dt = datetime.datetime(*entry.published_parsed[:6])
        return dt.strftime("%Y-%m-%d")
    except:
        return "unknown-date"

def fetch_full_article(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=15000)

            # Wait for the main article body to load
            page.wait_for_selector('div.RichTextStoryBody', timeout=5000)

            # Extract the text content from the paragraphs inside the body
            content = page.query_selector_all('div.RichTextStoryBody p')
            full_text = "\n".join(p.inner_text() for p in content)

            browser.close()
            return full_text.strip()

    except Exception as e:
        print(f"Playwright error fetching {url}: {e}")
        return ""
    
def save_entry(entry):
    # Save the entry as a JSON file
    title_slug = slugify(entry.title)
    date_str = format_date(entry)
    filename = f"feed_{date_str}_{title_slug}.json"
    filepath = os.path.join('./data/raw/ap/', filename)
    full_text = fetch_full_article(entry.link)

    # Avoid overwriting if file already exists
    if os.path.exists(filepath):
        return False

    data = {
        "title": entry.title,
        "link": entry.link,
        "published": entry.get("published", ""),
        "summary": entry.get("summary", ""),
        "full_text": full_text
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return True

def check_and_save_new_entries():
    feed = fetch_feed()
    new_count = 0

    for entry in feed.entries:
        saved = save_entry(entry)
        if saved:
            new_count += 1

    print(f"Saved {new_count} new entries.")

if __name__ == '__main__':
    import sys

    if '--once' in sys.argv:
        check_and_save_new_entries()
    else:
        while True:
            check_and_save_new_entries()
            time.sleep(INTERVAL)

