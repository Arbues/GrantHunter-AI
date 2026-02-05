# 🧪 Estrategia de Testing y Verificación

Este documento detalla cómo validamos que **GrantHunter AI** funcione correctamente, explicando la lógica interna de los tests y presentando la evidencia de ejecución exitosa.

## 1. Filosofía de los Tests

Nuestra estrategia de validación se basa en verificar **Flujos Complejos** en lugar de solo unidades aisladas.

### 🔄 Los 4 Pilares de Verificación

1. **Scraping Híbrido** (`verify_scraper.py`):
    * *Objetivo*: Asegurar que podemos leer cualquier web, sin importar si usamos Docker o ejecución local.
    * *Mecánica*: El software intenta conectar primero al contenedor Docker (CDP/WS). Si falla (o el protocolo no coincide), activa automáticamente un navegador local "headless" (fallback).
    * *Validación*: Se prueba contra una web simple (`example.com`) y una SPA compleja (`ycombinator.com`) para garantizar que el JavaScript se renderiza.

2. **Búsqueda Real** (`verify_search.py`):
    * *Objetivo*: Confirma que `Brave Search API` devuelve resultados relevantes y vivos.
    * *Mecánica*: Envía queries reales (ej: "grants for AI research").
    * *Rate Limiting*: **IMPORTANTE**. Se valida que el sistema espere 1.5s entre peticiones para respetar el Free Tier de Brave (1 QPS).

3. **Inteligencia de Agente** (`verify_discovery_agent.py`):
    * *Objetivo*: Probar que el **DiscoveryAgent** (el cerebro) sabe orquestar las herramientas.
    * *Mecánica*:
        1. **Genera**: Usa `Groq Qwen3-32B` para crear variaciones de búsqueda ("Smart Queries").
        2. **Busca**: Ejecuta las búsquedas de forma asíncrona (respetando rate limits).
        3. **Lee**: Scrapea los 5 mejores resultados en paralelo.
    * *Validación*: El test pasa solo si retorna una lista de objetos con `URL` y `Contenido` extraído.

4. **Flujo End-to-End** (`verify_flow.py`):
    * *Objetivo*: Simular el uso real de un usuario.
    * *Flujo*:
        1. El sistema lee un perfil Markdown (`dummy_profile.md`).
        2. **Identity Core**: Extrae skills y nacionalidad usando **Groq Qwen3-32B**.
        3. **Discovery**: Encuentra becas compatibles.
        4. **Analyst**: Usa **Groq Compound** (con control de concurrencia) para comparar "Perfil vs. Beca" y asignar un puntaje.

## 2. Evidencia de Funcionamiento (Proof of Work)

El siguiente log es el resultado real de la ejecución final del sistema (`verify_flow.py`), demostrando que todos los módulos se integran sin errores:

```text
Testing End-to-End Flow...
Invoking Workflow...
--- IDENTITY NODE ---
--- DISCOVERY NODE ---
Generated Queries:
['AI for climate solutions grant opportunity foundation',
 'computational sustainability funding announcement university research',
 'machine learning climate modeling research fellowship']

# ... Conexión exitosa al navegador remoto (Docker) ...
Connected to remote Playwright via WS.
Navigating to https://www.climatechange.ai/calls/innovation_grants_2024...
Navigating to https://www.nsf.gov/news/news_summ.jsp?cntn_id=132978&org=NSF...
...

--- ANALYST NODE ---
✅ Workflow Finished.
✅ Identity Step Passed.
✅ Discovery Step Passed. Found 4 opportunities.
✅ Analyst Step Passed. Analyzed 4 matches.
```

## 3. Conclusión Técnica

El sistema ha demostrado ser **robusto y autocurativo** (scraper) y **funcional end-to-end**. La migración a **Groq** ha mejorado drásticamente la latencia de inferencia, y la implementación de rate limiters y semáforos asegura la estabilidad frente a límites de API.
