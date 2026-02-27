import asyncio
import os
import uuid
import datetime
from langgraph.graph import StateGraph, END
from .state import AgentState
from backend.mcp_servers.identity.parser import parse_profile_file
from backend.mcp_servers.discovery.discovery import DiscoveryAgent
from backend.mcp_servers.analyst.analyst import AnalystAgent
from backend.utils.output_utils import save_results_json, generate_report_md
from backend.utils.logger import get_logger

# Initialize Agents
discovery_agent = DiscoveryAgent()
analyst_agent = AnalystAgent()


def resolve_session_id(given_id: str | None = None) -> str:
    """
    Determines the session ID based on environment:
      - If given_id is explicitly provided (e.g. by FastAPI/Streamlit), use it.
      - If APP_ENV=production, generate a unique UUID4 per run.
      - Otherwise (dev/test), return 'dev' so runs overwrite the same output folder.
    """
    if given_id:
        return given_id
    if os.getenv("APP_ENV") == "production":
        return str(uuid.uuid4())
    return "dev"


async def identity_node(state: AgentState):
    session_id = state.get("session_id", "dev")
    logger = get_logger("Identity", session_id)
    logger.info("--- IDENTITY NODE ---")

    file_path = state["profile_file_path"]
    try:
        identity_output = await parse_profile_file(file_path)
        logger.info(f"Profile parsed. Name={identity_output.fixed_data.full_name}")
        return {
            "profile_data": identity_output.fixed_data,
            "narrative_chunks": identity_output.chunks,
        }
    except Exception as e:
        logger.error(f"Identity Error: {e}")
        return {"profile_data": None}


async def discovery_node(state: AgentState):
    session_id = state.get("session_id", "dev")
    logger = get_logger("Discovery", session_id)
    logger.info("--- DISCOVERY NODE ---")

    profile = state.get("profile_data")
    if not profile:
        logger.warning("No profile data. Skipping discovery.")
        return {"opportunities": []}

    interests = profile.interests
    user_query = state["user_query"]

    # Run Discovery Agent
    results, queries = await discovery_agent.run(interests, user_query)
    logger.info(f"Found {len(results)} opportunities.")
    return {"opportunities": results, "queries": queries}


# Limit concurrency for Analyst calls to avoid 429 errors
analyst_semaphore = asyncio.Semaphore(1)


async def analyst_node(state: AgentState):
    session_id = state.get("session_id", "dev")
    logger = get_logger("Analyst", session_id)
    logger.info("--- ANALYST NODE ---")

    profile = state.get("profile_data")
    opportunities = state.get("opportunities", [])

    if not profile or not opportunities:
        logger.warning("Missing profile or opportunities. Skipping analysis.")
        return {"matches": []}

    async def limited_analyze(profile, content):
        async with analyst_semaphore:
            await asyncio.sleep(2.0)
            return await analyst_agent.analyze(profile, content)

    tasks = [limited_analyze(profile, opp["content"]) for opp in opportunities]
    results = await asyncio.gather(*tasks)

    successful = sum(1 for m in results if m.reasoning != "Error during analysis")
    logger.info(f"Analysis complete: {successful}/{len(results)} successful.")
    return {"matches": results}


async def output_node(state: AgentState):
    """
    Final node: persists results to disk.
    Writes output/<session_id>/results.json, REPORT.md, and run.log.
    """
    session_id = state.get("session_id", "dev")
    logger = get_logger("Output", session_id)
    logger.info("--- OUTPUT NODE ---")

    # Enrich run_metadata with end timestamp
    run_metadata = state.get("run_metadata", {})
    run_metadata["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    updated_state = {**state, "run_metadata": run_metadata}

    json_path = save_results_json(updated_state)
    report_path = generate_report_md(updated_state)

    logger.info(f"Results saved to {json_path}")
    logger.info(f"Report saved to {report_path}")

    return {"run_metadata": run_metadata}


# Define Graph
workflow = StateGraph(AgentState)

workflow.add_node("identity", identity_node)
workflow.add_node("discovery", discovery_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("output", output_node)

workflow.set_entry_point("identity")
workflow.add_edge("identity", "discovery")
workflow.add_edge("discovery", "analyst")
workflow.add_edge("analyst", "output")
workflow.add_edge("output", END)

app = workflow.compile()
