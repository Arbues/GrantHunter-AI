import os
from typing import List
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .models import IdentityOutput, FixedIdentityData, NarrativeChunk

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

parser = PydanticOutputParser(pydantic_object=IdentityOutput)

PROMPT_TEMPLATE = """
You are an expert Profile Analyzer for a Grant Funding AI.
Your task is to analyze the following raw user profile (Markdown/Text) and extract a Hybrid Data Structure.

1. **Fixed Data**: Extract objective facts (Name, Nationality, Degree, Skills, Interests).
   - "Interests" are crucial: infer them from the user's projects if not explicitly stated.
2. **Narrative Chunks**: Break down the profile into meaningful semantic chunks (e.g., specific projects, work experiences, thesis).
   - Each chunk should have a clear 'topic' and the full 'content'.
   - Do not summarize too much; keep the original detail for drafting purposes.

Raw Profile:
{profile_text}

{format_instructions}
"""

prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["profile_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

def parse_profile_file(file_path: str) -> IdentityOutput:
    """Reads a local file and parses it into IdentityOutput."""
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Profile file not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"profile_text": raw_text})
        
        # Assign IDs to chunks if missing (though Pydantic might expect them, we can post-process)
        # The LLM is asked to generate them, but we can ensure uniqueness here if needed.
        for chunk in result.chunks:
            if not chunk.id:
                chunk.id = str(uuid.uuid4())
                
        return result
    except Exception as e:
        print(f"Error parsing profile: {e}")
        raise e
