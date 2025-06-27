from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class NPRIngestor(BaseIngestor):
    RSS_URL = "https://feeds.npr.org/1004/rss.xml"

    def fetch_full_text(self, article_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(article_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # NPR article body is typically in <div class="storytext"> or <article> blocks
            article_body = soup.find('div', class_='storytext') or soup.find('article')

            if not article_body:
                print("No main article content found.")
                return ""

            paragraphs = article_body.find_all('p')
            full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

            return full_text.strip()

        except Exception as e:
            print(f"Error fetching NPR article: {e}")
            return ""
