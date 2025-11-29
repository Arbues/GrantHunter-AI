# GrantHunter AI - Development Tasks

- [ ] **Phase 1: Infrastructure & Setup**
    - [x] Create Implementation Plan <!-- id: 0 -->
    - [x] Create `docker-compose.yml` (PostgreSQL + Playwright Service) <!-- id: 1 -->
    - [x] Initialize Python Monorepo (Orchestrator + MCP Servers) <!-- id: 2 -->
    - [x] Configure Environment (Gemini API, DB Connection) <!-- id: 3 -->

- [ ] **Phase 2: MCP Servers (The Limbs)**
    - [x] **Identity Server**
        - [x] Implement MD/TXT File Reader <!-- id: 4 -->
        - [x] Implement Hybrid Parser (Gemini -> JSON + Chunks) <!-- id: 5 -->
    - [x] **Discovery Server**
        - [x] Implement Search Tool (Brave/Serper) <!-- id: 6 -->
        - [x] Implement Robust Scraper (Playwright in Docker) <!-- id: 7 -->
    - [x] **Analyst & Executor Servers**
        - [x] Implement Match Scoring Logic (Gemini) <!-- id: 8 -->
        - [x] Implement Application Drafter (Gemini) <!-- id: 9 -->

- [x] **Phase 3: Orchestration (The Brain)**
    - [x] Setup LangGraph State Graph <!-- id: 10 -->
    - [x] Implement Agent Workflow (Identity -> Discovery -> Analyst) <!-- id: 11 -->

- [x] **Phase 4: Interface (Streamlit MVP)**
    - [x] Setup Streamlit App <!-- id: 12 -->
    - [x] Implement Profile Selection (Local Files) <!-- id: 13 -->
    - [x] Implement Chat/Search Interface <!-- id: 14 -->
    - [x] Implement Results Display (Match Scores) <!-- id: 15 -->

- [x] **Phase 5: Verification**
    - [x] Test Playwright Scraper on Dynamic Sites <!-- id: 16 -->
    - [x] End-to-End Flow Test <!-- id: 17 -->
