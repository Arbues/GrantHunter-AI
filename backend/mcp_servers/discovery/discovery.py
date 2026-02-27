import os
import re
import asyncio
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from .search_tool import SearchTool
from .scraper_tool import ScraperTool
from backend.utils.content_utils import log_token_usage

class DiscoveryAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.6,
            groq_api_key=os.getenv("GROQ_API_KEY")
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
        
        # 2. Execute Search (Async)
        all_urls = set()
        for q in queries:
            urls = await self.search_tool.search(q, count=3) # Keep count low for MVP
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
            Do NOT include any introduction, thinking process, or multiple lines.
            """,
            input_variables=["interests", "user_query"]
        )
        chain = prompt | self.llm
        
        raw_response = await chain.ainvoke({"interests": ", ".join(interests), "user_query": user_query})
        log_token_usage("Discovery", raw_response)
        text_content = raw_response.content
        text_content = re.sub(r'<think>.*?</think>', '', text_content, flags=re.DOTALL).strip()
        return parser.parse(text_content)
