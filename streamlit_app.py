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

# Agregamos información de instrucciones
st.write('Suba un archivo .XLSX con los ensayos de sus alumnos.')

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

       # Agregamos un botón para guardar los resultados en un archivo CSV
        if st.button('Guardar resultados'):
            guardar_resultados(resultados)

def guardar_resultados(resultados):
    # Convertimos los resultados a un dataframe de pandas
    df = pd.DataFrame(resultados)

    # Pedimos al usuario que seleccione la ubicación y el nombre del archivo
    archivo_guardado = st.file_uploader('Selecciona la ubicación y el nombre del archivo donde guardar los resultados', type=['csv'])

    if archivo_guardado:
        # Guardamos los resultados en un archivo CSV
        with open(archivo_guardado.name, 'w') as f:
            df.to_csv(f, index=False)
            
# Agregamos un botón para guardar los resultados en un archivo CSV
st.download_button(
    label='Descargar resultados como archivo CSV',
    data=tabla.to_csv(index=False),
    file_name='resultados.csv',
    mime='text/csv'
)
