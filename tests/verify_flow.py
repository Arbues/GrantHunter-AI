import asyncio
import os
import sys
import json
import pathlib

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv(override=True)

from backend.orchestrator.graph import app, resolve_session_id
from backend.mcp_servers.identity.models import FixedIdentityData

async def test_flow():
    print("Testing End-to-End Flow...")

    # In test runs APP_ENV is not set, so session_id = "dev" (fixed, safe to overwrite)
    session_id = resolve_session_id()
    print(f"Session ID: {session_id}")

    # Create a dummy profile file
    profile_path = "tests/dummy_profile.md"
    with open(profile_path, "w") as f:
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
        "session_id": session_id,
        "run_metadata": {},
        "profile_file_path": profile_path,
        "user_query": "Find grants for AI climate research",
    }

    print("Invoking Workflow...")
    try:
        result = await app.ainvoke(initial_state)

        print("✅ Workflow Finished.")

        # --- Identity Check (strict) ---
        profile = result.get("profile_data")
        if (
            profile
            and profile.full_name
            and profile.hard_skills
            and profile.interests
        ):
            print(f"✅ Identity Passed. Name={profile.full_name}, Skills={profile.hard_skills[:3]}")
        else:
            print(f"❌ Identity Failed. Profile parsed incorrectly: {profile}")
            sys.exit(1)

        # --- Discovery Check ---
        opps = result.get("opportunities")
        if isinstance(opps, list) and len(opps) > 0:
            print(f"✅ Discovery Passed. Found {len(opps)} opportunities.")
        else:
            print(f"❌ Discovery Failed. Opportunities: {opps}")
            sys.exit(1)

        # --- Analyst Check (strict: no silent errors) ---
        matches = result.get("matches")
        if not isinstance(matches, list) or len(matches) == 0:
            print("❌ Analyst Failed. No matches returned.")
            sys.exit(1)

        error_matches = [m for m in matches if m.reasoning == "Error during analysis"]
        successful_matches = len(matches) - len(error_matches)

        if len(error_matches) == len(matches):
            print(f"❌ Analyst FAILED. ALL {len(matches)} analyses errored (rate limit or model failure).")
            sys.exit(1)
        elif error_matches:
            print(f"⚠️  Analyst PARTIAL. {successful_matches}/{len(matches)} succeeded, {len(error_matches)} errored.")
        else:
            print(f"✅ Analyst Passed. {successful_matches}/{len(matches)} successful analyses.")

        # Print match scores for visibility
        for i, m in enumerate(matches):
            status = "✅" if m.reasoning != "Error during analysis" else "❌"
            print(f"  {status} Match #{i+1}: score={m.match_score}, viable={m.is_viable}")

        # --- Output File Check ---
        output_dir = pathlib.Path("output") / session_id
        json_path = output_dir / "results.json"
        report_path = output_dir / "REPORT.md"
        log_path = output_dir / "run.log"

        output_ok = True

        if json_path.exists():
            data = json.loads(json_path.read_text())
            if data.get("session_id") == session_id and "results" in data:
                print(f"✅ Output JSON Passed. {len(data['results'])} results in {json_path}")
            else:
                print(f"❌ Output JSON Failed. Unexpected content: {list(data.keys())}")
                output_ok = False
        else:
            print(f"❌ Output JSON Failed. File not found: {json_path}")
            output_ok = False

        if report_path.exists() and report_path.stat().st_size > 0:
            print(f"✅ Output REPORT.md Passed. Size={report_path.stat().st_size} bytes.")
        else:
            print(f"❌ Output REPORT.md Failed. File missing or empty: {report_path}")
            output_ok = False

        if log_path.exists() and log_path.stat().st_size > 0:
            print(f"✅ Output run.log Passed. Size={log_path.stat().st_size} bytes.")
        else:
            print(f"⚠️  Output run.log not found or empty at {log_path}.")
            # Non-fatal: log is helpful but not blocking

        if not output_ok:
            sys.exit(1)

    except Exception as e:
        print(f"❌ Workflow Failed with Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_flow())
