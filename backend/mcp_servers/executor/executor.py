import os
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk
from backend.utils.content_utils import log_token_usage
import re

# el agente executor es el que se encarga de generar el texto final de la beca 
class ExecutorAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
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
            Eres un Redactor Profesional de Becas. 
            Tu tarea es escribir un borrador de postulación (carta de motivación o similar) basado en la información del candidato.
            
            REGLA CRÍTICA: Escribe TODO el borrador en ESPAÑOL.
            
            DATOS DEL CANDIDATO:
            Nombre: {name}
            Grado: {degree}
            Habilidades: {skills}
            
            EXPERIENCIA RELEVANTE (Contexto):
            {context_str}
            
            DETALLES DE LA OPORTUNIDAD:
            {opportunity_content}
            
            INSTRUCCIONES DE TAREA:
            {instructions}
            
            Escribe un borrador persuasivo, profesional y personalizado. 
            Usa la experiencia específica del candidato para demostrar que encaja con los requisitos.
            No inventes hechos. Usa marcadores de posición [Como Este] si falta información específica.
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
            log_token_usage("Executor", raw_response)
            text_content = raw_response.content
            text_content = re.sub(r'<think>.*?</think>', '', text_content, flags=re.DOTALL).strip()
            return text_content
            
        except Exception as e:
            print(f"Error drafting application: {e}")
            return f"Error generation draft: {e}"
