import os
from typing import List
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk
import re

# el agente executor es el que se encarga de generar el texto final de la beca 
class ExecutorAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="qwen/qwen3-32b",
            temperature=0.7,
            groq_api_key=os.getenv("GROQ_API_KEY")
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
        
        try:
            raw_response = await chain.ainvoke({
                "name": profile.full_name,
                "degree": profile.highest_degree,
                "skills": ", ".join(profile.hard_skills),
                "context_str": context_str,
                "opportunity_content": opportunity_content[:15000],
                "instructions": instructions
            })
            
            text_content = raw_response.content
            # Strip <think> tags if present
            text_content = re.sub(r'<think>.*?</think>', '', text_content, flags=re.DOTALL).strip()
            return text_content
            
        except Exception as e:
            print(f"Error drafting application: {e}")
            return f"Error generation draft: {e}"
