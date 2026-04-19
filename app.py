import streamlit as st
import google.generativeai as genai
import time
from streamlit_pwa import pwa_manifest # Librería para compatibilidad móvil

# --- CONFIGURACIÓN DE PÁGINA (Estilo Zen/Minimalista) ---
st.set_page_config(
    page_title="kAI", 
    page_icon="⚪", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURACIÓN PWA (Para instalar en celular) ---
# Esto crea el archivo que el celular necesita para reconocer la app
pwa_manifest(
    name="kAI Asistente Zen",
    short_name="kAI",
    description="Tu asistente minimalista potenciado por Gemini.",
    icon_url="https://raw.githubusercontent.com/Ronaldo-Dev/kai-chatbot/main/icon.png", # Reemplaza por una URL de icono real si tienes una
    theme_color="#000000",
    background_color="#FFFFFF"
)

# --- ESTILOS CSS PERSONALIZADOS (Super Minimalista) ---
st.markdown("""
    <style>
    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fondo y tipografía general */
    .stApp {
        background-color: #fdfdfd;
        color: #1a1a1a;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Estilo del Chat */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Avatar de kAI (Minimalista) */
    .stChatMessage[data-testid="stChatMessageAssistant"] .stAvatar {
        background-color: #1a1a1a !important;
        color: white !important;
    }

    /* Título minimalista */
    .main-title {
        font-size: 2.5rem;
        font-weight: 200;
        text-align: center;
        margin-bottom: 0rem;
        letter-spacing: -1px;
        color: #000;
    }
    .subtitle {
        font-size: 0.9rem;
        font-weight: 300;
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
    
    /* Input de chat centrado y limpio */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 1px solid #eee !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- PANTALLA DE CARGA (Minimalista - BY: RONALDO) ---
if 'initialized' not in st.session_state:
    with st.empty():
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh;">
                <div style="font-size: 3rem; font-weight: 100; letter-spacing: -2px; color: #000;">kAI</div>
                <div style="font-size: 0.8rem; font-weight: 300; color: #aaa; margin-top: 10px;">BY: RONALDO</div>
                <div class="loader"></div>
            </div>
            <style>
                .loader {
                    margin-top: 30px;
                    border: 1px solid #eee;
                    border-top: 1px solid #000;
                    border-radius: 50%;
                    width: 25px;
                    height: 25px;
                    animation: spin 1.5s linear infinite;
                }
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
            """, unsafe_allow_html=True
        )
        time.sleep(2.5) # Un poco más rápido
        st.session_state.initialized = True
    st.rerun()

# --- SEGURIDAD Y CONFIGURACIÓN DE API ---
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Por favor, configura GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- BARRA LATERAL (Para instrucciones de instalación) ---
with st.sidebar:
    st.markdown("### 📱 Instalar kAI en tu Celular")
    st.markdown("""
        Esta app funciona como una Web App Progresiva (PWA). Para tenerla como una app nativa:
        
        **En Android (Chrome):**
        1. Toca el menú de 3 puntos (⋮).
        2. Toca **"Instalar aplicación"** o **"Agregar a pantalla principal"**.
        
        **En iOS (Safari):**
        1. Toca el botón **"Compartir"** (cuadrado con flecha hacia arriba).
        2. Desplázate hacia abajo y toca **"Agregar a inicio"**.
    """)
    st.markdown("---")
    st.caption("kAI v1.0 | By Ronaldo")

# --- CUERPO PRINCIPAL ---
st.markdown('<div class="main-title">kAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asistente Zen</div>', unsafe_allow_html=True)

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con avatares minimalistas
for message in st.session_state.messages:
    avatar = "⚪" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant", avatar="⚪"):
        msg_placeholder = st.empty()
        full_res = ""
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Stream de respuesta
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    # Un cursor minimalista
                    msg_placeholder.markdown(full_res + "⚡")
            
            # Respuesta final sin cursor
            msg_placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"Error de conexión.")
            # st.error(str(e)) # Descomenta para debuggear
