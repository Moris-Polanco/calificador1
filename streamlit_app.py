import streamlit as st
import pandas as pd
import openai
import os

# Ocultar los detalles del archivo cargado en Streamlit
st.set_option('deprecation.showfileUploaderEncoding', False)

# Activar el wide mode
st.set_page_config(layout="wide")

api_key = st.sidebar.text_input("APIkey", type="password")
  # Using the streamlit cache
@st.cache
def process_prompt(input):

  return pred.model_prediction(input=input.strip() , api_key=api_key)

  if api_key:

    # Agregamos un título al principio
    st.title('Evaluador de ensayos')

    # Agregamos información de instrucciones
    st.write('Suba un archivo .XLSX con los ensayos de sus alumnos. Máximo: 10 ensayos.')

    # Añadimos la columna de la izquierda con el título, descripción y caja de API Key
    st.sidebar.title('Herramientas de evaluación')
    st.sidebar.write('Ingrese su API Key de OpenAI para poder utilizar esta herramienta:')
    api_key = st.sidebar.text_input('API Key')

    # Verificar si se ingresó una API Key válida
    if api_key:
        try:
            # Activar la API Key de OpenAI
            openai.api_key = api_key

            # Crear una variable de estado para verificar si el usuario ya ha cargado un archivo
            if 'archivo_cargado' not in st.session_state:
                st.session_state.archivo_cargado = False

            # Pedimos al usuario que suba el archivo Excel
            if not st.session_state.archivo_cargado:
                archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

                if archivo:
                    # Leemos el archivo con pandas
                    data = pd.read_excel(archivo)

                    # Pedimos al usuario que seleccione las columnas con el título y el ensayo
                    columnas = data.columns
                    columna_titulo = st.selectbox('Selecciona la columna que contiene los títulos:', columnas)
                    columna_ensayo = st.selectbox('Selecciona la columna que contiene los ensayos:', columnas)

                    # Agregamos un botón para iniciar la evaluación
                    if st.button('Evaluar'):
                        # Obtenemos los títulos y los ensayos del archivo
                        titulos = data[columna_titulo].head(10).tolist()
                        ensayos = data[columna_ensayo].head(10).tolist()

                        # Utilizamos la API de GPT-3 para calificar cada ensayo
                        resultados = []
                        for i, ensayo in enumerate(ensayos):
                            prompt = f"Califica el ensayo titulado '{titulos[i]}'. "
                            prompt += f"Ensayo: {ensayo}. "
                            response = openai.Completion.create(
                                engine="text-davinci-003",
                                prompt=prompt,
                                temperature=0,
                                max_tokens=512,
                                n=1,
                                stop=None
                            )
                            justificacion = response.choices[0].text.strip()

                            # Agregamos sugerencias de mejora a la justificación
                            response = openai.Completion.create(
                                engine="text-davinci-003",
                                prompt=f"Sugiere mejoras para el ensayo titulado '{titulos[i]}'. Ensayo: {ensayo}",
                                temperature=0,
                                max_tokens=512,
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

                    # Guardar los resultados en un archivo de Excel
                    nombre_archivo = 'resultados.xlsx'
                    tabla.to_excel(nombre_archivo, index=False)

                    # Descargar el archivo de Excel
                    st.download_button(
                        label='Descargar resultados en Excel',
                        data=open(nombre_archivo, 'rb').read(),
                        file_name=nombre_archivo,
                        mime='application/vnd.ms-excel'
                    )

                  
