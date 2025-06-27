from bs4 import BeautifulSoup
import requests
from ingest.base_ingestor import BaseIngestor

class BBCIngestor(BaseIngestor):
    RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"

    def fetch_full_text(self, article_url):
        response = requests.get(self.RSS_URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        article = soup.find('article')

        if article:
            return(article.get_text())