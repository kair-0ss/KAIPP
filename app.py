import streamlit as st
import time
from datetime import datetime
import pytz
import motores_busqueda as mb
import herramientas as hr

# --- CONFIGURACIÓN DARK PREMIUM ---
st.set_page_config(page_title="kAI Ultra", page_icon="⚡")
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a2e, #16161d); color: white; }
    .stChatInputContainer { padding-bottom: 20px; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- PANTALLA DE CARGA ---
if 'ready' not in st.session_state:
    with st.empty():
        st.markdown("<div style='text-align:center;margin-top:35vh;'><h1 style='letter-spacing:10px;font-weight:100;'>kAI</h1><p>BY: RONALDO</p></div>", unsafe_allow_html=True)
        time.sleep(2.5)
    st.session_state.ready = True
    st.rerun()

# --- LÓGICA DEL CHAT ---
st.title("⚡ kAI Intelligence")

if "messages" not in st.session_state: st.session_state.messages = []
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        p = prompt.lower()
        res = ""
        idioma = "en" if any(x in p for x in ["hello", "how", "what"]) else "ko" if any(x in p for x in ["안녕", "시간"]) else "es"

        # 1. SALUDOS
        if any(s in p for s in ["hola", "buenos", "quien eres", "hello", "안녕"]):
            res = "¡Hola! Soy kAI, tu asistente multifuncional creado por Ronaldo. Investigo, redacto ensayos, resuelvo mates y hablo idiomas."

        # 2. MATEMÁTICAS
        elif any(c in p for c in "0123456789") and any(op in p for op in ["+","-","*","/","cuanto"]):
            mate = hr.resolver_mates(p)
            res = f"🔢 Resultado: **{mate}**" if mate else "No pude calcular eso."

        # 3. HORA MUNDIAL
        elif "hora en" in p:
            zona = "Europe/Madrid" if "madrid" in p else "Asia/Tokyo" if "tokio" in p else "America/New_York" if "york" in p else "America/Caracas"
            h = datetime.now(pytz.timezone(zona)).strftime("%H:%M:%S")
            res = f"🕒 Hora en esa zona: **{h}**"

        # 4. RECOMENDACIÓN
        elif "recomienda" in p or "que hago" in p:
            res = hr.obtener_recomendacion()

        # 5. INVESTIGACIÓN / ENSAYO / LISTAS
        else:
            with st.status("🔍 Investigando en múltiples fuentes...") as s:
                info = mb.buscar_y_unificar(p)
                if "ensayo" in p:
                    res = hr.generar_ensayo_unico(p, info)
                elif "lista" in p or "resumen" in p:
                    res = hr.generar_resumen_dinamico(info)
                else:
                    res = f"Análisis rápido:\n\n{info[:600]}..."
                s.update(label="Proceso completado", state="complete")

        # TRADUCCIÓN Y SALIDA
        res = hr.traducir_auto(res, idioma)
        
        # Efecto escritura
        area = st.empty()
        curr = ""
        for c in res:
            curr += c
            area.markdown(curr)
            time.sleep(0.002)
        st.session_state.messages.append({"role": "assistant", "content": res})
