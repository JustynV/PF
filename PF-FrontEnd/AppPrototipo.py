import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import plotly.graph_objects as go

st.set_page_config(page_title="EasyStock", page_icon=":chart_with_upwards_trend:")


load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = "stock"

@st.cache_resource
def get_database():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db


@st.cache_data
def fetch_data(collection_name):
    db = get_database()
    collection = db[collection_name]
    data = list(collection.find())
    return data

@st.cache_data
def fetch_collection_names():
    db = get_database()
    collection_names = db.list_collection_names()
    return collection_names


st.title('EasyStock')

st.header('Bienvenido al sistema de análisis del mercado')

import pandas as pd

stocks = fetch_collection_names()

stock = st.selectbox(
    '¿Qué Stock quieres analizar?',
    stocks)



if st.button('Analizar'):
    result = fetch_data(stock)
    vals = {}
    for doc in result:
        vals = {key: value for key, value in doc.items() if key != '_id'}

    df = pd.DataFrame.from_dict(vals, orient='index')
    df = df.astype(float)
    st.write('Ahora analizando:', stock)
    trace = go.Candlestick(
        x=df.index,
        open=df['1. open'],
        high=df['2. high'],
        low=df['3. low'],
        close=df['4. close'],
        name='Candlestick'
    )

    layout = go.Layout(
        title=f'Valores de {stock}',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        hovermode='x'
    )

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig)






