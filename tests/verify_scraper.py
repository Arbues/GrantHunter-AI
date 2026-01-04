import asyncio
import os
import sys

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.mcp_servers.discovery.scraper_tool import ScraperTool

async def test_scraper():
    print("Testing Scraper Tool...")
    scraper = ScraperTool()
    
    test_cases = [
        {
            "name": "Simple Static Site",
            "url": "https://example.com",
            "expected_keyword": "Example Domain"
        },
        {
            "name": "Complex/Dynamic Site",
            "url": "https://www.ycombinator.com/",
            "expected_keyword": "Y Combinator"
        }
    ]
    
    for case in test_cases:
        print(f"\n--- Testing Case: {case['name']} ---")
        print(f"Scraping {case['url']}...")
        
        content = await scraper.scrape_url(case['url'])
        
        if case['expected_keyword'].lower() in content.lower():
            print(f"✅ PASSED: '{case['expected_keyword']}' found in content.")
            print(f"Content Length: {len(content)} characters")
            print(f"Preview: {content[:150].replace('\n', ' ')}...")
        else:
            print(f"❌ FAILED: '{case['expected_keyword']}' NOT found.")
            print(f"Content length retrieved: {len(content)}")
            if content:
                print(f"Content Preview: {content[:200]}")
            else:
                print("Content is empty.")

if __name__ == "__main__":
    asyncio.run(test_scraper())
