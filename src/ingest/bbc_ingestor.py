from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class BBCIngestor(BaseIngestor):
    RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"

    def fetch_full_text(self, article_url):
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        article = soup.find('article')
        
        if not article:
            return None

        # # Remove unwanted sections like "related content", "media", or "byline"
        # for unwanted in article.select('[data-component="byline"], [data-component="media-block"], .bbc-1msyfg1, .bbc-1fxtbkn'):  # classes may vary
        #     unwanted.decompose()

        # Gather all paragraphs that are part of the article body
        paragraphs = article.find_all('p')

        cleaned_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
        return cleaned_text