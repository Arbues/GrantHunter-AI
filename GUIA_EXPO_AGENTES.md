# 🎓 Guía de Estudio y Exposición: Agentes AI en GrantHunter

Esta guía ha sido diseñada para ayudarte a entender las profundidades de GrantHunter AI y para que puedas realizar una exposición brillante ante tu grupo de clase.

---

## 📚 1. Fundamentos: ¿Qué es un Agente?

Antes de mostrar código, debes explicar el concepto. Un Agente no es solo un programa; es una entidad que utiliza un LLM (Cerebro) para razonar y actuar.

- **Percepción**: El agente recibe entradas (tu CV y tu búsqueda).
- **Razonamiento**: El LLM decide qué pasos tomar basándose en un sistema de estados.
- **Acción**: El agente usa herramientas (Brave Search, Playwright) para interactuar con el mundo.

**Concepto Clave**: GrantHunter usa un **Grafo de Estados** (via [LangGraph](file:///home/arbues/Github/personales/GrantHunter-AI/ARCHITECTURE.md)). Esto permite que el sistema no sea lineal, sino que pueda tomar decisiones lógicas en cada nodo.

---

## 🏗️ 2. Arquitectura de GrantHunter (El Cerebro)

Durante tu exposición, abre el archivo [ARCHITECTURE.md](file:///home/arbues/Github/personales/GrantHunter-AI/ARCHITECTURE.md) y muestra el diagrama de "Flujo de Orquestación".

### Los 4 Nodos del Sistema

1. **Identity Node (El Analista de Perfil)**:
    - **Función**: Lee tu CV y extrae data estructurada (Skills, Intereses).
    - **Dónde verlo**: [backend/mcp_servers/identity/parser.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/mcp_servers/identity/parser.py)
    - **Punto para explicar**: Cómo convertimos un Markdown desordenado en un JSON limpio que los demás agentes puedan entender.

2. **Discovery Node (El Investigador)**:
    - **Función**: Genera queries de búsqueda, navega por internet y extrae contenido de webs.
    - **Dónde verlo**: [backend/mcp_servers/discovery/discovery.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/mcp_servers/discovery/discovery.py)
    - **Punto para explicar**: Este agente usa **Herramientas (Tools)**. No sabe el contenido de antemano, sale a buscarlo usando la API de Brave.

3. **Analyst Node (El Juez Estricto)**:
    - **Función**: Compara el perfil del usuario con cada beca encontrada y da un puntaje.
    - **Dónde verlo**: [backend/mcp_servers/analyst/analyst.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/mcp_servers/analyst/analyst.py)
    - **Punto para explicar**: Es "estricto". Si no cumples la nacionalidad o el grado, te pone un puntaje bajo. ¡Y responde en español!

4. **Output Node (El Secretario)**:
    - **Función**: Organiza todo y genera los reportes finales.
    - **Dónde verlo**: [backend/orchestrator/graph.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/orchestrator/graph.py) (función `output_node`).

---

## 💻 3. Mapa de Código para la Exposición

Cuando te pregunten "muéstrame el código", dirígete a estos puntos clave:

1. **El Orquestador**: [backend/orchestrator/graph.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/orchestrator/graph.py)
    - Muestra cómo se define el flujo: `workflow.add_node`, `workflow.add_edge`. Esto es la "coreografía" de los agentes.
2. **El Prompt del Analista**: [backend/mcp_servers/analyst/analyst.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/mcp_servers/analyst/analyst.py#L33-L58)
    - Muestra el `PromptTemplate`. Explica cómo le damos "personalidad" y "reglas" (ser estricto, hablar español).
3. **El Estado**: [backend/orchestrator/state.py](file:///home/arbues/Github/personales/GrantHunter-AI/backend/orchestrator/state.py)
    - Explica que los agentes comparten una "memoria de corto plazo" llamada `AgentState`.

---

## 🎤 4. Guion Sugerido para la Exposición (10-15 min)

1. **Intro (2 min)**: "Hoy les presento GrantHunter AI, un sistema multi-agente que busca becas por ti."
2. **Arquitectura (3 min)**: Muestra el diagrama de [ARCHITECTURE.md](file:///home/arbues/Github/personales/GrantHunter-AI/ARCHITECTURE.md). Explica que usamos LangGraph para orquestar.
3. **Deep Dive: Agentes (5 min)**:
    - Abre `discovery.py`. "Aquí el agente razona qué buscar."
    - Abre `analyst.py`. "Aquí el agente evalúa con criterio humano."
4. **Demostración / Resultados (3 min)**: Muestra un ejemplo en la carpeta `output/` (si tienes una corrida previa).
5. **Cierre (2 min)**: "La clave no es solo el LLM, es cómo conectamos el razonamiento con herramientas externas."

---

## 💡 Tips de Oro

- **Menciona Groq**: Di que usamos Groq por su velocidad extrema (Llama 4 Scout), lo que permite que los agentes "piensen" en milisegundos.
- **Explica el 'Think'**: En el código verás un `re.sub(r'<think>.*?</think>', ...)`. Explica que esto es para limpiar los pensamientos internos de los modelos de razonamiento antes de mostrar el resultado final.
- **Transparencia**: Di que los agentes son deterministas en su flujo pero creativos en su análisis.

---
*¡Mucha suerte en tu exposición, Arbués! Con esto demostrarás que dominas la arquitectura de agentes moderna.*
