import streamlit as st
import pandas as pd
import openai
import os

# Configuramos el diseño de la página
st.set_page_config(layout="wide")

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Agregamos un título al principio
st.title('Evaluador de ensayos')

# Agregamos información de instrucciones en la columna izquierda
st.sidebar.title('Instrucciones')
st.sidebar.write('1. Pida a sus alumnos que escriban un ensayo en un Google Forms.')
st.sidebar.write('2. Convierta el formulario en una hoja de cálculo con al menos dos columnas: Autor y Ensayo.')
st.sidebar.write('3. Cargue la hoja de cálculo a la aplicación de Streamlit.')
st.sidebar.write('4. Haga clic en Evaluar y espere los resultados.')

# Pedimos al usuario que suba el archivo Excel
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
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None,
                timeout=5
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
                timeout=5,
            )
            sugerencias = response.choices[0].text.strip()

            # Agregamos la calificación y las sugerencias de mejora a la tabla
            resultados.append({
                'Ensayo': titulos[i],
                'Justificación': justificacion,
                'Sugerencias de mejora': sugerencias,
            })

        # Mostramos los resultados en una tabla en un pop up
        if len(resultados) > 0:
            tabla_resultados = pd.DataFrame(resultados)
            tabla_html = tabla_resultados.to_html(index=False)
            st.write(f'<h2>Resultados:</h2>{tabla_html}', unsafe_allow_html=True, target='new')
        else:
            st.write("No se encontraron resultados")
