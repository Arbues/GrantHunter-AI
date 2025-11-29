import asyncio
import os
import sys

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.mcp_servers.discovery.scraper_tool import ScraperTool

async def test_scraper():
    print("Testing Scraper Tool...")
    scraper = ScraperTool()
    
    # Test with a known URL (e.g., Example.com or a simple dynamic site)
    url = "https://example.com"
    print(f"Scraping {url}...")
    
    content = await scraper.scrape_url(url)
    
    if "Example Domain" in content:
        print("✅ Scraper Test Passed: Content retrieved successfully.")
        print(f"Content Preview: {content[:100]}...")
    else:
        print("❌ Scraper Test Failed: Content mismatch or empty.")
        print(f"Content: {content}")

if __name__ == "__main__":
    asyncio.run(test_scraper())
