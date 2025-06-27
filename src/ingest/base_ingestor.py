import datetime
import feedparser
import hashlib
import re
from ingest.save_to_database import save_entry

class BaseIngestor:
    RSS_URL = None #will be set by the subclasses 

    def slugify(self, text):
        # Convert title to a filesystem-friendly slug
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        return text.strip('-')

    def format_date(self, entry):
        # Extract and format the published date
        try:
            dt = datetime.datetime(*entry.published_parsed[:6])
            return dt.strftime("%Y-%m-%d")
        except:
            return "unknown-date"
    
    def fetch_full_text(self, url):
        raise NotImplementedError(
            "Subclass must implement fetch_full_text()"
        )

    def generate_entry_hash(self, entry):
        hash_input = f"{entry.title}{entry.link}{entry.get('published', '')}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

    def format_entry(self, entry):
        title_slug = self.slugify(entry.title)
        date_str = self.format_date(entry)
        full_text = self.fetch_full_text(entry.link)

        data = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", ""),
            "summary": entry.get("summary", ""),
            "full_text": full_text,
            "id": self.generate_entry_hash(entry)
        }
        return data

    def check_and_save_new_entries(self):
        feed = feedparser.parse(self.RSS_URL)

        for entry in feed.entries:
            save_entry(self.format_entry(entry))
