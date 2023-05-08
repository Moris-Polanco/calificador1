import streamlit as st
import pandas as pd
import openai
import os

# Configure the page layout
st.set_page_config(layout="wide")

# Access the OpenAI API key through an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Add a title at the beginning
st.title('Essay evaluator')

# Add instructional information
st.write('Upload an .XLSX file with your students\' essays.')

# Ask the user to upload the Excel file
archivo = st.file_uploader('Upload Excel file', type=['xlsx'])

if archivo:
    # Read the file with pandas
    data = pd.read_excel(archivo)

    # Ask the user to select the columns with the title and the essay
    columns = data.columns
    title_column = st.selectbox('Select the column that contains the titles:', columns)
    essay_column = st.selectbox('Select the column that contains the essays:', columns)

    # Add a button to start the evaluation
    if st.button('Evaluate'):
        # Get the titles and essays from the file
        titles = data[title_column].tolist()
        essays = data[essay_column].tolist()

        # Use the GPT-3 API to grade each essay
        results = []
        for i, essay in enumerate(essays):
            prompt = f"Grade the essay titled '{titles[i]}'. "
            prompt += f"Essay: {essay}. "
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None,
                timeout=5
            )
            justification = response.choices[0].text.strip()

            # Add improvement suggestions to the justification
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Suggest improvements for the essay titled '{titles[i]}'. Essay: {essay}",
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None,
                timeout=5,
            )
            suggestions = response.choices[0].text.strip()

            # Add the grade and improvement suggestions to the table
            results.append({
                'Essay': titles[i],
                'Justification': justification,
                'Improvement suggestions': suggestions,
            })

        # Show the results in a table in a pop-up
        if len(results) > 0:
            results_table = pd.DataFrame(results)
            table_html = results_table.to_html(index=False)
            st.write(f'<h2>Results:</h2>{table_html}', unsafe_allow_html=True, target='new')
        else:
            st.write("No results found")
