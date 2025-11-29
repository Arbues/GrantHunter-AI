import os
import asyncio
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from .search_tool import SearchTool
from .scraper_tool import ScraperTool

class DiscoveryAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.search_tool = SearchTool()
        self.scraper_tool = ScraperTool()

    async def run(self, user_interests: List[str], user_query: str) -> List[dict]:
        """
        Orchestrates the discovery process:
        1. Generate search queries based on interests and user input.
        2. Execute search.
        3. Scrape results (HTML only).
        """
        # 1. Generate Queries
        queries = await self._generate_queries(user_interests, user_query)
        print(f"Generated Queries: {queries}")
        
        # 2. Execute Search (Parallel)
        all_urls = set()
        for q in queries:
            urls = self.search_tool.search(q, count=3) # Keep count low for MVP
            all_urls.update(urls)
        
        unique_urls = list(all_urls)[:5] # Limit to 5 for MVP speed
        print(f"Found URLs: {unique_urls}")
        
        # 3. Scrape Content (Parallel)
        results = []
        tasks = [self.scraper_tool.scrape_url(url) for url in unique_urls]
        scraped_contents = await asyncio.gather(*tasks)
        
        for url, content in zip(unique_urls, scraped_contents):
            if content:
                results.append({
                    "url": url,
                    "content": content[:10000] # Truncate for token limits if needed
                })
                
        return results

    async def _generate_queries(self, interests: List[str], user_query: str) -> List[str]:
        parser = CommaSeparatedListOutputParser()
        prompt = PromptTemplate(
            template="""
            You are a Grant Search Expert.
            User Interests: {interests}
            User Request: {user_query}
            
            Generate 3 distinct, high-quality search queries to find relevant grants, scholarships, or funding opportunities.
            Focus on official sources, universities, and research organizations.
            Return ONLY a comma-separated list of queries.
            """,
            input_variables=["interests", "user_query"]
        )
        chain = prompt | self.llm | parser
        return chain.invoke({"interests": ", ".join(interests), "user_query": user_query})
