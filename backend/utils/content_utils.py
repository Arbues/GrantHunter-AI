"""
Utilities for smart content extraction to minimize LLM token usage
while preserving the most relevant information.
"""

GRANT_KEYWORDS = [
    "deadline", "eligibility", "requirements", "funding", "apply",
    "criteria", "award", "grant", "scholarship", "fellowship",
    "amount", "budget", "eligible", "submit", "application",
    "who can apply", "how to apply", "selection", "evaluation"
]


def extract_relevant_content(raw_text: str, max_chars: int = 4000) -> str:
    """
    Extracts the most relevant sections of scraped content for grant analysis.
    
    Strategy:
      1. Lines containing grant keywords are prioritized (moved to the top).
      2. Remaining lines are appended up to max_chars.
      3. Hard truncation is applied at max_chars to enforce the token budget.
    
    This is more effective than naive slicing because boilerplate (navbars,
    footers, ads) that appears at the start/end of scraped pages is deprioritized.
    """
    if not raw_text:
        return ""

    lines = raw_text.splitlines()
    priority_lines = []
    rest_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(kw in stripped.lower() for kw in GRANT_KEYWORDS):
            priority_lines.append(stripped)
        else:
            rest_lines.append(stripped)

    combined = "\n".join(priority_lines) + "\n\n" + "\n".join(rest_lines)
    return combined[:max_chars]


def log_token_usage(agent_name: str, response) -> None:
    """
    Logs Groq token usage from a LangChain response object.
    Groq returns usage in response.response_metadata['token_usage'].
    """
    try:
        usage = response.response_metadata.get("token_usage", {})
        prompt = usage.get("prompt_tokens", "?")
        completion = usage.get("completion_tokens", "?")
        total = usage.get("total_tokens", "?")
        print(f"[TOKEN_USAGE][{agent_name}] prompt={prompt}, completion={completion}, total={total}")
    except Exception:
        pass  # Non-critical: never crash because of logging
