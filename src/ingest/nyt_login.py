from playwright.sync_api import sync_playwright

def login_and_save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False so you can log in manually
        context = browser.new_context()
        page = context.new_page()

        # Go to NYT login page
        page.goto("https://myaccount.nytimes.com/auth/login")

        print("⚠️ Please log in manually in the browser window...")

        # Wait for manual login
        page.wait_for_url("https://www.nytimes.com/", timeout=300_000)  # Wait up to 5 minutes

        # Save session state after login
        context.storage_state(path="nyt_auth.json")
        print("✅ Login successful. Session saved to nyt_auth.json.")

        browser.close()

if __name__ == '__main__':
    login_and_save_session()