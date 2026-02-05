import asyncio
import os
import sys

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from backend.mcp_servers.discovery.search_tool import SearchTool

async def test_search():
    print("Testing Search Tool...")
    searcher = SearchTool()
    
    query = "grants for AI research 2024"
    print(f"Searching for: '{query}'...")
    
    urls = await searcher.search(query)
    
    if urls:
        print(f"✅ PASSED: Found {len(urls)} URLs.")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
    else:
        print("❌ FAILED: No URLs found or error occurred.")

if __name__ == "__main__":
    # Search tool is sync in implementation, but we run in async script for consistency
    asyncio.run(test_search())
