from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class NYTIngestor(BaseIngestor):
    RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"

    def fetch_full_text(self, article_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(article_url, headers=headers, timeout=10)
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