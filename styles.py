import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Fondo y tipografía general */
        .stApp {
            background-color: #fdfcfb;
            color: #2c362e;
        }
        
        /* Contenedor de Flashcards */
        .flashcard {
            background: white;
            padding: 40px;
            border-radius: 25px;
            border: 1px solid #e0d7cc;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.02);
            margin: 20px 0;
        }
        
        /* Texto en Coreano */
        .korean-text {
            font-size: 55px;
            font-weight: 800;
            color: #4a5d4e;
            margin-bottom: 5px;
        }
        
        /* Botones estilo tierra */
        .stButton>button {
            background-color: #8c7851 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 10px 20px !important;
            width: 100%;
        }

        /* Estilo para inputs */
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 1px solid #d9ccbc;
        }
        
        /* Tabs personalizadas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #f7f3f0;
            padding: 10px;
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)
