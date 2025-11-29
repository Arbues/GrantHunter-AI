import streamlit as st
import asyncio
import os
import sys

# Add root to path to allow imports from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.orchestrator.graph import app as workflow_app
from backend.mcp_servers.executor.executor import ExecutorAgent
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk

# Page Config
st.set_page_config(page_title="GrantHunter AI", page_icon="🚀", layout="wide")

# Custom CSS for "Cyber/Technical" look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 4px;
    }
    .stCard {
        background-color: #161b22;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 GrantHunter AI")
st.caption("Your Autonomous Funding Agent")

# Sidebar: Profile Selection
with st.sidebar:
    st.header("Identity Core")
    uploaded_file = st.file_uploader("Upload Profile (MD/TXT)", type=["md", "txt"])
    
    profile_path = None
    if uploaded_file:
        # Save to temp file
        profile_path = f"temp_{uploaded_file.name}"
        with open(profile_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Loaded: {uploaded_file.name}")

# Main Area: Command Center
query = st.text_input("Command Center", placeholder="e.g., Find PhD grants in AI for Peruvian students in Europe")

if st.button("Launch Discovery Agent") and profile_path and query:
    with st.spinner("Agents are working... (Identity -> Discovery -> Analyst)"):
        # Run Workflow
        initial_state = {
            "profile_file_path": profile_path,
            "user_query": query
        }
        
        # Run async workflow in sync streamlit
        try:
            result = asyncio.run(workflow_app.ainvoke(initial_state))
            st.session_state["results"] = result
            st.session_state["profile_data"] = result.get("profile_data")
            st.session_state["narrative_chunks"] = result.get("narrative_chunks")
        except Exception as e:
            st.error(f"Workflow Error: {e}")

# Results Dashboard
if "results" in st.session_state:
    results = st.session_state["results"]
    matches = results.get("matches", [])
    opportunities = results.get("opportunities", [])
    
    st.subheader(f"Found {len(matches)} Opportunities")
    
    for i, match in enumerate(matches):
        opp = opportunities[i]
        
        # Card View
        with st.container():
            st.markdown(f"""
            <div class="stCard">
                <h3>{match.match_score}% Match</h3>
                <p><b>URL:</b> <a href="{opp['url']}" target="_blank">{opp['url']}</a></p>
                <p><b>Reasoning:</b> {match.reasoning}</p>
                <p><b>Missing:</b> {', '.join(match.missing_requirements) if match.missing_requirements else 'None'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Draft Button
            if st.button(f"Draft Application #{i+1}", key=f"draft_{i}"):
                executor = ExecutorAgent()
                with st.spinner("Executor Agent is drafting..."):
                    draft = asyncio.run(executor.draft(
                        profile=st.session_state["profile_data"],
                        chunks=st.session_state["narrative_chunks"],
                        opportunity_content=opp["content"]
                    ))
                    st.session_state[f"draft_content_{i}"] = draft

            # Show Draft if exists
            if f"draft_content_{i}" in st.session_state:
                st.text_area("Draft Application", value=st.session_state[f"draft_content_{i}"], height=300)
