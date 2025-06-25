import feedparser
import json
import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup

INTERVAL = 3600  # seconds (1 hour)

os.makedirs('./data/raw/cnn/', exist_ok=True)

def fetch_feed():
    # Download and parse the feed
    return feedparser.parse('http://rss.cnn.com/rss/cnn_world.rss')

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
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # CNN article content is usually within <div class="article__content"> or <section id="body-text">
        article_section = soup.find('section', id='body-text') or soup.find('div', class_='article__content')

        if not article_section:
            print("No CNN article body found.")
            return ""

        paragraphs = article_section.find_all('div', class_='paragraph') or article_section.find_all('p')

        full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        return full_text.strip()

    except Exception as e:
        print(f"Error fetching CNN article: {e}")
        return ""

def save_entry(entry):
    # Save the entry as a JSON file
    title_slug = slugify(entry.title)
    date_str = format_date(entry)
    filename = f"feed_{date_str}_{title_slug}.json"
    filepath = os.path.join('./data/raw/cnn/', filename)
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

