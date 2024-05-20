import streamlit as st
import pandas as pd
import io

def read_file(file):
    data = pd.read_csv(file, header=None, names=["Fecha", "Temperatura"])
    return data

def find_extreme_days(data):
    max_temp = data["Temperatura"].max()
    min_temp = data["Temperatura"].min()
    max_day = data[data["Temperatura"] == max_temp].iloc[0]
    min_day = data[data["Temperatura"] == min_temp].iloc[0]
    return max_day, min_day

def save_extreme_days(max_day, min_day):
    output = io.StringIO()
    output.write(f"Día de temperatura máxima: {max_day['Fecha']}, {max_day['Temperatura']:.1f}\n")
    output.write(f"Día de temperatura mínima: {min_day['Fecha']}, {min_day['Temperatura']:.1f}\n")
    return output.getvalue().encode('utf-8')

def main():
    st.title("Identificación de Días con Temperaturas Extremas")

    uploaded_file = st.file_uploader("Sube tu archivo de registro de temperaturas (TXT)", type=["txt"])

    if uploaded_file is not None:
        data = read_file(uploaded_file)
        st.write("Datos cargados:")
        st.dataframe(data)

        max_day, min_day = find_extreme_days(data)
        st.write("Días con temperaturas extremas:")
        st.write(f"Día de temperatura máxima: {max_day['Fecha']}, {max_day['Temperatura']:.1f}")
        st.write(f"Día de temperatura mínima: {min_day['Fecha']}, {min_day['Temperatura']:.1f}")

        save_button = st.button("Guardar días extremos en archivo")

        if save_button:
            output = save_extreme_days(max_day, min_day)
            st.download_button(label="Descargar días extremos",
                               data=output,
                               file_name="dias_extremos.txt",
                               mime="text/plain")
            st.success("Archivo guardado con éxito como 'dias_extremos.txt'.")

if __name__ == "__main__":
    main()