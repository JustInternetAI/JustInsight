from playwright.sync_api import sync_playwright
from ingest.base_ingestor import BaseIngestor

class APIngestor(BaseIngestor):
    RSS_URL = "https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en"

    def fetch_full_text(self, article_url):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(article_url, timeout=15000)

                # Wait for the main article body to load
                page.wait_for_selector('div.RichTextStoryBody', timeout=5000)

                # Extract the text content from the paragraphs inside the body
                content = page.query_selector_all('div.RichTextStoryBody p')
                full_text = "\n".join(p.inner_text() for p in content)

                browser.close()
                return full_text.strip()

        except Exception as e:
            print(f"Playwright error fetching {article_url}: {e}")
            return ""
    
