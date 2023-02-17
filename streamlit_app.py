import os
import openai
import streamlit as st
import pandas as pd

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Agregamos información en una columna a la izquierda
st.sidebar.title('Calificador de ensayos')
st.sidebar.subheader('Instrucciones')
st.sidebar.markdown('Suba un archivo .XLSX con los ensayos de sus alumnos y especifique qué columna contiene los ensayos.')
st.sidebar.subheader('Autor')
st.sidebar.markdown('Moris Polanco')

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

# Si se subió un archivo, lo procesamos
if archivo:
    # Leemos el archivo con pandas
    data = pd.read_excel(archivo)

    # Obtenemos los ensayos de la columna especificada en el archivo
    columna_ensayos = st.selectbox('Selecciona la columna que contiene los ensayos:', data.columns)
    ensayos = data[columna_ensayos].tolist()

    # Utilizamos la API de GPT-3 para calificar cada ensayo
    resultados = []
    for ensayo in ensayos:
        st.write(f'Ensayo: {ensayo}')
        nota = st.number_input('Asigna una nota del 1 al 10:', min_value=1, max_value=10, step=1)
        justificacion = st.text_input('Justificación de la nota:')
        resultados.append({'Calificación': nota, 'Justificación': justificacion})

    # Mostramos los resultados en una tabla
    st.write('Resultados:')
    tabla = pd.DataFrame(resultados)
    st.table(tabla)
