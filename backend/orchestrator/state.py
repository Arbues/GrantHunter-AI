from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk
from backend.mcp_servers.analyst.analyst import MatchResult

class Opportunity(TypedDict):
    url: str
    content: str

class AgentState(TypedDict):
    # Input
    profile_file_path: str
    user_query: str
    
    # Identity
    profile_data: Optional[FixedIdentityData]
    narrative_chunks: List[NarrativeChunk]
    
    # Discovery
    opportunities: List[Opportunity]
    
    # Analyst
    matches: List[MatchResult]
    
    # Executor (Optional, if we want to store drafts here)
    drafts: Dict[str, str] # url -> draft content
