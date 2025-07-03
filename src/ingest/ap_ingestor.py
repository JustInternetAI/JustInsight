import re
import requests
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from ingest.base_ingestor import BaseIngestor

class APIngestor(BaseIngestor):
    RSS_URL = "https://news.google.com/rss/search?q=when:24h+allinurl:apnews.com&hl=en-US&gl=US&ceid=US:en"

    def resolve_google_news_redirect(self, url):
        resp = requests.get(url)
        data = BeautifulSoup(resp.text, 'html.parser').select_one('c-wiz[data-p]').get('data-p')
        obj = json.loads(data.replace('%.@.', '["garturlreq",'))

        payload = {
            'f.req': json.dumps([[['Fbv4je', json.dumps(obj[:-6] + obj[-2:]), 'null', 'generic']]])
        }

        headers = {
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        }

        url = "https://news.google.com/_/DotsSplashUi/data/batchexecute"
        response = requests.post(url, headers=headers, data=payload)
        array_string = json.loads(response.text.replace(")]}'", ""))[0][2]
        return json.loads(array_string)[1]


    def fetch_full_text(self, article_url):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                #change the article_url to the redirected one (or just the same)
                article_url = self.resolve_google_news_redirect(article_url)
                #print(article_url)
                page.goto(article_url, wait_until="domcontentloaded", timeout=15000)

                # Wait for the main article body to load
                page.wait_for_selector('div.RichTextStoryBody', timeout=3000)

                # Extract the text content from the paragraphs inside the body
                content = page.query_selector_all('div.RichTextStoryBody p')
                full_text = "\n".join(p.inner_text() for p in content)

                browser.close()
                return full_text.strip()

        except Exception as e:
            #print(f"Playwright error fetching {article_url}: {e}")
            return ""
    
