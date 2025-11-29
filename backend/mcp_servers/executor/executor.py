import os
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk

class ExecutorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    async def draft(self, profile: FixedIdentityData, chunks: List[NarrativeChunk], opportunity_content: str, instructions: str = "Draft a cover letter") -> str:
        """
        Generates a draft application.
        """
        # Format chunks into a readable string
        context_str = "\n\n".join([f"Topic: {c.topic}\nContent: {c.content}" for c in chunks])
        
        prompt = PromptTemplate(
            template="""
            You are a Professional Grant Writer.
            
            CANDIDATE INFO:
            Name: {name}
            Degree: {degree}
            Skills: {skills}
            
            RELEVANT EXPERIENCE (Context):
            {context_str}
            
            OPPORTUNITY DETAILS:
            {opportunity_content}
            
            TASK:
            {instructions}
            
            Write a compelling, professional draft tailored to the opportunity. 
            Use the candidate's specific experience to prove they fit the requirements.
            Do not invent facts. Use placeholders [Like This] if information is missing.
            """,
            input_variables=["name", "degree", "skills", "context_str", "opportunity_content", "instructions"]
        )
        
        chain = prompt | self.llm
        
        response = chain.invoke({
            "name": profile.full_name,
            "degree": profile.highest_degree,
            "skills": ", ".join(profile.hard_skills),
            "context_str": context_str,
            "opportunity_content": opportunity_content[:15000],
            "instructions": instructions
        })
        
        return response.content
