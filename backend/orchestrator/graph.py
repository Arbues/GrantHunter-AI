import asyncio
from langgraph.graph import StateGraph, END
from .state import AgentState
from backend.mcp_servers.identity.parser import parse_profile_file
from backend.mcp_servers.discovery.discovery import DiscoveryAgent
from backend.mcp_servers.analyst.analyst import AnalystAgent

# Initialize Agents
discovery_agent = DiscoveryAgent()
analyst_agent = AnalystAgent()

async def identity_node(state: AgentState):
    print("--- IDENTITY NODE ---")
    file_path = state["profile_file_path"]
    try:
        identity_output = parse_profile_file(file_path)
        return {
            "profile_data": identity_output.fixed_data,
            "narrative_chunks": identity_output.chunks
        }
    except Exception as e:
        print(f"Identity Error: {e}")
        return {"profile_data": None}

async def discovery_node(state: AgentState):
    print("--- DISCOVERY NODE ---")
    profile = state.get("profile_data")
    if not profile:
        return {"opportunities": []}
    
    interests = profile.interests
    user_query = state["user_query"]
    
    # Run Discovery Agent
    results = await discovery_agent.run(interests, user_query)
    return {"opportunities": results}

async def analyst_node(state: AgentState):
    print("--- ANALYST NODE ---")
    profile = state.get("profile_data")
    opportunities = state.get("opportunities", [])
    
    if not profile or not opportunities:
        return {"matches": []}
    
    matches = []
    # Analyze in parallel
    tasks = [analyst_agent.analyze(profile, opp["content"]) for opp in opportunities]
    results = await asyncio.gather(*tasks)
    
    return {"matches": results}

# Define Graph
workflow = StateGraph(AgentState)

workflow.add_node("identity", identity_node)
workflow.add_node("discovery", discovery_node)
workflow.add_node("analyst", analyst_node)

workflow.set_entry_point("identity")
workflow.add_edge("identity", "discovery")
workflow.add_edge("discovery", "analyst")
workflow.add_edge("analyst", END)

app = workflow.compile()
