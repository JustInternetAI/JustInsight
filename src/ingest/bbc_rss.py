import feedparser

feed = feedparser.parse('bbc_world.xml')

for entry in feed.entries:
    print("Title:", entry.title)
    print("Link:", entry.link)
    print("Published:", entry.published)
    print("Raw XML:\n", entry)
    print("-" * 80)
