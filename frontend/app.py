import streamlit as st
import asyncio
import os
import sys
import uuid
import time
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(override=True)

# --- CONFIGURACIÓN DE RUTAS ---
# Añadir la raíz al path para permitir importaciones desde backend
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from backend.orchestrator.graph import app as workflow_app, resolve_session_id
from backend.mcp_servers.executor.executor import ExecutorAgent
# Importamos modelos para tipado (opcional)
from backend.mcp_servers.identity.models import FixedIdentityData, NarrativeChunk

# --- INICIALIZACIÓN DE SESIÓN ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = resolve_session_id()

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GrantHunter AI — Terminal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UI CYBER PREMIUM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'JetBrains+Mono', monospace;
    }
    
    .stApp {
        background-color: #0b0e14;
        color: #e6edf3;
    }
    
    /* Estilo de Tarjeta Personalizada - Simplificado para evitar superposición */
    .stCard {
        background-color: #161b22;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin: 10px 0 24px 0;
    }
    .stCard:hover {
        border-color: #238636;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
    
    /* Colores de Estado */
    .status-box {
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .status-viable { background-color: #238636; color: white; border: 1px solid #3fb950; }
    .status-low { background-color: #8e6a00; color: white; border: 1px solid #d29922; }
    
    /* Títulos */
    h1, h2, h3 {
        color: #58a6ff;
        font-weight: 700;
    }

    /* Estilo para el área de texto del borrador */
    textarea {
        background-color: #0d1117 !important;
        color: #d1d5da !important;
        border: 1px solid #30363d !important;
    }
    
    /* Estilo para las queries */
    .query-tag {
        display: inline-block;
        background-color: #21262d;
        color: #8b949e;
        padding: 2px 8px;
        border-radius: 4px;
        margin: 2px;
        font-size: 0.8rem;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://img.icons8.com/isometric/100/rocket.png", width=80)
with col2:
    st.title("GrantHunter AI")
    st.caption(f"v1.0.0-beta · Sesión: `{st.session_state['session_id']}`")

st.divider()

# --- SIDEBAR: NÚCLEO DE IDENTIDAD ---
with st.sidebar:
    st.header("🧬 Núcleo de Identidad")
    uploaded_file = st.file_uploader("Cargar Perfil (Markdown/Texto)", type=["md", "txt"])
    
    profile_path = None
    if uploaded_file:
        profile_path = os.path.join("tests", f"active_profile_{st.session_state['session_id']}.md")
        with open(profile_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Archivo cargado: {uploaded_file.name}")
        
    st.info("El Agente de Identidad analizará tu perfil para extraer habilidades e intereses.")

# --- PRINCIPAL: CENTRO DE COMANDO ---
st.subheader("📡 Centro de Comando")
# Quitamos el help= para evitar problemas de rendering de tooltips
query = st.text_input(
    "Consulta de Búsqueda", 
    placeholder="Ej: Buscar becas de doctorado en IA para estudiantes peruanos en Europa"
)

launch_col, _ = st.columns([1, 5])

if launch_col.button("🚀 INICIAR AGENTES") and profile_path and query:
    # --- EJECUCIÓN DEL FLUJO ---
    progress_bar = st.progress(0, text="Preparando motores...")
    
    with st.status("🛠️ Orquestando Agentes...", expanded=True) as status:
        st.write("Inicializando estado del sistema...")
        progress_bar.progress(10, text="Inicializando sistema...")
        
        initial_state = {
            "session_id": st.session_state["session_id"],
            "run_metadata": {"source": "streamlit"},
            "profile_file_path": profile_path,
            "user_query": query
        }
        
        try:
            st.write("Ejecutando Pipeline de LangGraph...")
            progress_bar.progress(30, text="Analizando Identidad y Generando Búsquedas...")
            
            # Ejecución asíncrona
            result = asyncio.run(workflow_app.ainvoke(initial_state))
            
            progress_bar.progress(100, text="¡Proceso finalizado!")
            st.session_state["results"] = result
            st.session_state["profile_data"] = result.get("profile_data")
            st.session_state["narrative_chunks"] = result.get("narrative_chunks")
            st.session_state["queries"] = result.get("queries", [])
            
            status.update(label="✅ ¡Análisis Completado!", state="complete", expanded=False)
            st.balloons()
            time.sleep(1)
            progress_bar.empty()
            
        except Exception as e:
            st.error(f"Fallo en la ejecución: {e}")
            status.update(label="❌ Error de Ejecución", state="error")
            progress_bar.empty()

# --- DASHBOARD DE RESULTADOS ---
if "results" in st.session_state:
    st.divider()
    
    # Mostrar Queries Generadas
    if st.session_state.get("queries"):
        st.write("🔍 **Estrategia de Búsqueda (en inglés):**")
        q_html = "".join([f'<span class="query-tag">{q}</span>' for q in st.session_state["queries"]])
        st.markdown(f"<div>{q_html}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    res = st.session_state["results"]
    matches = res.get("matches", [])
    opportunities = res.get("opportunities", [])
    
    st.subheader(f"📊 Oportunidades Encontradas ({len(matches)})")
    
    if not matches:
        st.warning("No se encontraron oportunidades. Intenta con una consulta más amplia.")
    else:
        # Ordenamiento por Score (Mayor a Menor)
        results_list = []
        for i in range(len(matches)):
            results_list.append({
                "opp": opportunities[i],
                "match": matches[i],
                "orig_idx": i
            })
        results_list.sort(key=lambda x: x["match"].match_score, reverse=True)
        
        for i, item in enumerate(results_list):
            opp = item["opp"]
            match = item["match"]
            idx = item["orig_idx"]
            rank = i + 1
            
            # Contenedor de Oportunidad
            with st.container():
                st.markdown(f"""
                <div class="stCard">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <h3 style="margin:0;">#{rank} · Puntaje: {match.match_score}/100</h3>
                        <span class="status-box {'status-viable' if match.is_viable else 'status-low'}">
                            {'VIABLE' if match.is_viable else 'BAJA COMPATIBILIDAD'}
                        </span>
                    </div>
                    <p style="margin-bottom: 8px;"><b>Fuente:</b> <a href="{opp['url']}" target="_blank" style="color:#58a6ff; text-decoration: none;">{opp['url']}</a></p>
                    <p style="font-size:0.95rem; color:#d1d5da; line-height:1.5;">{match.reasoning}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Se muestra la información de requisitos fuera del contenedor problemático
                st.markdown("**🔍 Detalles y Requisitos:**")
                if match.missing_requirements:
                    for req in match.missing_requirements:
                        st.markdown(f"<span style='font-size:0.9rem;'>- ❌ {req}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='font-size:0.9rem; color:#238636;'>✅ El perfil parece cumplir con los requisitos clave.</span>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                _, draft_col = st.columns([1, 1])
                
                # Generación de Borrador
                if draft_col.button(f"📝 Redactar Postulación #{rank}", key=f"btn_draft_{idx}"):
                    executor = ExecutorAgent()
                    with st.spinner(f"El Agente está redactando en español para #{rank}..."):
                        try:
                            draft = asyncio.run(executor.draft(
                                profile=st.session_state["profile_data"],
                                chunks=st.session_state["narrative_chunks"],
                                opportunity_content=opp["content"]
                            ))
                            st.session_state[f"draft_{idx}"] = draft
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al redactar: {e}")

                # Mostrar borrador si existe
                if f"draft_{idx}" in st.session_state:
                    st.text_area(
                        f"Borrador para #{rank}", 
                        value=st.session_state[f"draft_{idx}"], 
                        height=350,
                        key=f"area_draft_{idx}"
                    )
                    st.download_button(
                        label=f"Descargar TXT #{rank}",
                        data=st.session_state[f"draft_{idx}"],
                        file_name=f"postulacion_beca_{rank}.txt",
                        mime="text/plain",
                        key=f"dl_draft_{idx}"
                    )

# --- PIE DE PÁGINA ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    "<div style='text-align: center; font-size: 0.8rem; color: #8b949e;'>"
    "GrantHunter AI · 2026 · Powered by LangGraph & Groq<br>"
    "Design by Antigravity AI"
    "</div>", 
    unsafe_allow_html=True
)
