import streamlit as st
import pandas as pd
import openai
import os

# Configure OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

if not api_key:
    st.warning("Please enter a valid API key to continue.")
else:
    openai.api_key = api_key

# Set page layout
st.set_page_config(layout="wide")

# Add a description in the left column
st.sidebar.write("""
# Essay Evaluator
This is an application that uses OpenAI's GPT-3 API to evaluate essays. Upload an .XLSX file containing your students' essays and select the columns that contain the titles and essays. Then, click the "Evaluate" button to obtain the grade for each essay. In this essay evaluator tool, students can write their essays in a Google Form, which can be shared with the class. The teacher can then convert the form responses into an Excel sheet, which can be uploaded to the evaluator. This makes it easy for teachers to evaluate multiple essays quickly and efficiently. Once the Excel sheet is uploaded, the tool uses OpenAI's GPT-3 API to provide a justification for each essay, as well as suggestions for improvement. The results are displayed in a pop-up table, which can be used by the teacher to grade the essays and provide feedback to the students. This tool is a great way to streamline the essay grading process and make it more efficient for teachers and students alike.
""")

# Upload Excel file
archivo = st.file_uploader('Upload Excel file', type=['xlsx'])

if archivo:
    # Read Excel file using pandas
    data = pd.read_excel(archivo)

    # Ask the user to select the columns for titles and essays
    columnas = data.columns
    columna_titulo = st.selectbox('Select the column containing the titles:', columnas)
    columna_ensayo = st.selectbox('Select the column containing the essays:', columnas)

    # Add a button to start the evaluation
    if st.button('Evaluate'):
        # Get the titles and essays from the file
        titulos = data[columna_titulo].tolist()
        ensayos = data[columna_ensayo].tolist()

        # Use the GPT-3 API to grade each essay
        resultados = []
        for i, ensayo in enumerate(ensayos):
            prompt = f"Grade the essay titled '{titulos[i]}'. "
            prompt += f"Essay: {ensayo}. "
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

            # Add improvement suggestions to the justification
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Suggest improvements for the essay titled '{titulos[i]}'. Essay: {ensayo}",
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None,
                timeout=5,
            )
            sugerencias = response.choices[0].text.strip()

            # Add the grade and improvement suggestions to the table
            resultados.append({
                'Essay': titulos[i],
                'Justification': justificacion,
                'Improvement suggestions': sugerencias,
            })

        # Show the results in a table in a pop-up
        if len(resultados) > 0:
            tabla_resultados = pd.DataFrame(resultados)
            tabla_html = tabla_resultados.to_html(index=False)
            st.write(f'<h2>Results:</h2>{tabla_html}', unsafe_allow_html=True, target='new')
        else:
            st.write("No results found")
