import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="kAI", 
    page_icon="⚪", 
    layout="centered"
)

# --- ESTILOS CSS (Minimalismo Extremo) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Título Estilo Zen */
    .title-container {
        text-align: center;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 100;
        letter-spacing: -2px;
        color: #000;
        margin-bottom: 0;
    }
    .by-line {
        font-size: 0.7rem;
        letter-spacing: 2px;
        color: #aaa;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# --- PANTALLA DE CARGA (BY: RONALDO) ---
if 'initialized' not in st.session_state:
    with st.empty():
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh;">
                <h1 style="font-family: sans-serif; font-weight: 100; font-size: 4rem; color: #000; margin-bottom: 0;">kAI</h1>
                <p style="font-family: sans-serif; letter-spacing: 3px; color: #888; font-size: 0.8rem;">BY: RONALDO</p>
                <div style="margin-top: 20px; width: 30px; height: 30px; border: 1px solid #eee; border-top: 1px solid #000; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            </div>
            <style> @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } } </style>
            """, unsafe_allow_html=True
        )
        time.sleep(2.5)
        st.session_state.initialized = True
    st.rerun()

# --- CONFIGURACIÓN API ---
# Recuerda poner tu clave en los Secrets de Streamlit con el nombre GOOGLE_API_KEY
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configura la API Key en los Secrets.")
    st.stop()

# --- INTERFAZ ---
st.markdown('<div class="title-container"><p class="main-title">kAI</p><p class="by-line">By Ronaldo</p></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes
for message in st.session_state.messages:
    avatar = "⚪" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Escribe tu duda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚪"):
        placeholder = st.empty()
        full_response = ""
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            full_response += chunk.text
            placeholder.markdown(full_response + " ▪️")
        
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Instrucciones de instalación en el Sidebar
with st.sidebar:
    st.title("Instalación")
    st.info("Para usar como app: En iPhone pulsa 'Compartir' > 'Añadir a pantalla de inicio'. En Android pulsa los 3 puntos > 'Instalar aplicación'.")
