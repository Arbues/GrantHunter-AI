import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class ScraperTool:
    def __init__(self):
        # Connect to the Docker container's CDP endpoint
        self.cdp_url = os.getenv("PLAYWRIGHT_CDP_URL", "ws://localhost:3000")

    async def scrape_url(self, url: str) -> str:
        """
        Scrapes the content of a URL using Playwright in the Docker container.
        Returns cleaned text content.
        """
        async with async_playwright() as p:
            try:
                # Connect to the remote browser
                browser = await p.chromium.connect_over_cdp(self.cdp_url)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Navigate with timeout
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                
                # Get HTML content
                content = await page.content()
                
                # Clean with BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")
                
                # Remove scripts and styles
                for script in soup(["script", "style"]):
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
                return ""
