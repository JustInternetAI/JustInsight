import requests

url = 'http://feeds.bbci.co.uk/news/world/rss.xml'
response = requests.get(url)

if response.status_code == 200:
    with open('bbc_world.xml', 'wb') as f:
        f.write(response.content)
    print("Downloaded the latest BBC World RSS feed successfully.")
else:
    print(f"Failed to download feed. Status code: {response.status_code}")

import feedparser
import json
import os

# Parse the RSS XML file
feed = feedparser.parse('bbc_world.xml')

# Output directory
output_dir = './data/raw/bbc/'

# Create directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for i, entry in enumerate(feed.entries, 1):
    data = {
        "title": entry.title,
        "link": entry.link,
        "published": entry.get("published", ""),
        "raw_xml": entry.get('summary', '')  # summary usually contains raw content
    }
    
    # Save as JSON file
    filename = os.path.join(output_dir, f'entry_{i}.json')
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Saved {len(feed.entries)} entries to {output_dir}")