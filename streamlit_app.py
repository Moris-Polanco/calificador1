import os
import openai
import streamlit as st
import pandas as pd

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Agregamos información en una columna a la izquierda
st.sidebar.title('Calificador de ensayos')
st.sidebar.subheader('Instrucciones')
st.sidebar.markdown('Suba un archivo .XLSX con los ensayos de sus alumnos y especifique qué columna contiene los ensayos. Defina los criterios de calificación.')
st.sidebar.subheader('Autor')
st.sidebar.markdown('Moris Polanco')

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

# Definimos los criterios de evaluación
criterios = ['Ortografía', 'Argumentación']

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
        prompt = f"Califica este ensayo. Ortografía: {valores_criterios['Ortografía']}. Argumentación: {valores_criterios['Argumentación']}. Ensayo: {ensayo}."
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
        nota_ortografia = int(justificacion.split("Ortografía:")[1].split(".")[0].strip())
        nota_argumentacion = int(justificacion.split("Argumentación:")[1].split(".")[0].strip())
        nota_total = nota_ortografia * valores_criterios['Ortografía'] + nota_argumentacion * valores_criterios['Argumentación']
        resultados.append({'Calificación': nota_total, 'Justificación': justificacion})

    # Mostramos los resultados en una tabla
    st.write('Resultados:')
    tabla = pd.DataFrame(resultados)
    st.table(tabla)
