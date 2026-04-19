import random
from datetime import datetime
import pytz

def generar_ensayo_unico(tema, info):
    if len(info) < 50: return "No hay info suficiente para un ensayo."
    oraciones = [o.strip() for o in info.split('.') if len(o) > 30]
    random.shuffle(oraciones)
    
    intros = [f"El impacto de {tema} es innegable hoy.", f"Analizar {tema} nos permite entender el futuro."]
    cuerpo = ". ".join(oraciones[:3])
    
    return f"## 📜 ENSAYO: {tema.upper()}\n{random.choice(intros)}\n\n{cuerpo}.\n\n*Redactado por kAI (ID: {random.randint(100,999)})*"

def generar_resumen_dinamico(info):
    puntos = [i.strip() for i in info.split('.') if len(i) > 25]
    res = "### 💡 PUNTOS CLAVE\n"
    for p in random.sample(puntos, min(len(puntos), 4)):
        res += f"* {p}\n"
    return res

def resolver_mates(exp):
    try:
        f = exp.replace("mas","+").replace("menos","-").replace("por","*").replace("entre","/")
        problema = "".join(c for c in f if c in "0123456789+-*/().")
        return eval(problema)
    except: return None

def obtener_recomendacion():
    h = datetime.now().hour
    if h < 12: return "🌅 Mañana productiva: ¡Prioriza tus tareas hoy!"
    if h < 18: return "☀️ Tarde activa: No olvides hidratarte mientras investigas."
    return "🌙 Noche de relax: Buen momento para leer tus ensayos generados."

def traducir_auto(texto, idioma):
    dic = {
        "en": {"hi": "Hello! I'm kAI.", "bye": "Success in your research!"},
        "ko": {"hi": "안녕하세요! kAI입니다.", "bye": "행운을 빕니다!"}
    }
    if idioma in dic:
        return f"{dic[idioma]['hi']}\n\n{texto}\n\n{dic[idioma]['bye']}"
    return texto
