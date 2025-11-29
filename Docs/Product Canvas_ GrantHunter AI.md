# **🚀 Product Canvas: GrantHunter AI**

**Versión:** 1.1 (Ajuste de Fuentes) | **Owner:** Arbués Pérez | **Status:** Definición de Producto

## **1\. Visión del Producto**

**GrantHunter AI** es una plataforma web inteligente que actúa como un **Agente de Financiación Personal** enfocado en perfiles técnicos y de investigación. A diferencia de los buscadores pasivos, GrantHunter *caza* activamente oportunidades (becas, grants, **workshops, eventos totalmente financiados**) en la web profunda, **extrae requisitos** de fuentes variadas (HTML, PDFs, formularios), evalúa la compatibilidad con el perfil académico del usuario y redacta borradores de aplicación, eliminando el 90% de la fricción administrativa en la búsqueda y postulación a fondos.

## **2\. El Problema vs. La Solución**

| El Dolor (Problem) | La Solución (GrantHunter AI) |
| :---- | :---- |
| **Búsqueda Fragmentada:** Perder horas navegando sitios de universidades, redes sociales y portales de eventos, donde la información está diluida. | **Discovery Agéntico:** Un agente autónomo escanea múltiples fuentes (URLs) y extrae solo lo relevante, sin importar el formato de la convocatoria. |
| **Fatiga de Lectura:** Leer bases complejas (o contenido dinámico) para descubrir al final que no eres elegible por un requisito menor. | **Filtro Inteligente (Match Score):** El sistema lee la convocatoria y te dice: *"Match 85%. Cumples todo excepto X"* antes de que inviertas tiempo. |
| **Síndrome de la Hoja en Blanco:** No saber cómo adaptar el CV o la carta de motivación a esa beca específica. | **Redacción Contextual:** Genera las respuestas del formulario y adapta tu CV basándose en *tus* logros reales y *sus* requisitos. |
| **Gestión del Caos:** Tener links en Excel, fechas en el calendario y borradores en Word. | **Grant Kanban:** Un tablero visual unificado para gestionar el estado y los *deadlines* de cada aplicación. |

## 

## **3\. Módulos del Producto (Funcionalidad)**

### **Módulo A: El Núcleo de Identidad (Identity Core)**

*El cerebro que sabe quién eres.*

* **Perfil Holístico:** Ingesta de CV (PDF/LaTeX), Portafolio (Markdown/Web), y Preferencias (Países, Monto Mínimo, Temas de Interés).  
* **Vectorización de Logros:** Desglosa tus proyectos (ej. "Sistema de Papas") en "skills atómicos" (Python, SARIMA, Agricultura) para hacer cruces semánticos, no solo de palabras clave.

### **Módulo B: El Cazador (Deep Discovery)**

*El agente que sale a buscar.*

* **Búsqueda Activa:** No espera a que la base de datos se actualice. El usuario puede decir *"Busca grants de robótica en Alemania para peruanos"* y el agente navega en tiempo real.  
* **Ingesta de Contenido Robusta:** Capacidad de **leer webs dinámicas (Playwright)**, contenido estático o descargar/leer PDFs para obtener las bases.

### **Módulo C: El Analista (Match & Strategy)**

*El juez que decide si vale la pena.*

* **Scoring de Viabilidad:** Asigna un puntaje (0-100%) basado en requisitos duros (Visa, Grado, Edad) y blandos (Tema de investigación o alineación con el evento).  
* **Análisis de Brechas (Gap Analysis):** Muestra visualmente: *"Te falta el certificado de inglés C1, ¿puedes conseguirlo antes del deadline?"*.

### **Módulo D: El Ejecutor (Application Assistant)**

*El redactor que trabaja por ti.*

* **Generador de Respuestas:** Crea borradores para preguntas típicas ("Why you?", "Research Proposal") citando tus proyectos pasados como evidencia.  
* **Pre-llenado (Form Helper):** Mapea los campos del formulario web y te entrega los datos listos para copiar/pegar (MVP) o inyecta los datos en el navegador (Futuro).

## **4\. Definición del MVP vs. Producto Final**

Aquí definimos el alcance para ser realistas pero ambiciosos.

| Característica | 🟢 MVP (Lo que construimos AHORA) | 🟡 Producto Final (Visión Atractiva) |
| :---- | :---- | :---- |
| **Interfaz (UI)** | **Dashboard Simple (Streamlit/FastAPI UI):** Subida de archivos, Chatbot de comandos, Lista de resultados. | **Web App React/Next.js:** Diseño "Dark Mode" futurista, animaciones, drag-and-drop. |
| **Input de Perfil** | Archivos Markdown/Texto locales en carpeta. | Formulario web interactivo, importación de LinkedIn/GitHub con un clic. |
| **Búsqueda** | Basada en listas de URLs predefinidas o búsqueda general simple (Brave). | Integración con APIs de Google Scholar, LinkedIn Jobs y Scraping masivo programado. |
| **Resultados** | JSON/Tabla con Links y Score de Match. | **Tarjetas Interactivas:** Vista detallada con "Semáforo" de requisitos (Verde/Rojo). |
| **Aplicación** | Generación de un archivo respuestas.md descargable. | **Modo "Copiloto":** Una extensión de navegador o vista dividida que llena los campos web por ti. |
| **Feedback** | Logs de texto. | Sistema de aprendizaje: Si rechazas una beca, el agente aprende tus gustos. |

## **5\. Diseño de Experiencia de Usuario (UX Flow)**

### **El Flujo "Happy Path" (Producto Final)**

1. **Onboarding:** Usuario sube su CV (PDF) y pega link de su Portafolio. El sistema extrae los datos y crea el "Perfil Digital".  
2. **Command Center:** Usuario escribe: *"Busca pasantías de verano en visión por computador en Europa"*.  
3. **Scanning (Animación):** El sistema muestra que está "Pensando/Navegando" (usando Agentes MCP por detrás).  
4. **Resultados:** Aparecen 5 tarjetas.  
   * *Tarjeta 1 (ESA Internship):* **95% Match**.  
   * *Tarjeta 2 (Max Planck):* **60% Match** (Falta requisito de PhD).  
5. **Deep Dive:** Usuario hace clic en *ESA Internship*. Ve el resumen de requisitos y el botón **"Preparar Aplicación"**.  
6. **Drafting:** El sistema genera las respuestas a las preguntas del formulario. Usuario edita/aprueba.  
7. **Submission:** Usuario recibe todos los textos finales y la lista de documentos a adjuntar para hacer el envío manual en el portal oficial.

## **6\. Arquitectura Conceptual (Sin entrar en código)**

* **Frontend:** Web App (Next.js \+ Tailwind). Debe sentirse rápida y "técnica".  
* **Backend Brain:** Orquestador de Agentes (Python).  
* **Memoria:** Base de datos local/nube (PostgreSQL) para guardar el historial de búsqueda y aplicaciones.  
* **Los Brazos (MCP):**  
  * *Brazo Web:* Navegador Headless para leer el mundo.  
  * *Brazo Lector:* Procesador de Documentos para leer PDFs.  
  * *Brazo Escritor:* LLM para redactar ensayos.

## **7\. Criterios de Éxito del Producto**

Para considerar que este software es un éxito para tu portafolio y uso personal:

1. **Precisión del Match:** El agente NO debe recomendar oportunidades si el perfil es incompatible (ej. becas para la UE vs. perfil peruano).  
2. **Ahorro de Tiempo:** El usuario debe poder evaluar la viabilidad de una oportunidad en **2 minutos** (vs 30 min de lectura manual).  
3. **Seguridad:** El usuario siempre tiene el control final del envío ("Human in the loop"). Nunca se envía nada automáticamente.  
4. **Estética:** Debe verse como una herramienta profesional de ingeniería, no como un prototipo escolar.