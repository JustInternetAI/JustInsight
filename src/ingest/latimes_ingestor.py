from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class LATIMESIngestor(BaseIngestor):
    RSS_URL = "https://www.latimes.com/world/rss2.0.xml"

    def fetch_full_text(self, article_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(article_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # LATimes articles are usually under <section name="article-body"> or similar
            article_body = soup.find('section', attrs={'name': 'article-body'})
            if not article_body:
                article_body = soup.find('div', class_='rich-text-article-body')  # fallback

            if not article_body:
                return ""

            paragraphs = article_body.find_all('p')
            full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            return full_text.strip()

        except Exception as e:
            print(f"Error fetching LA Times article: {article_url} — {e}")
            return ""