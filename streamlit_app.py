import os
import openai
import streamlit as st
import pandas as pd

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

# Pedimos al usuario que defina los criterios de calificación
st.write('Defina los criterios de calificación:')
criterios = []
i = 0
while True:
    criterio = st.text_input(f'Criterio {i}:', key=f'criterio_{i}')
    i += 1
    if criterio == '':
        break
    criterios.append(criterio)

# Si se subió un archivo, lo procesamos
if archivo:
    # Leemos el archivo con pandas
    data = pd.read_excel(archivo)

    # Obtenemos los ensayos de la columna especificada en el archivo
    columna_ensayos = st.selectbox('Selecciona la columna que contiene los ensayos:', data.columns)
    ensayos = data[columna_ensayos].tolist()

    # Pedimos al usuario que valore cada criterio
    valores_criterios = {}
    for criterio in criterios:
        valor = st.slider(f'¿Qué tan importante es el criterio {criterio}?', min_value=1, max_value=10, step=1)
        valores_criterios[criterio] = valor

    # Utilizamos la API de GPT-3 para calificar cada ensayo
    resultados = []
    for ensayo in ensayos:
        prompt = f"Califica este ensayo: {ensayo}. "
        for criterio in criterios:
            peso = valores_criterios[criterio]
            prompt += f"{criterio}: {peso}, "
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=60,
        )
        calificacion = response.choices[0].text.strip()
        resultados.append(calificacion)

    # Mostramos los resultados en una tabla
    st.write('Resultados:')
    tabla = {'Ensayo': ensayos, 'Calificación': resultados}
    st.table(tabla)
