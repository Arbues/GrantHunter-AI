import os
import requests
import asyncio
from typing import List, Dict

class SearchTool:
    def __init__(self):
        self.api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    async def search(self, query: str, count: int = 5) -> List[str]:
        """
        Executes a search query and returns a list of URLs.
        Includes a 1.5s sleep to respect Brave API's free tier rate limits (1 QPS).
        """
        if not self.api_key:
            print("Warning: BRAVE_SEARCH_API_KEY not found.")
            return []

        # Rate limiting: 1.5s sleep to be safe with 1 QPS limit
        await asyncio.sleep(1.5)

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": query,
            "count": count
        }

        try:
            # We use requests for now, but we run it in a thread to not block event loop
            # or just call it directly since it's a single call after sleep.
            # For better async, we could use httpx, but let's stick to minimal changes.
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.get(self.base_url, headers=headers, params=params)
            )
            response.raise_for_status()
            data = response.json()
            
            urls = []
            if "web" in data and "results" in data["web"]:
                for result in data["web"]["results"]:
                    urls.append(result["url"])
            
            return urls
        except Exception as e:
            print(f"Error during search: {e}")
            return []
