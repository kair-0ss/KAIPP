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

# --- PANTALLA DE CARGA BONITA ---
if 'initialized' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="loading-container">
                <div class="pulse"></div>
                <h1 style="font-family: sans-serif; font-weight: 200; margin-top: 30px; letter-spacing: 5px;">kAI</h1>
                <p style="color: #6c7086; letter-spacing: 2px;">BY: RONALDO</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3)
    st.session_state.initialized = True
    placeholder.empty()
    st.rerun()

# --- LÓGICA DE BÚSQUEDA ---
def investigar(query):
    contexto = ""
    try:
        # Wikipedia rápida
        wikipedia.set_lang("es")
        contexto += wikipedia.summary(query, sentences=2) + "\n"
    except: pass
    
    try:
        # DuckDuckGo para info fresca
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=2)]
            for r in results:
                contexto += f"\nFuente Web: {r['body']}"
    except: pass
    return contexto

# --- INTERFAZ DE USUARIO ---
st.markdown("<h2 style='text-align: center; font-weight: 200;'>¿Qué investigamos hoy?</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada de texto
if prompt := st.chat_input("Escribe tu duda aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Lo que hace única a la app: El proceso de pensamiento visible
        with st.status("🔮 Conectando con la red...", expanded=True) as status:
            st.write("Buscando en Wikipedia...")
            info = investigar(prompt)
            time.sleep(1)
            st.write("Cruzando datos web...")
            time.sleep(1)
            status.update(label="Investigación finalizada", state="complete", expanded=False)
        
        # Respuesta final construida
        if info:
            respuesta = f"Basado en mi investigación sobre **{prompt}**:\n\n{info}\n\n--- \n*Respuesta generada por kAI (By Ronaldo)*"
        else:
            respuesta = "No pude encontrar datos específicos en la red, pero cuéntame más para ayudarte."
            
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# Botón flotante para limpiar (Sidebar)
with st.sidebar:
    st.markdown("### ⚙️ Panel kAI")
    if st.button("Limpiar Memoria"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.caption("Versión Escolar 1.0")
    st.caption("Desarrollado en Venezuela")
