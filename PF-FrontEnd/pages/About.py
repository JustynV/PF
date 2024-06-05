import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

st.header("Métricas de los datos")

data = {
    'Stock': ['Avianca', 'Avianca', 'Avianca', 'Bancolombia', 'Bancolombia', 'Bancolombia',
              'Cementos Argos', 'Cementos Argos', 'Cementos Argos', 'Ecopetrol', 'Ecopetrol', 'Ecopetrol',
              'Grupo Aval', 'Grupo Aval', 'Grupo Aval', 'Tecnoglass', 'Tecnoglass', 'Tecnoglass'],
    'Model': ['Linear Regression', 'Decision Tree', 'Random Forest', 'Linear Regression', 'Decision Tree', 'Random Forest',
              'Linear Regression', 'Decision Tree', 'Random Forest', 'Linear Regression', 'Decision Tree', 'Random Forest',
              'Linear Regression', 'Decision Tree', 'Random Forest', 'Linear Regression', 'Decision Tree', 'Random Forest'],
    'MSE': [0.0182, 0.0097, 0.0048, 16.3785, 27.7908, 19.1536, 6.2585, 7.6595, 5.0359, 3.8022, 5.8736, 3.1108,
            0.5459, 1.1955, 0.5340, 17.3586, 25.8200, 16.9108],
    'R2': [0.1505, 0.5456, 0.7736, 0.8718, 0.7826, 0.8501, 0.9158, 0.8970, 0.9323, 0.7902, 0.6759, 0.8283,
           0.9010, 0.7832, 0.9031, 0.7802, 0.6731, 0.7859]
}

df = pd.DataFrame(data)


color_map = {
    'Linear Regression': '#FFFF80',
    'Decision Tree': '#ED5AB3',
    'Random Forest': '#1640D6'
}

fig_r2 = make_subplots(rows=1, cols=1, subplot_titles=('R2 por Modelo y Stock',))

for model in df['Model'].unique():
    fig_r2.add_trace(
        go.Bar(
            x=df[df['Model'] == model]['Stock'],
            y=df[df['Model'] == model]['R2'],
            name=model,
            marker_color=color_map[model]
        ),
        row=1, col=1
    )

fig_r2.update_layout(
    template='plotly', 
    height=600, width=600,
    legend_title_text='Modelo',
    legend=dict(
        x=1.05,
        y=1,
        traceorder='normal',
        font=dict(
            size=12,
        ),
    ),
    xaxis=dict(tickangle=45)
)

fig_r2.update_xaxes(title_text="Stock", row=1, col=1)
fig_r2.update_yaxes(title_text="R2", row=1, col=1)

fig_mse = make_subplots(rows=1, cols=1, subplot_titles=('MSE por Modelo y Stock',))

for model in df['Model'].unique():
    fig_mse.add_trace(
        go.Bar(
            x=df[df['Model'] == model]['Stock'],
            y=df[df['Model'] == model]['MSE'],
            name=model,
            marker_color=color_map[model],
        ),
        row=1, col=1
    )

fig_mse.update_layout(
    template='plotly', 
    height=600, width=600,
    legend_title_text='Modelo',
    legend=dict(
        x=1.05,
        y=1,
        traceorder='normal',
        font=dict(
            size=12,
        ),
    ),
    xaxis=dict(tickangle=45)
)

fig_mse.update_xaxes(title_text="Stock", row=1, col=1)
fig_mse.update_yaxes(title_text="MSE", row=1, col=1)

st.plotly_chart(fig_r2)
st.plotly_chart(fig_mse)
