# 🚀 GrantHunter AI

> **Estado Actual:** ✅ Backend Operativo | 🏗️ Frontend en Desarrollo | 🧠 Modelos: Gemini 1.5 Flash

**GrantHunter AI** es un Agente de Financiación Personal diseñado para perfiles técnicos. A diferencia de un buscador pasivo, este agente **actúa**: busca activamente en la web, lee requisitos complejos, entiende tu perfil y te dice si vale la pena aplicar.

## 🛠️ Arquitectura Técnica

El proyecto funciona sobre una arquitectura de **Agentes Distribuidos** orquestados por LangGraph:

* **Brain (Orchestrator)**: Gestiona el flujo de trabajo (`Identity` -> `Discovery` -> `Analyst`).
* **Identity Core**: Lee tu CV/Perfil (Markdown) y extrae tus "superpoderes" técnicos.
* **Discovery Module**:
  * Usa **Brave Search API** para encontrar oportunidades en tiempo real.
  * Usa un **Scraper Híbrido** (Docker/Local) basado en Playwright para leer cualquier web.
* **Analyst Module**: Usa `Google Gemini 1.5 Flash` para leer las bases de la beca y compararlas con tu perfil.

## 📂 Estructura del Proyecto

* `backend/`: Código fuente de los agentes y herramientas.
* `agentes/`: Entorno virtual de Python con las dependencias.
* `tests/`: Scripts de verificación (Ver `TESTS.md` para más detalle).
* `docker-compose.yml`: Infraestructura (Base de datos y Navegador Remoto).

## ⚡ Guía de Inicio Rápido (Local)

### 1. Requisitos

* Docker & Docker Compose
* Python 3.12+
* Clave API de Google AI Studio (`GOOGLE_API_KEY`)
* Clave API de Brave Search (`BRAVE_SEARCH_API_KEY`)

### 2. Configuración

Crea un archivo `.env` en la raíz:

```bash
GOOGLE_API_KEY="tu_key"
BRAVE_SEARCH_API_KEY="tu_key"
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
