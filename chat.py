import re
import spacy

# Cargar modelo pre-entrenado de Spacy
nlp = spacy.load('es_core_news_md')

# Abrir archivo de conversaciones
with open('conversaciones.txt', 'r', encoding='utf-8') as f:
    conversaciones = f.read()

# Extraer mensajes de Isaac y Cristina
patron = r'\[(\d+\/\d+\/\d+,\s\d+:\d+:\d+)\]\s(Isaac|Cristina xd):\s(.+)'
mensajes = re.findall(patron, conversaciones)

# Crear diccionario de respuestas
ia_respuestas = {}
preguntas = []
for i in range(len(mensajes)-1):
    if mensajes[i][1] == 'Isaac':
        pregunta = mensajes[i][2]
        respuesta = mensajes[i+1][2]
        if pregunta not in preguntas:
            preguntas.append(pregunta)
        ia_respuestas[pregunta] = respuesta

# Bucle principal del chat
ultimas_preguntas = []
while True:
    # Leer la entrada del usuario
    entrada = input('Isaac: ')

    # Salir del bucle si el usuario escribe "adios"
    if entrada.lower() == 'adios':
        print('Cristina xd: Hasta luego, ¡que tengas un buen día!')
        break

    # Buscar la mejor respuesta entre las respuestas anteriores y la entrada actual
    entrada_doc = nlp(entrada.lower())
    mejor_respuesta = None
    mejor_puntuacion = 0
    for pregunta, respuesta in ia_respuestas.items():
        pregunta_doc = nlp(pregunta.lower())
        respuesta_doc = nlp(respuesta.lower())
        if entrada_doc.similarity(pregunta_doc) > mejor_puntuacion:
            if respuesta not in ultimas_preguntas:
                mejor_puntuacion = entrada_doc.similarity(pregunta_doc)
                mejor_respuesta = respuesta

    # Generar respuesta de la IA
    if mejor_respuesta:
        ia_entrada_doc = nlp(mejor_respuesta.lower())
        ia_respuesta = None
        for pregunta, respuesta in ia_respuestas.items():
            pregunta_doc = nlp(pregunta.lower())
            respuesta_doc = nlp(respuesta.lower())
            if ia_entrada_doc.similarity(respuesta_doc) > 0.9:
                if respuesta not in ultimas_preguntas:
                    ia_respuesta = respuesta
                    break

        # Seleccionar una respuesta similar
        if ia_respuesta:
            similar_respuestas = []
            for pregunta, respuesta in ia_respuestas.items():
                respuesta_doc = nlp(respuesta.lower())
                if ia_entrada_doc.similarity(respuesta_doc) > 0.9 and respuesta != ia_respuesta:
                    similar_respuestas.append(respuesta)

            # Mostrar la respuesta seleccionada aleatoriamente de las similares
            if similar_respuestas:
                from random import choice
                respuesta_seleccionada = choice(similar_respuestas)
            else:
                respuesta_seleccionada = ia_respuesta

        # Mostrar la respuesta generada por la IA
        else:
            respuesta_seleccionada = 'Cristina xd: Lo siento, no sé cómo responder a eso.'
    else:
        respuesta_seleccionada = 'Cristina xd: Lo siento, no sé cómo responder a eso.'
    
    # Mostrar la respuesta
    # Mostrar la respuesta
    if mejor_respuesta:
        print(f'Cristina xd: {mejor_respuesta}')
        ultimas_preguntas.append(mejor_respuesta)
        if len(ultimas_preguntas) > 5:
            ultimas_preguntas.pop(0)
    else:
        # Generar respuesta con la IA
        ia_respuesta = None
        while not ia_respuesta:
            # Leer la entrada del usuario
            entrada = input('Isaac: ')

            # Salir del bucle si el usuario escribe "adios"
            if entrada.lower() == 'adios':
                print('Cristina xd: Hasta luego, ¡que tengas un buen día!')
                break

            # Generar respuesta con la IA
            ia_respuesta = mejor_respuesta(entrada)

        # Buscar la mejor respuesta en el archivo de conversaciones
        mejor_respuesta = buscar_respuesta(ia_respuesta, conversaciones)
        if mejor_respuesta:
            print(f'Cristina xd: {mejor_respuesta}')
            ultimas_preguntas.append(mejor_respuesta)
            if len(ultimas_preguntas) > 5:
                ultimas_preguntas.pop(0)
        else:
            print('Cristina xd: Lo siento, no sé cómo responder a eso.')
            if len(ultimas_preguntas) > 0:
                with open("lecciones.txt", "a") as file:
                    file.write(f"PREGUNTA: {ultimas_preguntas[-1]}\n")
                    file.write(f"RESPUESTA: {ia_respuesta}\n")
                    file.write("\n")
                    ultimas_preguntas.pop(-1)