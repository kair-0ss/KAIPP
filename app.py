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

# --- CONFIGURACIÓN HUGGING FACE ---
# Pon tu token en los Secrets de Streamlit como: HF_TOKEN
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.markdown('<p class="main-title">kAI</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Escribe algo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        output = query({"inputs": f"<s>[INST] {prompt} [/INST]", "parameters": {"max_new_tokens": 500}})
        try:
            # Extraer solo el texto de la respuesta
            res_text = output[0]['generated_text'].split('[/INST]')[-1]
            st.markdown(res_text)
            st.session_state.messages.append({"role": "assistant", "content": res_text})
        except:
            st.error("Espera un momento, el modelo se está despertando...")
