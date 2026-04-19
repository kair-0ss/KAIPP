import random

def generar_ensayo_unico(tema, texto_investigado):
    if len(texto_investigado) < 50:
        return f"Lo siento, Ronaldo, no encontré suficiente información sobre '{tema}' para redactar un ensayo digno."

    # Dividimos el texto en oraciones reales
    oraciones = [o.strip() for o in texto_investigado.split('.') if len(o) > 30]
    random.shuffle(oraciones)

    # Estructura Dinámica
    intros = [
        f"El estudio de {tema} representa un desafío intelectual en la era moderna.",
        f"Hablar de {tema} es adentrarse en un mundo de descubrimientos constantes.",
        f"Pocas cosas han impactado tanto nuestra visión actual como lo ha hecho {tema}."
    ]
    
    conector = ["Además,", "Por otra parte,", "En este sentido,", "Resulta interesante que"]
    
    # Construcción del cuerpo usando las oraciones reales investigadas
    cuerpo = ""
    for i in range(min(len(oraciones), 3)):
        cuerpo += f"{random.choice(conector)} {oraciones[i].lower()}. "

    ensayo = f"""
### {tema.upper()}
{random.choice(intros)}

{cuerpo}

En conclusión, este análisis demuestra que {tema} seguirá siendo un tema de debate y estudio. 
___
*Documento generado exclusivamente por kAI para Ronaldo.*
"""
    return ensayo
