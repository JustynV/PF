import streamlit as st

st.title("Acerca del proyecto")

st.header("¿Quienes somos?")

st.write("EasyStock es un proyecto educativo el cuál busca hacer un análisis a profundidad sobre cómo el sentimiento general respecto a una empresa puede afectar el valor de sus acciones en el mercado de la bolsa de Valores")

st.header("¿Cual es nuestro objetivo?")
st.write("El objetivo principal es proporcionar a inversores, agentes del mercado e individuos por igual, una herramienta sólida e informativa que les permita analizar datos de manera coherente y organizada en lo que es considerado entorno volátil y competitivo como lo es la bolsa de valores.")


st.header("¿Qué tecnologías usamos?")

st.markdown("""
El lenguaje de programación principal es Python y manejamos diversas librerías tales como:
- Beautiful Soup (bs4): Manejo de Webscrapping
- Pymongo: Manejo de MongoDB con Python
- Pandas: manipulación y análisis de datos
- Pysentimiento: Herramienta de análisis de sentimientos
- Json: Manejo de datos recibidos de la DB.
- Streamlit: Despliegue y visualización de datos
""")


st.write("Adicional a esto, almacenamos la información en nuestra propia base de datos de MongoDB Atlas")