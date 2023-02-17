def guardar_resultados(resultados):
    # Convertimos los resultados a un dataframe de pandas
    df = pd.DataFrame(resultados)

    # Pedimos al usuario que seleccione la ubicación y el nombre del archivo
    archivo_guardado = st.file_uploader('Selecciona la ubicación y el nombre del archivo donde guardar los resultados', type=['xlsx'])

    if archivo_guardado:
        # Guardamos los resultados en un archivo Excel
        df.to_excel(archivo_guardado, index=False)

        # Mostramos un mensaje de éxito
        st.write('Los resultados se han guardado correctamente en el archivo Excel.')
        st.write('Descarga el archivo a continuación:')
        st.download_button(
            label='Descargar archivo Excel',
            data=df.to_excel(index=False, header=True),
            file_name='resultados.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
