from typing import List, Optional, Dict, Any
from typing_extensions import TypedDict
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk
from backend.mcp_servers.analyst.analyst import MatchResult

class Opportunity(TypedDict):
    url: str
    content: str

class AgentState(TypedDict):
    # Session
    session_id: str          # "dev" in dev/test, UUID4 in production
    run_metadata: Dict[str, Any]  # timestamps, token counts, etc.

    # Input
    profile_file_path: str
    user_query: str
    
    # Identity
    profile_data: Optional[FixedIdentityData]
    narrative_chunks: List[NarrativeChunk]
    
    # Discovery
    queries: List[str]
    opportunities: List[Opportunity]
    
    # Analyst
    matches: List[MatchResult]
    
    # Executor (Optional, if we want to store drafts here)
    drafts: Dict[str, str] # url -> draft content
