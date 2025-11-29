import asyncio
import os
import sys

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.orchestrator.graph import app
from backend.mcp_servers.identity.models import FixedIdentityData

async def test_flow():
    print("Testing End-to-End Flow...")
    
    # Create a dummy profile file
    with open("tests/dummy_profile.md", "w") as f:
        f.write("""
        # John Doe
        **Nationality:** American
        **Degree:** PhD in Computer Science
        **Skills:** Python, AI, Grant Writing
        **Interests:** Artificial Intelligence, Climate Change
        
        ## Projects
        I developed an AI model to predict climate patterns using satellite data.
        """)
        
    initial_state = {
        "profile_file_path": "tests/dummy_profile.md",
        "user_query": "Find grants for AI climate research"
    }
    
    print("Invoking Workflow...")
    try:
        result = await app.ainvoke(initial_state)
        
        print("✅ Workflow Finished.")
        
        # Check Identity
        profile = result.get("profile_data")
        if profile and profile.full_name == "John Doe":
            print("✅ Identity Step Passed.")
        else:
            print(f"❌ Identity Step Failed. Profile: {profile}")
            
        # Check Discovery
        opps = result.get("opportunities")
        if isinstance(opps, list):
            print(f"✅ Discovery Step Passed. Found {len(opps)} opportunities.")
        else:
            print("❌ Discovery Step Failed.")
            
        # Check Analyst
        matches = result.get("matches")
        if isinstance(matches, list):
            print(f"✅ Analyst Step Passed. Analyzed {len(matches)} matches.")
        else:
            print("❌ Analyst Step Failed.")
            
    except Exception as e:
        print(f"❌ Workflow Failed with Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_flow())
