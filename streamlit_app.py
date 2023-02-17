import streamlit as st
import pandas as pd
import openai
import os

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Agregamos un título al principio
st.title('Evaluador de ensayos')

# Agregamos información en una columna a la izquierda
st.sidebar.subheader('Instrucciones')
st.sidebar.markdown('Suba un archivo .XLSX con los ensayos de sus alumnos.')
st.sidebar.subheader('Autor')
st.sidebar.markdown('Moris Polanco')

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

# Si se subió un archivo, lo procesamos
if archivo:
    # Leemos el archivo con pandas
    data = pd.read_excel(archivo)

    # Pedimos al usuario que seleccione las columnas con el título y el ensayo
    columnas = data.columns
    columna_titulo = st.selectbox('Selecciona la columna que contiene los títulos:', columnas)
    columna_ensayo = st.selectbox('Selecciona la columna que contiene los ensayos:', columnas)

    # Obtenemos los títulos y los ensayos del archivo
    titulos = data[columna_titulo].tolist()
    ensayos = data[columna_ensayo].tolist()

    # Utilizamos la API de GPT-3 para calificar cada ensayo
    resultados = []
    for i, ensayo in enumerate(ensayos):
        prompt = f"Califica el ensayo titulado '{titulos[i]}'. "
        prompt += f"Ensayo: {ensayo}. "
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=60,
        )
        justificacion = response.choices[0].text.strip()

        # Agregamos sugerencias de mejora a la justificación
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Sugiere mejoras para el ensayo titulado '{titulos[i]}'. Ensayo: {ensayo}",
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=60,
        )
        sugerencias = response.choices[0].text.strip()

        # Agregamos la calificación y las sugerencias de mejora a la tabla
        resultados.append({
            'Ensayo': titulos[i],
            'Justificación': justificacion,
            'Sugerencias de mejora': sugerencias,
        })

    # Mostramos los resultados en una tabla
    st.write('Resultados:')
    tabla = pd.DataFrame(resultados)
    st.table(tabla)
