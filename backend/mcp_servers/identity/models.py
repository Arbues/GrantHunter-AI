from typing import List, Optional
from pydantic import BaseModel, Field

class FixedIdentityData(BaseModel):
    """Structured data extracted from the user profile."""
    full_name: str = Field(description="Full name of the user")
    nationality: str = Field(description="Nationality or citizenship")
    highest_degree: str = Field(description="Highest academic degree obtained")
    years_experience: int = Field(description="Total years of professional experience")
    hard_skills: List[str] = Field(description="List of technical skills")
    soft_skills: List[str] = Field(description="List of soft skills")
    languages: List[str] = Field(description="List of languages spoken")
    interests: List[str] = Field(description="List of research interests or funding topics (e.g., 'AI', 'Climate Change')")

class NarrativeChunk(BaseModel):
    """A semantic chunk of text from the profile."""
    id: str = Field(description="Unique identifier for the chunk")
    topic: str = Field(description="Main topic of this chunk (e.g., 'Leadership', 'Thesis', 'Project X')")
    content: str = Field(description="The actual text content")
    # embedding: List[float] # Embeddings will be handled separately in the DB/Vector Store

class IdentityOutput(BaseModel):
    """Hybrid output containing both fixed data and narrative chunks."""
    fixed_data: FixedIdentityData
    chunks: List[NarrativeChunk]
