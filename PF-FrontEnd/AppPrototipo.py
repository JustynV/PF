import streamlit as st
import pages.home as home
import pages.innerAnalysis as analysis


st.set_page_config(page_title="EasyStock",
                   page_icon=":chart_with_upwards_trend:")

st.title('Inicio')
st.header('Para acceder al modelo de análisis de sentimiento o al análisis interno, usa la sidebar a la izquierda')

