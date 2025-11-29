import os
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from backend.mcp_servers.identity.models import FixedIdentityData

class MatchResult(BaseModel):
    match_score: int = Field(description="Compatibility score from 0 to 100")
    reasoning: str = Field(description="Brief explanation of the score")
    missing_requirements: List[str] = Field(description="List of specific requirements the user lacks")
    is_viable: bool = Field(description="True if the score is above a threshold (e.g., 60)")

class AnalystAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.parser = PydanticOutputParser(pydantic_object=MatchResult)

    async def analyze(self, profile: FixedIdentityData, opportunity_content: str) -> MatchResult:
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
        
        chain = prompt | self.llm | self.parser
        
        try:
            # Convert Pydantic model to JSON string for the prompt
            profile_json = profile.json()
            return chain.invoke({"profile_json": profile_json, "opportunity_content": opportunity_content[:15000]})
        except Exception as e:
            print(f"Error analyzing opportunity: {e}")
            return MatchResult(match_score=0, reasoning="Error during analysis", missing_requirements=[], is_viable=False)
