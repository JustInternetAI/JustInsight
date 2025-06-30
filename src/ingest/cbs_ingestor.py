from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class CBSIngestor(BaseIngestor):
    RSS_URL = "https://www.cbsnews.com/latest/rss/world"

    def fetch_full_text(self, article_url):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(article_url, headers=headers, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, 'html.parser')

            # Step 1: find the <h1> (article title)
            h1 = soup.find('h1')
            if not h1:
                print(f"[warn] No <h1> tag found in {article_url}")
                return ""

            # Step 2: Walk up parent nodes until we find one with enough <p> tags
            root = h1
            while root and root.name != 'body':
                paragraphs = root.find_all('p')
                if len(paragraphs) >= 5:
                    break
                root = root.parent

            if root is None or root.name == 'body':
                print(f"[warn] Couldn't find content container in {article_url}")
                return ""

            # Step 3: Extract text from heading/paragraph tags under that container
            tags = root.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p'])
            text = "\n".join(tag.get_text(strip=True) for tag in tags)

            return text.strip()

        except Exception as e:
            print(f"[error] {e} while scraping {article_url}")
            return ""