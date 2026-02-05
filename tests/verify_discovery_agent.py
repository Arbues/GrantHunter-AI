import asyncio
import os
import sys
from dotenv import load_dotenv

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load env vars
load_dotenv(override=True)

from backend.mcp_servers.discovery.discovery import DiscoveryAgent

async def test_discovery_agent():
    print("Testing Discovery Agent (Groq + Search + Scraper)...")
    
    # Check for API Key
    if not os.getenv("GROQ_API_KEY"):
        print("❌ SKIPPING: GROQ_API_KEY not found in environment.")
        return

    agent = DiscoveryAgent()
    
    interests = ["Artificial Intelligence", "Climate Change"]
    user_query = "Find research grants for AI applications in climate science"
    
    print(f"\nUser Interests: {interests}")
    print(f"User Query: {user_query}")
    print("\n--- Running Agent ---")
    
    try:
        results = await agent.run(user_interests=interests, user_query=user_query)
        
        if results:
            print(f"\n✅ PASSED: Discovery Agent found {len(results)} results.")
            for i, res in enumerate(results, 1):
                url = res.get('url', 'No URL')
                content_len = len(res.get('content', ''))
                print(f"  {i}. {url} (Content: {content_len} chars)")
        else:
            print("\n⚠️ WARNING: Agent finished but returned no results.")
            
    except Exception as e:
        print(f"\n❌ FAILED: Agent encountered an error: {e}")

if __name__ == "__main__":
    asyncio.run(test_discovery_agent())
