# 📊 Estado del Proyecto — GrantHunter AI

Este archivo representa el estado actual de madurez del sistema y la hoja de ruta refinada.

---

## ✅ Logros Recientes (Sesión Actual)

1. **Frontend MVP Premium**: Interfaz en Streamlit con estética *Cyber/Technical*, barra de progreso real y visualización de queries internas.
2. **IA 100% en Español**: Agentes programados para razonar, analizar y redactar borradores en español, manteniendo búsquedas en inglés para mayor alcance.
3. **Persistencia Estándar**: Nodo de salida que genera automáticamente `results.json`, `REPORT.md` y `run.log` en carpetas de sesión.
4. **Scoring Implacable**: El Agente Analista ahora penaliza duramente si faltan requisitos críticos (nacionalidad, grado, etc.).
5. **Fix de Interfaz**: Se eliminaron superposiciones de CSS y se corrigió el ordenamiento por puntaje (de mayor a menor).

---

## ⏩ Logros de Sesiones Anteriores

* **Motor llama-4-scout**: Estandarización de inferencia ultra-rápida.
* **Optimización de Tokens**: Extracción inteligente de contenido (reducción de 15k a 4k caracteres).
* **Infraestructura Docker**: Playwright y Postgres integrados.

---

## ⏳ Pendientes Refinados (Hoja de Ruta)

* [ ] **Descubrimiento Interactivo**: Implementar un sistema con un "Stop" claro que permita al usuario elegir entre enlaces generales encontrados por el Discovery antes de profundizar en el scraping.
* [ ] **Factibilidad de Redes Sociales**: Evaluar la integración de fuentes como **LinkedIn, Facebook y Twitter**, donde se publican muchas convocatorias informales.
* [ ] **Arquitectura FastAPI**: Desacoplar el grafo de la UI para permitir ejecuciones asíncronas de larga duración.
* [ ] **Caché de Consultas**: Evitar repetir búsquedas idénticas para optimizar costos y tiempo.

---

## 💡 Notas de Operación

> [!IMPORTANT]
> **Cambio a Producción:** Por defecto, usa `session_id = "dev"`. Para activar carpetas únicas por ejecución, usa:
> `export APP_ENV=production && streamlit run frontend/app.py`

> [!TIP]
> **Estrategia de Búsqueda:** Las *queries* generadas siempre estarán en inglés para maximizar los resultados de fuentes internacionales de alta calidad.

---
*Última actualización: 2026-02-27*
