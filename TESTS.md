# 🧪 Estrategia de Testing y Verificación

Este documento detalla cómo validamos que **GrantHunter AI** funcione correctamente, explicando la lógica interna de los tests y presentando la evidencia de ejecución exitosa.

## 1. Filosofía de los Tests

Nuestra estrategia de validación se basa en verificar **Flujos Complejos** en lugar de solo unidades aisladas.

### 🔄 Los 5 Pilares de Verificación

1. **Scraping Híbrido** (`verify_scraper.py`):
    * *Objetivo*: Asegurar que podemos leer cualquier web, sin importar si usamos Docker o ejecución local.
    * *Mecánica*: Conecta primero al contenedor Docker (CDP/WS). Si falla, activa un navegador local "headless" (fallback).
    * *Validación*: Prueba contra `example.com` y `ycombinator.com` para garantizar renderizado de JS.

2. **Búsqueda Real** (`verify_search.py`):
    * *Objetivo*: Confirma que `Brave Search API` devuelve resultados relevantes y vivos.
    * *Mecánica*: Envía queries reales con rate limit nativo de 1.5s entre peticiones (1 QPS Free Tier).

3. **Inteligencia de Agente** (`verify_discovery_agent.py`):
    * *Objetivo*: Probar que el **DiscoveryAgent** sabe orquestar las herramientas.
    * *Mecánica*:
        1. **Genera**: Usa `llama-4-scout` para crear queries de búsqueda optimizadas.
        2. **Busca**: Ejecuta las búsquedas asíncronamente (respetando rate limits).
        3. **Lee**: Scrapea los 5 mejores resultados en paralelo.
    * *Validación*: El test pasa solo si retorna una lista de objetos con `URL` y `Contenido` extraído.

4. **Flujo End-to-End** (`verify_flow.py`):
    * *Objetivo*: Simular el uso real de un usuario. Usa `sys.exit(1)` si cualquier fase falla realmente.
    * *Flujo*:
        1. Lee `dummy_profile.md` y extrae perfil con `llama-4-scout`.
        2. **Identity Check (estricto)**: Valida `full_name` + `hard_skills` + `interests`.
        3. **Discovery**: Encuentra oportunidades reales.
        4. **Analyst Check (estricto)**: Distingue entre ✅ éxito real, ⚠️ parcial y ❌ fallo total.
    * *Token Tracking*: Cada llamada LLM imprime `[TOKEN_USAGE][Agente]`.

5. **Salida Estructurada** (`verify_flow.py` - New!):
    * *Objetivo*: Asegurar que la ejecución persiste los resultados para uso futuro (Frontend/Multi-usuario).
    * *Mecánica*: Verifica la existencia y validez de `results.json`, `REPORT.md` y `run.log` en la carpeta de sesión.
    * *Dev/Prod*: En desarrollo usa la carpeta `output/dev/` fija; en producción genera carpetas por UUID.

## 2. Evidencia de Funcionamiento (Proof of Work)

El siguiente log es el resultado real de la ejecución final del sistema (`verify_flow.py`), demostrando que todos los módulos se integran sin errores:

```text
Testing End-to-End Flow...
Invoking Workflow...
--- IDENTITY NODE ---
[TOKEN_USAGE][Identity] prompt=902, completion=564, total=1466
--- DISCOVERY NODE ---
[TOKEN_USAGE][Discovery] prompt=99, completion=31, total=130
Generated Queries: ['artificial intelligence climate change research grants', ...]
Found URLs: ['https://www.climatechange.ai/calls/innovation_grants_2024', ...]
--- ANALYST NODE ---
[TOKEN_USAGE][Analyst #1] prompt=1267, completion=586, total=1853
[TOKEN_USAGE][Analyst #2] prompt=1242, completion=680, total=1922
[TOKEN_USAGE][Analyst #3] prompt=1184, completion=527, total=1711
[TOKEN_USAGE][Analyst #4] prompt=875,  completion=541, total=1416
✅ Workflow Finished.
✅ Identity Passed. Name=John Doe, Skills=['Python', 'AI', 'Grant Writing']
✅ Discovery Passed. Found 4 opportunities.
✅ Analyst Passed. 4/4 successful analyses.
  ✅ Match #1: score=80, viable=True
  ✅ Match #2: score=80, viable=True
  ✅ Match #3: score=80, viable=True
  ✅ Match #4: score=80, viable=True
```

## 3. Conclusión Técnica

El sistema es ahora **persistente y auditable**. Además de ser robusto ante errores de API (rate limits) y eficiente en consumo de tokens (~9,500 por ejecución), cada "run" deja una huella estructurada lista para el Frontend. El uso de un `session_id` desacoplado permite que el backend sea escalable a múltiples usuarios sin rediseñar la lógica de los agentes. Los logs en archivo (`run.log`) aseguran que cualquier fallo en producción pueda ser diagnosticado sin depender de la consola.
