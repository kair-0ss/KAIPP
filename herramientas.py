import random

def generar_ensayo_unico(tema, texto_investigado):
    if len(texto_investigado) < 50:
        return f"Lo siento, Ronaldo, no encontré suficiente información sobre '{tema}' para un ensayo."

    oraciones = [o.strip() for o in texto_investigado.split('.') if len(o) > 30]
    random.shuffle(oraciones)

    intros = [
        f"El estudio de {tema} representa un desafío intelectual en la era moderna.",
        f"Hablar de {tema} es adentrarse en un mundo de descubrimientos constantes.",
        f"Pocas cosas han impactado tanto nuestra visión actual como lo ha hecho {tema}."
    ]
    
    conector = ["Además,", "Por otra parte,", "En este sentido,", "Resulta interesante que"]
    
    cuerpo = ""
    # Usamos máximo 3 oraciones de la investigación para el cuerpo
    for i in range(min(len(oraciones), 3)):
        cuerpo += f"{random.choice(conector)} {oraciones[i].lower()}. "

    return f"""## 📜 Ensayo: {tema.upper()}
{random.choice(intros)}

{cuerpo}

En conclusión, este análisis demuestra que {tema} seguirá siendo un pilar fundamental para el entendimiento de nuestra realidad actual.
___
*ID de Redacción única: {random.randint(1000, 9999)} | By Ronaldo*"""

def generar_resumen_dinamico(texto_investigado):
    """Esta es la función que daba el error. Asegúrate que el nombre sea idéntico."""
    if not texto_investigado:
        return "No hay datos para resumir."
    
    ideas = [i.strip() for i in texto_investigado.split('.') if len(i) > 25]
    # Seleccionamos 4 puntos al azar para que sea único
    puntos_clave = random.sample(ideas, min(len(ideas), 4))
    
    resumen = "### 💡 Puntos Clave Extraídos\n"
    for p in puntos_clave:
        resumen += f"* {p}\n"
    return resumen
