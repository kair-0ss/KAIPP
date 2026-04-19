import streamlit as st
import time
import requests
from duckduckgo_search import DDGS
import wikipedia

# --- CONFIGURACIÓN E INNOVACIÓN VISUAL ---
st.set_page_config(page_title="kAI | Intelligence", page_icon="✨", layout="centered")

# CSS para una interfaz única tipo "Glassmorphism"
st.markdown("""
    <style>
    /* Fondo principal oscuro profundo */
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2e, #11111b);
        color: #cdd6f4;
    }
    
    /* Personalización del Chat Input */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent !important;
    }
    
    .stChatInputContainer > div {
        background-color: #1e1e2e !important;
        border: 1px solid #45475a !important;
        border-radius: 25px !important;
    }

    /* Burbujas de chat únicas */
    .stChatMessage {
        background-color: #181825 !important;
        border: 1px solid #313244 !important;
        border-radius: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Animación del Loader */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
    }
    .pulse {
        width: 80px;
        height: 80px;
        background: #89b4fa;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(137, 180, 250, 0.7);
        animation: pulse-blue 2s infinite;
    }
    @keyframes pulse-blue {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(137, 180, 250, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(137, 180, 250, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(137, 180, 250, 0); }
    }
    </style>
""", unsafe_allow_html=True)
import streamlit as st
import time
import motores_busqueda 
import herramientas      

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="kAI | Unificado", page_icon="🤖")

# (Mantenemos el CSS anterior de modo oscuro y pantalla de carga)

st.title("🤖 kAI v2.0")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- PROCESAMIENTO DEL MENSAJE ---
if prompt := st.chat_input("Dime algo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        saludos = ["hola", "buenos dias", "buenas tardes", "que tal", "quien eres"]
        
        # 1. RESPUESTA A SALUDOS
        if any(s in p_low for s in saludos):
            respuesta = "¡Hola! Soy **kAI**, tu asistente de investigación desarrollado por **Ronaldo**. Puedo buscar en Wikipedia, la web y artículos científicos para redactar ensayos o resúmenes únicos. ¿En qué puedo ayudarte hoy?"
            st.markdown(respuesta)
            st.session_state.messages.append({"role": "assistant", "content": respuesta})

        # 2. GENERACIÓN DE ENSAYO / INVESTIGACIÓN ÚNICA
        elif "ensayo" in p_low or "redacta" in p_low or "investiga" in p_low:
            tema = p_low.replace("ensayo", "").replace("redacta", "").replace("investiga", "").strip()
            
            with st.status(f"Generando respuesta unificada sobre {tema}...") as s:
                st.write("Consultando múltiples motores...")
                # USAMOS LA NUEVA FUNCIÓN UNIFICADA
                info_total = motores_busqueda.buscar_y_unificar(tema)
                
                st.write("Sintetizando información única...")
                if "ensayo" in p_low:
                    resultado = herramientas.generar_ensayo_unico(tema, info_total)
                else:
                    resultado = herramientas.generar_resumen_dinamico(info_total)
                
                s.update(label="Análisis completado", state="complete")
            
            # Efecto de escritura pro
            area = st.empty()
            txt = ""
            for char in resultado:
                txt += char
                area.markdown(txt)
                time.sleep(0.003)
            st.session_state.messages.append({"role": "assistant", "content": resultado})

        # 3. RESPUESTA POR DEFECTO
        else:
            with st.spinner("Buscando en la red..."):
                info = motores_busqueda.buscar_y_unificar(prompt)
                res = f"Aquí tienes una síntesis de lo que encontré:\n\n{info[:700]}..." if info else "No tengo info sobre eso."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
