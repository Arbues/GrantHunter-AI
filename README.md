# 🚀 GrantHunter AI

> **Estado Actual:** ✅ Backend Operativo | ✅ Frontend MVP Operativo | 🧠 Modelos: Groq (`llama-4-scout`)

**GrantHunter AI** es un Agente de Financiación Personal diseñado para perfiles técnicos. A diferencia de un buscador pasivo, este agente **actúa**: busca activamente en la web, lee requisitos complejos, entiende tu perfil y te dice si vale la pena aplicar.

---

## 🛠️ Arquitectura Técnica

El proyecto funciona sobre una arquitectura de **Agentes Distribuidos** orquestados por LangGraph:

* **Brain (Orchestrator)**: Gestiona el flujo de trabajo (`Identity` -> `Discovery` -> `Analyst` -> `Output`).
* **Identity Core**: Lee tu CV/Perfil (Markdown) y extrae tus habilidades e intereses.
* **Discovery Module**:
  * Genera 3 queries de búsqueda inteligentes (inglés) para maximizar resultados.
  * Usa **Brave Search API** para encontrar oportunidades en tiempo real.
  * Usa un **Scraper Híbrido** (Docker/Local) con Playwright.
* **Analyst Module**: Evalúa compatibilidad con scoring estricto (penaliza requisitos "hard" no cumplidos).
* **Output Standard**: Persiste resultados en cada ejecución:
  * `results.json`: Datos estructurados para el frontend.
  * `REPORT.md`: Reporte humano legible.
  * `run.log`: Logs detallados de la sesión.
* **Soporte Bilingüe**: Análisis y redacción de borradores en **Español** (IA optimizada).

## 📂 Estructura del Proyecto

* `backend/`: Código fuente de los agentes y herramientas.
* `frontend/`: Interfaz web (`app.py`) en Streamlit con estética *Cyber/Technical*.
* `output/`: Directorio de persistencia de resultados (por sesión).
* `tests/`: Scripts de verificación.
* `docker-compose.yml`: Infraestructura (Base de datos y Navegador Remoto).

## ⚡ Guía de Inicio Rápido

### 1. Requisitos e Instalación

* Docker & Docker Compose
* Python 3.12+
* `.env` configurado con `GROQ_API_KEY` y `BRAVE_SEARCH_API_KEY`.

```bash
# Activar entorno
source agentes/bin/activate
```

### 2. Ejecución de la UI (Frontend)

La forma más recomendada de usar GrantHunter AI es a través de su interfaz web:

```bash
streamlit run frontend/app.py
```

### 3. Ejecución de Prueba (Terminal)

```bash
python3 tests/verify_flow.py
```

## 🧪 Testing y Arquitectura

* Para entender la estrategia de validación: [TESTS.md](./TESTS.md).
* Para detalles de diseño e infraestructura: [ARCHITECTURE.md](./ARCHITECTURE.md).

---
*Built with ❤️ by Antigravity Agent*
