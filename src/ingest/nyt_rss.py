import feedparser
import json
import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup
import hashlib

INTERVAL = 3600  # seconds (1 hour)
HASHES = './data/raw/saved_hashes.json'

os.makedirs('./data/raw/nyt/', exist_ok=True)

def fetch_feed():
    # Download and parse the feed
    return feedparser.parse('https://rss.nytimes.com/services/xml/rss/nyt/World.xml')

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
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for main content section (works for most NYT articles)
        main = soup.find('main')
        if not main:
            return ""

        paragraphs = main.find_all('p')
        full_text = "\n".join(p.get_text() for p in paragraphs)
        return full_text.strip()

    except Exception as e:
        print(f"Error fetching full article: {e}")
        return ""

def load_saved_hashes():
    if os.path.exists(HASHES):
        with open(HASHES, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

def save_hashes(hashes):
    with open(HASHES, 'w', encoding='utf-8') as f:
        json.dump(list(hashes), f, indent=2)

def generate_entry_hash(entry):
    hash_input = f"{entry.title}{entry.link}{entry.get('published', '')}"
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

def save_entry(entry):
    saved_hashes = load_saved_hashes()
    entry_hash = generate_entry_hash(entry)

    if entry_hash in saved_hashes:
        return False  # Already saved
    
    # Save the entry as a JSON file
    title_slug = slugify(entry.title)
    date_str = format_date(entry)
    filename = f"feed_{date_str}_{title_slug}.json"
    filepath = os.path.join('./data/raw/nyt/', filename)
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

    saved_hashes.add(entry_hash)
    save_hashes(saved_hashes)

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
