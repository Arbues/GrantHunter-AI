# 🚀 GrantHunter AI

> **Estado Actual:** ✅ Backend Operativo | 🏗️ Frontend en Desarrollo | 🧠 Modelos: Groq (Qwen3-32B + Compound)

**GrantHunter AI** es un Agente de Financiación Personal diseñado para perfiles técnicos. A diferencia de un buscador pasivo, este agente **actúa**: busca activamente en la web, lee requisitos complejos, entiende tu perfil y te dice si vale la pena aplicar.

## 🛠️ Arquitectura Técnica

El proyecto funciona sobre una arquitectura de **Agentes Distribuidos** orquestados por LangGraph:

* **Brain (Orchestrator)**: Gestiona el flujo de trabajo (`Identity` -> `Discovery` -> `Analyst`).
* **Identity Core**: Lee tu CV/Perfil (Markdown) y extrae tus "superpoderes" técnicos usando **Groq Qwen3-32B**.
* **Discovery Module**:
  * Usa **Brave Search API** para encontrar oportunidades en tiempo real (con rate limiting de 1.5s).
  * Usa un **Scraper Híbrido** (Docker/Local) basado en Playwright para leer cualquier web.
  * Genera búsquedas inteligentes con **Groq Qwen3-32B**.
* **Analyst Module**: Usa **Groq Compound** para leer las bases de la beca y compararlas con tu perfil (con semáforo para evitar rate limits).

## 📂 Estructura del Proyecto

* `backend/`: Código fuente de los agentes y herramientas.
* `agentes/`: Entorno virtual de Python con las dependencias.
* `tests/`: Scripts de verificación (Ver `TESTS.md` para más detalle).
* `docker-compose.yml`: Infraestructura (Base de datos y Navegador Remoto).

## ⚡ Guía de Inicio Rápido (Local)

### 1. Requisitos

* Docker & Docker Compose
* Python 3.12+
* Clave API de Groq (`GROQ_API_KEY`) - [Obtener aquí](https://console.groq.com)
* Clave API de Brave Search (`BRAVE_SEARCH_API_KEY`)

### 2. Configuración

Crea un archivo `.env` en la raíz:

```bash
GROQ_API_KEY=tu_key_de_groq
BRAVE_SEARCH_API_KEY=tu_key_de_brave
```

### 3. Ejecución

Levanta los servicios base (opcional, el sistema tiene fallback local):

```bash
docker compose up -d
```

Ejecuta el flujo completo de prueba:

```bash
./agentes/bin/python3 tests/verify_flow.py
```

## 🧪 Testing

Para entender cómo validamos que el software realmente funciona, lee el archivo [TESTS.md](./TESTS.md).
