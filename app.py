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
from duckduckgo_search import DDGS
import wikipedia
import herramientas # Tu archivo con la lógica única

# ... (Configuración de página, CSS y pantalla de carga se mantienen igual) ...

# --- FUNCIÓN DE INVESTIGACIÓN ---
def investigar(query):
    contexto = ""
    try:
        wikipedia.set_lang("es")
        contexto += wikipedia.summary(query, sentences=3) + "\n"
    except: pass
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            for r in results: contexto += r['body'] + " "
    except: pass
    return contexto

# --- INTERFAZ DE CHAT ---
st.title("🤖 kAI")
st.caption("Investigación y Redacción Automática")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de usuario
if prompt := st.chat_input("¿Qué necesitas? (Ej: Hazme un ensayo sobre la Luna)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower()
        
        # 1. DETECCIÓN DE INTENCIÓN: ¿Quiere un ensayo?
        if "ensayo" in p_low or "redacta" in p_low:
            tema = p_low.replace("hazme un ensayo sobre", "").replace("ensayo sobre", "").replace("haz un ensayo de", "").strip()
            
            with st.status(f"Generando ensayo único sobre {tema}...", expanded=True) as s:
                info = investigar(tema)
                st.write("Analizando fuentes y mezclando ideas...")
                resultado = herramientas.generar_ensayo_unico(tema, info)
                s.update(label="Ensayo redactado con éxito", state="complete")
            
            # Efecto de escritura
            area = st.empty()
            acumulado = ""
            for letra in resultado:
                acumulado += letra
                area.markdown(acumulado)
                time.sleep(0.002)
            st.session_state.messages.append({"role": "assistant", "content": resultado})

        # 2. DETECCIÓN DE INTENCIÓN: ¿Quiere un resumen?
        elif "resume" in p_low or "resumen" in p_low:
            tema = p_low.replace("resume", "").replace("resumen de", "").strip()
            with st.spinner("Sintetizando información..."):
                info = investigar(tema)
                resultado = herramientas.generar_resumen_dinamico(info)
                st.markdown(resultado)
                st.session_state.messages.append({"role": "assistant", "content": resultado})

        # 3. RESPUESTA NORMAL (Búsqueda simple)
        else:
            with st.spinner("Buscando información..."):
                info = investigar(prompt)
                if info:
                    res = f"He encontrado esto para ti:\n\n{info[:500]}..."
                else:
                    res = "No encontré datos específicos, ¿puedes ser más detallado?"
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
