import os
import requests
from typing import List, Dict

class SearchTool:
    def __init__(self):
        self.api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    def search(self, query: str, count: int = 5) -> List[str]:
        """
        Executes a search query and returns a list of URLs.
        """
        if not self.api_key:
            print("Warning: BRAVE_SEARCH_API_KEY not found.")
            return []

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
            response = requests.get(self.base_url, headers=headers, params=params)
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
