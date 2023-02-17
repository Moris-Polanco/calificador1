# Importamos las librerías necesarias
import openai
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticamos con la API de Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('ruta/al/archivo/credenciales.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Nombre de la hoja de cálculo').sheet1
data = sheet.get_all_values()

# Obtenemos los ensayos de la hoja de cálculo
ensayos = [fila[0] for fila in data]

# Pedimos al usuario que ingrese los parámetros de calificación
parametro_1 = st.slider('Parámetro 1', min_value=0, max_value=10, step=1)
parametro_2 = st.slider('Parámetro 2', min_value=0, max_value=10, step=1)
parametro_3 = st.slider('Parámetro 3', min_value=0, max_value=10, step=1)

# Utilizamos la API de GPT-3 para calificar cada ensayo
openai.api_key = "API_KEY_DE_GPT-3"

resultados = []
for ensayo in ensayos:
    prompt = f"Califica este ensayo: {ensayo}. Parámetro 1: {parametro_1}, Parámetro 2: {parametro_2}, Parámetro 3: {parametro_3}"
    response = openai.Completion.create(
        engine="text-davinci-002",
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
