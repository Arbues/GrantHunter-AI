import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class ScraperTool:
    def __init__(self):
        # Connect to the Docker container's CDP endpoint
        self.cdp_url = os.getenv("PLAYWRIGHT_CDP_URL", "ws://localhost:3000")

    async def scrape_url(self, url: str) -> str:
        """
        Scrapes the content of a URL using Playwright.
        Tries to connect via CDP (Docker), falls back to local browser if it fails.
        Returns cleaned text content.
        """
        async with async_playwright() as p:
            browser = None
            try:
                print(f"Attempting to connect to Playwright via WS: {self.cdp_url}")
                try:
                    # Try connecting to remote browser (Docker) - Use connect() for Playwright Server
                    browser = await p.chromium.connect(self.cdp_url, timeout=5000)
                    print("Connected to remote Playwright via WS.")
                except Exception as cdp_error:
                    print(f"Remote Connection failed: {cdp_error}. Falling back to local browser...")
                    # Fallback to local browser
                    browser = await p.chromium.launch(headless=True)
                    print("Local browser launched.")

                if not browser:
                    raise Exception("Failed to initialize any browser (remote or local).")

                context = await browser.new_context()
                page = await context.new_page()
                
                # Navigate with timeout
                print(f"Navigating to {url}...")
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                
                # Get HTML content
                content = await page.content()
                
                # Clean with BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")
                
                # Remove scripts and styles
                for script in soup(["script", "style", "nav", "footer"]):
                    script.decompose()
                    
                text = soup.get_text(separator="\n")
                
                # Simple cleanup of extra whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_text = '\n'.join(chunk for chunk in chunks if chunk)
                
                await browser.close()
                return clean_text
                
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                if browser:
                    await browser.close()
                return ""
