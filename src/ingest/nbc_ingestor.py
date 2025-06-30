from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class NBCIngestor(BaseIngestor):
    RSS_URL = "http://feeds.nbcnews.com/feeds/worldnews"

    def fetch_full_text(self, article_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(article_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # NBC usually puts article content in divs with the class 'article-body__content'
            content_div = soup.find('div', class_='article-body__content')

            if not content_div:
                # Fallback: some older articles use this container
                content_div = soup.find('div', {'data-testid': 'article-body'})

            if not content_div:
                return ""

            paragraphs = content_div.find_all('p')
            full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
            return full_text.strip()

        except Exception as e:
            print(f"Error fetching NBC article: {article_url} — {e}")
            return ""