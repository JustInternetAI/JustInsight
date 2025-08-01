from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class USNEWSIngestor(BaseIngestor):
    RSS_URL = "https://www.usnews.com/rss/news"

    def fetch_full_text(self, article_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(article_url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Look for main article content container
            content_div = soup.find('div', class_='Article-body')
            if not content_div:
                # Fallback for other layouts
                content_div = soup.find('div', class_='MuiContainer-root')

            if not content_div:
                return ""

            paragraphs = content_div.find_all('p')
            full_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            return full_text.strip()

        except Exception as e:
            print(f"Error fetching U.S. News article: {e}")
            return ""