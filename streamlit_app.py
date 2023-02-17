import streamlit as st
import pandas as pd
import openai
import streamlit.secrets as secrets

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = secrets["openai_api_key"]

# Agregamos un título al principio
st.title('Evaluador de ensayos')

# Agregamos información en una columna a la izquierda
st.sidebar.subheader('Instrucciones')
st.sidebar.markdown('Suba un archivo .XLSX con los ensayos de sus alumnos.')
st.sidebar.subheader('Autor')
st.sidebar.markdown('Moris Polanco')

# Pedimos al usuario y contraseña
usuario = st.sidebar.text_input('Usuario')
contrasena = st.sidebar.text_input('Contraseña', type='password')

# Validamos el usuario y contraseña
if usuario != secrets["usuario"] or contrasena != secrets["contrasena"]:
    st.error('Usuario o contraseña incorrectos. Inténtalo de nuevo.')
else:
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
                engine="text-davinci-002",
                prompt=prompt,
                temperature=0.5,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60,
            )
            justificacion = response.choices[0].text.strip()

            resultados.append({'Ensayo': titulos[i], 'Justificación': justificacion})

        # Mostramos los resultados en una tabla
        st.write('Resultados:')
        tabla = pd.DataFrame(resultados)
        st.table(tabla)
import streamlit as st
import pandas as pd
import openai
import streamlit.secrets as secrets

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = secrets["openai_api_key"]

# Agregamos un título al principio
st.title('Evaluador de ensayos')

# Agregamos información en una columna a la izquierda
st.sidebar.subheader('Instrucciones')
st.sidebar.markdown('Suba un archivo .XLSX con los ensayos de sus alumnos.')
st.sidebar.subheader('Autor')
st.sidebar.markdown('Moris Polanco')

# Pedimos al usuario y contraseña
usuario = st.sidebar.text_input('Usuario')
contrasena = st.sidebar.text_input('Contraseña', type='password')

# Validamos el usuario y contraseña
if usuario != secrets["usuario"] or contrasena != secrets["contrasena"]:
    st.error('Usuario o contraseña incorrectos. Inténtalo de nuevo.')
else:
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
                engine="text-davinci-002",
                prompt=prompt,
                temperature=0.5,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60,
            )
            justificacion = response.choices[0].text.strip()

            resultados.append({'Ensayo': titulos[i], 'Justificación': justificacion})

        # Mostramos los resultados en una tabla
        st.write('Resultados:')
        tabla = pd.DataFrame(resultados)
        st.table(tabla)
