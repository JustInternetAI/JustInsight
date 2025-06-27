from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class CNNIngestor(BaseIngestor):
    RSS_URL = "http://rss.cnn.com/rss/cnn_world.rss"
        
    def fetch_full_text(self, url):
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