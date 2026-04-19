import streamlit as st
import requests
import xml.etree.ElementTree as ET
from styles import apply_styles

# Aplicar diseño
apply_styles()

# --- FUNCIONES DE API ---
def fetch_krdict(palabra):
    # Reemplaza con tu API KEY o usa st.secrets para mayor seguridad
    api_key = "49397A3E25C8A406FA42AEB22AB59C3B" 
    url = "https://krdict.korean.go.kr/api/search"
    params = {
        'key': api_key,
        'q': palabra,
        'translated': 'y',
        'trans_lang': 5, # 5 = Español
        'part': 'word',
        'sort': 'popular'
    }
    try:
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        resultados = []
        for item in root.findall('.//item'):
            data = {
                'word': item.find('word').text,
                'def': item.find('.//trans_dfn').text,
                'pos': item.find('pos').text
            }
            resultados.append(data)
        return resultados
    except:
        return None

# --- INTERFAZ ---
st.title("🌿 K-Vocab TrainerPro")

tab1, tab2, tab3 = st.tabs(["🗂 Aprender", "🎬 K-Drama Mode", "🏆 Ranking"])

with tab1:
    search = st.text_input("Busca una palabra para estudiar:", placeholder="Ej: 하늘 (Cielo)")
    
    if search:
        res = fetch_krdict(search)
        if res:
            for item in res[:1]: # Mostramos el resultado más popular
                st.markdown(f"""
                <div class="flashcard">
                    <p style="color: #8c7851; font-size: 14px; text-transform: uppercase;">Palabra del Diccionario</p>
                    <div class="korean-text">{item['word']}</div>
                    <p style="font-style: italic; color: #a0a0a0;">({item['pos']})</p>
                    <hr style="border: 0.5px solid #f0f0f0; margin: 20px 0;">
                    <p style="font-size: 20px; color: #2c362e;">{item['def']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🔥 Guardar en mi mazo"):
                    st.toast(f"'{item['word']}' añadida a tu racha.")
        else:
            st.error("No se encontraron resultados.")

with tab2:
    st.subheader("Modo Escucha Activa")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Video de ejemplo
    ans = st.text_input("¿Qué palabra identificaste en el segundo 0:15?")
    if st.button("Corregir"):
        st.success("¡Correcto! Has ganado 10 puntos de racha.")

with tab3:
    st.markdown("### Ranking Global")
    st.table({
        "Estudiante": ["Ji-soo", "Carlos_K", "Tu", "Elena"],
        "Racha": ["45 🔥", "30 🔥", "12 🔥", "5 🔥"],
        "Puntos": [4500, 3100, 1250, 400]
    })
    
import streamlit as st
import requests
import xml.etree.ElementTree as ET
from styles import apply_styles

# Aplicar diseño
apply_styles()

# --- FUNCIONES DE API ---
def fetch_krdict(palabra):
    # LA SIGUIENTE LÍNEA DEBE TENER 4 ESPACIOS DE SANGRÍA (INDENTACIÓN)
    if "KEYW" in st.secrets:
        api_key = st.secrets["KEYW"]
    else:
        api_key = "49397A3E25C8A406FA42AEB22AB59C3B"
    
    url = "https://krdict.korean.go.kr/api/search"
    params = {
        'key': api_key,
        'q': palabra,
        'translated': 'y',
        'trans_lang': 5, # 5 = Español
        'part': 'word',
        'sort': 'popular',
        'method': 'exact'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return None
            
        root = ET.fromstring(response.content)
        resultados = []
        
        for item in root.findall('.//item'):
            # Extraemos la definición traducida al español
            definition = "Sin definición"
            trans_res = item.find('.//trans_dfn')
            if trans_res is not None:
                definition = trans_res.text
                
            data = {
                'word': item.find('word').text if item.find('word') is not None else "N/A",
                'def': definition,
                'pos': item.find('pos').text if item.find('pos') is not None else "Sustantivo"
            }
            resultados.append(data)
        return resultados
    except Exception as e:
        return None

# --- RESTO DE LA INTERFAZ (Alineado al margen izquierdo) ---
st.title("🌿 K-Vocab TrainerPro")

tab1, tab2, tab3 = st.tabs(["🗂 Aprender", "🎬 K-Drama Mode", "🏆 Ranking"])

with tab1:
    search = st.text_input("Busca una palabra en Hangeul:", placeholder="Ej: 하늘")
    
    if search:
        res = fetch_krdict(search)
        if res:
            for item in res[:1]:
                st.markdown(f"""
                <div class="flashcard">
                    <p style="color: #8c7851; font-size: 14px; text-transform: uppercase;">Resultado Oficial</p>
                    <div class="korean-text">{item['word']}</div>
                    <p style="font-style: italic; color: #a0a0a0;">({item['pos']})</p>
                    <hr style="border: 0.5px solid #f0f0f0; margin: 20px 0;">
                    <p style="font-size: 20px; color: #2c362e;">{item['def']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No se encontraron resultados. Verifica que la búsqueda sea en coreano.")
