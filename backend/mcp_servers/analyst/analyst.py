import os
import re
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from backend.mcp_servers.identity.models import FixedIdentityData
from backend.utils.content_utils import extract_relevant_content, log_token_usage


class MatchResult(BaseModel):
    match_score: int = Field(description="Compatibility score from 0 to 100")
    reasoning: str = Field(description="Brief explanation of the score")
    missing_requirements: List[str] = Field(description="List of specific requirements the user lacks")
    is_viable: bool = Field(description="True if the score is above a threshold (e.g., 60)")


class AnalystAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.6,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=MatchResult)
        self._call_count = 0

    async def analyze(self, profile: FixedIdentityData, opportunity_content: str) -> MatchResult:
        self._call_count += 1
        call_label = f"Analyst #{self._call_count}"

        prompt = PromptTemplate(
            template="""
            You are a Grant Analyst. Compare the Candidate Profile with the Opportunity.

            CANDIDATE PROFILE:
            {profile_json}

            OPPORTUNITY CONTENT:
            {opportunity_content}

            Task:
            1. Evaluate compatibility (0-100%).
            2. Identify HARD requirements (Citizenship, Degree, etc.) and check if the user meets them.
            3. Identify SOFT requirements (Research topic, skills).
            4. List any MISSING requirements.

            {format_instructions}
            """,
            input_variables=["profile_json", "opportunity_content"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm

        try:
            profile_json = profile.json()
            relevant_content = extract_relevant_content(opportunity_content, max_chars=4000)
            raw_response = await chain.ainvoke({
                "profile_json": profile_json,
                "opportunity_content": relevant_content
            })
            log_token_usage(call_label, raw_response)
            text_content = raw_response.content
            text_content = re.sub(r'<think>.*?</think>', '', text_content, flags=re.DOTALL).strip()
            return self.parser.parse(text_content)
        except Exception as e:
            print(f"Error analyzing opportunity: {e}")
            return MatchResult(
                match_score=0,
                reasoning="Error during analysis",
                missing_requirements=[],
                is_viable=False
            )
