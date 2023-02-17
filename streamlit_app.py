import streamlit as st
import pandas as pd
import openai
import os

# Ocultar los detalles del archivo cargado en Streamlit
st.set_option('deprecation.showfileUploaderEncoding', False)

# Activar el wide mode
st.set_page_config(layout="wide")

api_key = st.sidebar.text_input("API Key", type="password")

# Usar el cache de Streamlit
@st.cache
def process_prompt(input, api_key):
    model_prediction = openai.Completion.create(
        engine="text-davinci-003",
        prompt=input,
        temperature=0,
        max_tokens=512,
        n=1,
        stop=None,
        api_key=api_key
    )
    return model_prediction.choices[0].text.strip()

if api_key:
    st.title('Evaluador de ensayos')
    st.write('Suba un archivo .XLSX con los ensayos de sus alumnos. Máximo: 10 ensayos.')

    st.sidebar.title('Herramientas de evaluación')
    st.sidebar.write('Ingrese su API Key de OpenAI para poder utilizar esta herramienta:')

    if st.button('Evaluar'):
        archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

        if archivo:
            data = pd.read_excel(archivo)

            columnas = data.columns
            columna_titulo = st.selectbox('Selecciona la columna que contiene los títulos:', columnas)
            columna_ensayo = st.selectbox('Selecciona la columna que contiene los ensayos:', columnas)

            titulos = data[columna_titulo].head(10).tolist()
            ensayos = data[columna_ensayo].head(10).tolist()

            resultados = []
            for i, ensayo in enumerate(ensayos):
                prompt = f"Califica el ensayo titulado '{titulos[i]}'. Ensayo: {ensayo}."
                justificacion = process_prompt(prompt, api_key)

                prompt = f"Sugiere mejoras para el ensayo titulado '{titulos[i]}'. Ensayo: {ensayo}."
                sugerencias = process_prompt(prompt, api_key)

                resultados.append({
                    'Ensayo': titulos[i],
                    'Justificación': justificacion,
                    'Sugerencias de mejora': sugerencias,
                })

            st.write('Resultados:')
            tabla = pd.DataFrame(resultados)
            st.table(tabla)

            nombre_archivo = 'resultados.xlsx'
            tabla.to_excel(nombre_archivo, index=False)
            st.download_button(
            label='Descargar resultados en Excel',
            data=open(nombre_archivo, 'rb').read(),
            file_name=nombre_archivo,
            mime='application/vnd.ms-excel')
