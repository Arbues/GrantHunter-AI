# 🏗️ GrantHunter AI - Architecture Design

> **Documentación Técnica Visual**
> Este documento detalla la arquitectura del sistema, flujos de datos y relaciones entre componentes utilizando diagramas visuales (Mermaid).

## 🔭 1. Visión General del Sistema (C4 Context)

Representación de alto nivel de cómo interactúa el Usuario con GrantHunter AI y los sistemas externos.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryTextColor':'#1a1a1a','secondaryTextColor':'#1a1a1a','tertiaryTextColor':'#1a1a1a','noteBkgColor':'#fff3cd','noteBorderColor':'#856404','noteTextColor':'#1a1a1a'}}}%%
C4Context
    title System Context Diagram - GrantHunter AI

    Person(user, "Investigador/Usuario", "Busca financiación académica o becas.")
    
    System_Boundary(granthunter, "GrantHunter AI Platform") {
        System(orchestrator, "Agent Orchestrator", "Coordina los agentes inteligentes.")
    }

    System_Ext(groq, "Groq Cloud API", "Inferencia LLM (Qwen + Llama).")
    System_Ext(brave, "Brave Search API", "Búsqueda web en tiempo real.")
    System_Ext(websites, "Sitios Web de Becas", "Universidades, Gobiernos, ONGs.")

    Rel(user, orchestrator, "Sube CV & Query", "CLI / Web")
    Rel(orchestrator, groq, "Generación & Análisis", "JSON/REST")
    Rel(orchestrator, brave, "Descubrimiento", "REST API")
    Rel(orchestrator, websites, "Scraping Contenido", "Playwright Automation")
```

---

## 🧠 2. Flujo de Orquestación (LangGraph)

El "cerebro" del sistema es un grafo de estados que coordina tres agentes especializados.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryTextColor':'#1a1a1a','secondaryTextColor':'#1a1a1a','tertiaryTextColor':'#1a1a1a','noteBkgColor':'#fff3cd','noteBorderColor':'#856404','noteTextColor':'#1a1a1a'}}}%%
stateDiagram-v2
    direction LR
    
    [*] --> IdentityNode: Input (Profile + Query)
    
    state IdentityNode {
        [*] --> ParseProfile
        ParseProfile --> ExtractSkills
        ExtractSkills --> [*]
    }

    IdentityNode --> DiscoveryNode: Profile Data

    state DiscoveryNode {
        [*] --> GenerateQueries
        GenerateQueries --> BraveSearch
        BraveSearch --> ScrapeContent
        ScrapeContent --> [*]
    }

    DiscoveryNode --> AnalystNode: Best Opportunities

    state AnalystNode {
        [*] --> SemaphoreControl
        SemaphoreControl --> AnalyzeMatch
        AnalyzeMatch --> [*]
    }

    AnalystNode --> OutputNode: All Results
    
    state OutputNode {
        [*] --> SaveJSON
        SaveJSON --> GenerateMarkdown
        GenerateMarkdown --> SessionLog
        SessionLog --> [*]
    }

    OutputNode --> [*]: Complete
    
    note right of IdentityNode
        Model: llama-4-scout
        Parses MD profile to data
    end note
    
    note right of DiscoveryNode
        Model: llama-4-scout
        Generates 3 optimized queries
    end note
    
    note right of AnalystNode
        Model: llama-4-scout
        Strict Scoring (Penalizes hard missing reqs)
    end note

    note right of OutputNode
        Persists to output/{session_id}/
        JSON + Report + Log
    end note
```

---

## ⚡ 3. Diagrama de Secuencia de Ejecución

Detalle paso a paso de una ejecución típica de búsqueda de becas.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'actorTextColor':'#1a1a1a','noteBkgColor':'#fff3cd','noteBorderColor':'#856404','noteTextColor':'#1a1a1a','labelTextColor':'#1a1a1a','loopTextColor':'#1a1a1a'}}}%%
sequenceDiagram
    participant U as Usuario
    participant O as Orchestrator (Graph)
    participant I as Identity Agent
    participant D as Discovery Agent
    participant S as Search/Scraper
    participant A as Analyst Agent
    participant LLM as Groq API

    U->>O: 1. Input: "CV.md" + "Busco becas AI"
    
    %% Identity Phase
    rect rgb(240, 248, 255)
    Note over O, I: Fase de Identidad
    O->>I: Procesa Perfil
    I->>LLM: Parse CV (Qwen3-32B)
    LLM-->>I: JSON (Skills, Education)
    I-->>O: FixedIdentityData
    end

    %% Discovery Phase
    rect rgb(255, 250, 240)
    Note over O, S: Fase de Descubrimiento
    O->>D: Busca Oportunidades
    D->>LLM: Genera Queries de Búsqueda
    LLM-->>D: ["Grant A", "Grant B", ...]
    loop Para cada Query
        D->>S: Brave Search API (Wait 1.5s)
        S-->>D: URLs
    end
    D->>S: Scrape URLs (Playwright)
    S-->>D: HTML Content (Title, Body)
    D-->>O: List[Opportunity]
    end

    %% Analyst Phase
    rect rgb(240, 255, 240)
    Note over O, A: Fase de Análisis
        O->>A: Evalúa Matches
        loop Para cada Oportunidad (Serializado)
            A->>LLM: Analyze(Profile, Opportunity)
            Note right of A: IA responde en ESPAÑOL
            LLM-->>A: MatchScore, Reasoning
        end
        A-->>O: List[MatchResult]
    end

    %% Output Phase
    rect rgb(255, 240, 245)
        Note over O, U: Fase de Salida
        O->>O: resolve_session_id('dev')
        O->>O: save_results_json()
        O->>O: generate_report_md()
        O->>U: Final results available in output/
    end
```

---

## 💾 4. Modelo de Datos (Data Dictionary)

Estructura de la información que fluye entre los agentes.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryTextColor':'#1a1a1a','secondaryTextColor':'#1a1a1a','tertiaryTextColor':'#1a1a1a','classText':'#1a1a1a'}}}%%
classDiagram
    class AgentState {
        +str session_id
        +dict run_metadata
        +str profile_file_path
        +str user_query
        +FixedIdentityData profile_data
        +List~str~ queries
        +List~dict~ opportunities
        +List~dict~ matches
    }

    class FixedIdentityData {
        +str full_name
        +str nationality
        +str degree
        +List~str~ skills
        +List~str~ interests
    }

    class Opportunity {
        +str url
        +str title
        +str content
        +str source
    }

    class MatchResult {
        +int match_score
        +str reasoning
        +List~str~ missing_requirements
        +boolean is_viable
    }

    AgentState *-- FixedIdentityData
    AgentState *-- Opportunity
    AgentState *-- MatchResult
```

---

## 🏗️ 5. Infraestructura & Despliegue

Componentes físicos (Contenedores) del sistema local.

```mermaid
%%{init: {'theme':'base', 'themeVariables': {'primaryTextColor':'#1a1a1a','secondaryTextColor':'#1a1a1a','tertiaryTextColor':'#1a1a1a','edgeLabelBackground':'#ffffff'}}}%%
graph TD
    subgraph "Docker Host"
        subgraph "Network: granthunter_net"
            DB[("Postgres (pgvector)\nImage: ankane/pgvector")]
            Browser["Playwright Service\nImage: mcr.microsoft.com/playwright:v1.58.1-jammy\nPort: 3000"]
        end
    end

    subgraph "Local Host"
        App["Python Pipeline\n(LangGraph Orchestrator)"]
        UI["Streamlit Frontend\n(app.py)"]
    end

    UI -- "ainvoke()" --> App
    App -- "CDP (ws://localhost:3000)" --> Browser
    App -- "SQL (localhost:5432)" --> DB
    App -- "HTTPS" --> Groq_API[Groq API]
    App -- "HTTPS" --> Brave_API[Brave Search API]
    App -- "Write" --> Output[("./output/session_id/")]

    style DB fill:#f9f,stroke:#333,stroke-width:2px
    style Browser fill:#bbf,stroke:#333,stroke-width:2px
    style App fill:#bfb,stroke:#333,stroke-width:2px
    style UI fill:#ffa,stroke:#333,stroke-width:2px
```

## 🧩 6. Tabla de Tecnologías

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Lenguaje** | Python 3.12 | Core logic |
| **Orquestación** | LangGraph | State management, ciclos |
| **LLM Inference** | Groq SDK | Inferencia ultra-rápida |
| **Modelos** | `llama-4-scout-17b-16e-instruct` | Todos los agentes (30k TPM, predecible) |
| **Analyst Module** | llama-4-scout | Evalúa match perfil vs beca (Scoring Estricto, IA en Español) |
| **Output Node** | Python Logic | Persistencia JSON, Markdown y Logs por sesión |
| **Frontend UI** | Streamlit | Interfaz Cyber/Technical con feedback en vivo |
| **Token Tracking** | Native Groq | Monitoreo de consumo por agente |
| **Búsqueda** | Brave Search API | Privacidad + Índice independiente (Búsquedas en Inglés) |
| **Base de Datos** | PostgreSQL + pgvector | (Futuro) Memoria a largo plazo |
