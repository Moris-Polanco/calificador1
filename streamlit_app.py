import os
import openai
import streamlit as st
import pandas as pd

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

# Si se subió un archivo, lo procesamos
if archivo:
    # Leemos el archivo con pandas
    data = pd.read_excel(archivo)

    # Obtenemos los ensayos de la columna especificada en el archivo
    columna_ensayos = st.selectbox('Selecciona la columna que contiene los ensayos:', data.columns)
    ensayos = data[columna_ensayos].tolist()

    # Pedimos al usuario que ingrese los parámetros de calificación
    parametro_1 = st.slider('Parámetro 1', min_value=0, max_value=10, step=1)
    parametro_2 = st.slider('Parámetro 2', min_value=0, max_value=10, step=1)
    parametro_3 = st.slider('Parámetro 3', min_value=0, max_value=10, step=1)

    # Utilizamos la API de GPT-3 para calificar cada ensayo
    resultados = []
    for ensayo in ensayos:
        prompt = f"Califica este ensayo: {ensayo}. Parámetro 1: {parametro_1}, Parámetro 2: {parametro_2}, Parámetro 3: {parametro_3}"
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
