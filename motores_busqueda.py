import wikipedia
from duckduckgo_search import DDGS
import requests

def buscar_y_unificar(tema):
    """Consulta múltiples fuentes y arma un solo bloque de información"""
    datos_unificados = []
    
    # 1. Wikipedia
    try:
        wikipedia.set_lang("es")
        datos_unificados.append(f"Resumen enciclopédico: {wikipedia.summary(tema, sentences=3)}")
    except: pass

    # 2. Web (DuckDuckGo)
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(tema, max_results=3):
                datos_unificados.append(f"Dato web: {r['body']}")
    except: pass

    # 3. ArXiv (Académico)
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{tema}&max_results=1"
        res = requests.get(url).text
        if "<summary>" in res:
            resumen = res.split("<summary>")[1].split("</summary>")[0].strip()
            datos_unificados.append(f"Contexto científico: {resumen[:400]}")
    except: pass

    # Unimos todo con saltos de línea
    return "\n\n".join(datos_unificados)
