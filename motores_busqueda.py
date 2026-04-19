import wikipedia
from duckduckgo_search import DDGS
import requests

def buscar_y_unificar(tema):
    datos = []
    # 1. Wikipedia
    try:
        wikipedia.set_lang("es")
        datos.append(f"WIKIPEDIA: {wikipedia.summary(tema, sentences=3)}")
    except: pass

    # 2. Web (DuckDuckGo)
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(tema, max_results=3):
                datos.append(f"WEB: {r['body']}")
    except: pass

    # 3. ArXiv (Científico)
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{tema}&max_results=1"
        res = requests.get(url).text
        if "<summary>" in res:
            resumen = res.split("<summary>")[1].split("</summary>")[0].strip()
            datos.append(f"CIENCIA: {resumen[:400]}")
    except: pass

    return "\n\n".join(datos)
