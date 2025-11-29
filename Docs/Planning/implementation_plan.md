# Implementation Plan - GrantHunter AI

## Goal
Develop **GrantHunter AI**, an intelligent distributed agent system that acts as a Personal Funding Agent. It actively searches for grants/scholarships, evaluates compatibility, and assists in drafting applications.

## User Review Required
> [!IMPORTANT]
> **LLM Provider**: This project will use **Google Gemini (Google AI Studio)** as the core intelligence.
> **Strict MVP Scope**: Frontend will be a minimal **Streamlit** interface. No React/Next.js for this phase.
> **Input Format**: User profiles must be provided as **Markdown (.md) or Text (.txt)** files. PDF ingestion for profiles is out of scope for MVP.
> **No Authentication**: User accounts and login features are excluded from the MVP.

## Tech Stack
- **Frontend**: Streamlit (Python) for a functional, clean, and rapid MVP UI.
- **Backend Orchestration**: Python, **LangGraph** for managing agent state and workflows.
- **Agent Protocol**: **MCP (Model Context Protocol)** to modularize agents.
- **Database**: **PostgreSQL** (running in a **Docker Container**) for structured data.
- **Browser Automation**: **Playwright** (running in a **Docker Container**) for robust deep web scraping.
- **LLM**: Google Gemini (via Google AI Studio API).

## Proposed Architecture (MCP Distributed System)

The system is designed as a set of specialized MCP Servers orchestrated by a central brain.

### 1. Orchestrator (The Brain)
- **LangGraph**: Manages the state and control flow between agents.
- **Responsibility**: Receives user commands, delegates to specific MCP servers, and aggregates results.

### 2. MCP Servers (The Limbs)
- **Identity Server (MCP)**:
    - **Input**: Reads local Markdown/TXT files.
    - **Output Strategy**: **Hybrid Data Structure**.
        - **Fixed Data (JSON)**: Structured fields (Skills, Education, **Interests**, Nationality) for filtering and search.
        - **Narrative Chunks (RAG)**: Text fragments vectorized using **Gemini Embeddings** for drafting.
- **Discovery Server (MCP)**:
    - **Tools**: `search_tool` (Brave Search/Serper), `scrape_tool` (Playwright in Docker).
    - **Workflow**: LLM generates multiple search queries -> Tool executes them in parallel -> Scraper extracts content (**HTML only for MVP**).
- **Analyst Server (MCP)**:
    - **Responsibility**: Compares User Profile (Fixed Data) vs. Scraped Opportunity.
    - **Logic**: Uses Gemini to score matches and generate "Gap Analysis".
- **Executor Server (MCP)**:
    - **Responsibility**: Generates application drafts (Cover Letters, Form Answers).
    - **Trigger**: **User-Initiated**. The user selects a specific opportunity to draft, preventing token waste on low-quality matches.
    - **Logic**: **On-Demand Retrieval (Pull)**. Requests specific "Narrative Chunks" from Identity Server.

### 3. Data Layer
- **PostgreSQL (Docker)**: Stores opportunities, match scores, and scraped content.
- **State Management**: LangGraph checkpoints to handle the session flow.

## Development Steps

### Phase 1: Infrastructure & Containers
1.  **Docker Setup**: Create `docker-compose.yml` for PostgreSQL and a Playwright Service (browserless or custom container).
2.  **Project Structure**: Initialize a monorepo-like structure for the Orchestrator and MCP Servers.
3.  **Env Setup**: Configure Gemini API keys and Database URLs.

### Phase 2: Core Agents (Backend)
1.  **Identity MCP**: Implement file reader for `.md`/`.txt` and profile parser.
2.  **Discovery MCP**:
    - Implement `Playwright` scraper ensuring it runs reliably inside the container.
    - Implement Search tool.
3.  **Analyst & Executor MCP**: Implement Gemini-based logic for scoring and drafting.

### Phase 3: Orchestration (LangGraph)
1.  Define the Graph: `User Input` -> `Identity` -> `Discovery` -> `Analyst` -> `Executor` -> `Output`.
2.  Implement state management to pass context between steps.

### Phase 4: Interface (MVP)
1.  **Streamlit App**:
    - Sidebar: Upload/Select Profile File (MD/TXT).
    - Main Area: Chat interface for commands ("Find grants for...").
    - Results View: Simple tables/cards showing Match Score and "Why/Why Not".

## Verification Plan
### Automated Tests
- **Unit Tests**: `pytest` for each MCP server logic.
- **Integration Tests**: Verify LangGraph flow from Input to Output.

### Manual Verification
- **Ingestion Test**: Verify Playwright successfully scrapes a complex dynamic site (e.g., a university funding page) running from the Docker container.
- **Match Test**: Provide a dummy `.md` profile and a known grant URL, verify the Match Score is logical.
