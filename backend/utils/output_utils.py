"""
Output utilities for GrantHunter AI.

Responsible for persisting the final AgentState into structured artifacts:
  - output/<session_id>/results.json  (machine-readable, for frontend)
  - output/<session_id>/REPORT.md     (human-readable, for the user)
"""

import json
import pathlib
import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.orchestrator.state import AgentState


def _get_output_dir(session_id: str) -> pathlib.Path:
    """Returns (and creates if needed) the output directory for this session."""
    output_dir = pathlib.Path("output") / session_id
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_results_json(state: "AgentState") -> pathlib.Path:
    """
    Serializes the final AgentState to a structured JSON file.

    Output: output/<session_id>/results.json
    """
    session_id = state.get("session_id", "dev")
    output_dir = _get_output_dir(session_id)

    profile = state.get("profile_data")
    opportunities = state.get("opportunities", [])
    matches = state.get("matches", [])
    run_metadata = state.get("run_metadata", {})

    # Build the ranked match list (zip opportunities + matches)
    ranked_results = []
    for i, match in enumerate(matches):
        opp = opportunities[i] if i < len(opportunities) else {}
        ranked_results.append({
            "rank": i + 1,
            "url": opp.get("url", ""),
            "match_score": match.match_score,
            "is_viable": match.is_viable,
            "reasoning": match.reasoning,
            "missing_requirements": match.missing_requirements,
        })

    # Sort by score descending for the final report
    ranked_results.sort(key=lambda x: x["match_score"], reverse=True)
    # Re-assign rank after sort
    for i, r in enumerate(ranked_results):
        r["rank"] = i + 1

    payload = {
        "session_id": session_id,
        "metadata": {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "user_query": state.get("user_query", ""),
            "profile_file": state.get("profile_file_path", ""),
            **run_metadata,
        },
        "profile": profile.model_dump() if profile else None,
        "opportunities_found": len(opportunities),
        "results": ranked_results,
    }

    json_path = output_dir / "results.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return json_path


def generate_report_md(state: "AgentState") -> pathlib.Path:
    """
    Generates a human-readable Markdown report from the final AgentState.

    Output: output/<session_id>/REPORT.md
    """
    session_id = state.get("session_id", "dev")
    output_dir = _get_output_dir(session_id)

    profile = state.get("profile_data")
    opportunities = state.get("opportunities", [])
    matches = state.get("matches", [])
    query = state.get("user_query", "")
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Build ranked pairs
    ranked = sorted(
        zip(opportunities, matches),
        key=lambda pair: pair[1].match_score,
        reverse=True,
    )

    lines = [
        "# 🚀 GrantHunter AI — Results Report",
        f"\n**Generated:** {timestamp}  ",
        f"**Session:** `{session_id}`  ",
        f"**Query:** _{query}_",
        "\n---\n",
        "## 👤 Candidate Profile",
    ]

    if profile:
        lines += [
            f"- **Name:** {profile.full_name}",
            f"- **Nationality:** {profile.nationality}",
            f"- **Degree:** {profile.highest_degree}",
            f"- **Skills:** {', '.join(profile.hard_skills)}",
            f"- **Interests:** {', '.join(profile.interests)}",
        ]
    else:
        lines.append("_Profile data unavailable._")

    lines += [
        "\n---\n",
        f"## 🔍 Opportunities Found: {len(opportunities)}",
        f"## 📊 Matches Analyzed: {len(matches)}\n",
        "---\n",
        "## 🏆 Ranked Matches",
    ]

    if not ranked:
        lines.append("\n_No matches were produced in this run._")
    else:
        for rank, (opp, match) in enumerate(ranked, start=1):
            viability = "✅ Viable" if match.is_viable else "⚠️ Not Viable"
            lines += [
                f"\n### #{rank} — Score: {match.match_score}/100 · {viability}",
                f"**URL:** [{opp.get('url', 'N/A')}]({opp.get('url', '')})",
                f"\n**Reasoning:**  \n{match.reasoning}",
            ]
            if match.missing_requirements:
                missing = ", ".join(match.missing_requirements)
                lines.append(f"\n**Missing Requirements:** {missing}")
            lines.append("\n---")

    report_path = output_dir / "REPORT.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
