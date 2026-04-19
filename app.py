import streamlit as st
import requests
import time

st.set_page_config(page_title="kAI - Presentación", page_icon="🤖")

# --- CSS MINIMALISTA ---
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    .main-title { font-size: 3rem; font-weight: 100; text-align: center; color: #000; }
    footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)

# --- PANTALLA DE CARGA ---
if 'init' not in st.session_state:
    with st.empty():
        st.markdown(f"<div style='text-align:center;margin-top:20vh;'><h1>kAI</h1><p>BY: RONALDO</p></div>", unsafe_allow_html=True)
        time.sleep(2)
        st.session_state.init = True
    st.rerun()

import streamlit as st
import requests
import time

# ... (Configuración de página y CSS se mantienen igual) ...

# --- CONFIGURACIÓN HUGGING FACE ---
# Asegúrate de tener HF_TOKEN en los Secrets de Streamlit
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def query(payload):
    # Intentamos hasta 3 veces por si el modelo está despertando
    for _ in range(3):
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            return response.json()
        except:
            # Si no es JSON, esperamos 5 segundos y reintentamos
            time.sleep(5)
    return None

# --- CUERPO DEL CHAT ---
if prompt := st.chat_input("Escribe algo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("kAI está pensando..."):
            data = query({
                "inputs": f"<s>[INST] {prompt} [/INST]",
                "parameters": {"max_new_tokens": 500, "wait_for_model": True} # <--- IMPORTANTE
            })
            
            if data and isinstance(data, list) and 'generated_text' in data[0]:
                res_text = data[0]['generated_text'].split('[/INST]')[-1].strip()
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            elif data and 'error' in data:
                st.error(f"El modelo se está cargando. Por favor, espera 20 segundos y vuelve a intentar. (Error: {data['error']})")
            else:
                st.error("Lo siento, hubo un problema de conexión con el servidor. Inténtalo de nuevo.")
