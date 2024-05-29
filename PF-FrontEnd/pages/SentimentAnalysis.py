import pandas as pd
import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import plotly.graph_objects as go


load_dotenv()
st.set_page_config(page_title="EasyStock Análisis Sentimientos",
                   page_icon="imgs/EasyStockS2.jpg")

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = "stock"

def get_all_news_dates(collection_name):
    db = get_database()
    dates = db[collection_name].find({}, {"date": 1, "_id": 0})
    return [news['date'] for news in dates]

def get_news_by_date(date, collection_name):
    db = get_database()
    date_str = date.strftime("%Y-%m-%d")
    news = list(db[collection_name].find({"date": date_str}, {"_id": 0, "article": 1, "sentiment": 1}))
    return news


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


stocks = fetch_collection_names()

stock = st.selectbox(
    '¿Qué Stock quieres analizar?',
    [stock for stock in stocks if "Sentimientos" not in stock])


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

    fig1 = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig1)

    collection_name = f"Sentimientos {stock.title()}"


    if(collection_name in stocks):
        data_from_db = fetch_data(collection_name)
        df_nlp = pd.DataFrame(data_from_db)
        df_nlp['date'] = pd.to_datetime(df_nlp['date'])
        df_nlp = df_nlp.sort_values(by='date')

        fecha_minima = df_nlp['date'].min()
        fecha_maxima = pd.Timestamp.now()
        df['date'] = pd.to_datetime(df.index)
        df = df[[
            'date', '1. open', '2. high', '3. low', '4. close', '5. volume']]
        df = df.sort_values(by='date')

        df_candlestick_filtered = df.loc[(
            df['date'] >= fecha_minima) & (df['date'] <= fecha_maxima)]

        min_price = df_candlestick_filtered['1. open'].min()
        max_price = df_candlestick_filtered['1. open'].max()
        df_candlestick_filtered['normalized_price'] = 2 * ((df_candlestick_filtered['1. open'] - min_price) / (max_price - min_price)) - 1

        min_sentiment = df_nlp['sentiment'].min()
        max_sentiment = df_nlp['sentiment'].max()
        df_nlp['normalized_sentiment'] = 2 * ((df_nlp['sentiment'] - min_sentiment) / (max_sentiment - min_sentiment)) - 1

        window_size = 10
        df_nlp['smoothed_sentiment'] = df_nlp['normalized_sentiment'].rolling(window=window_size, min_periods=1).mean()
        df_LR = df_nlp[df_nlp['revista'] == "larepublica.co"]
        df_PF = df_nlp[df_nlp['revista'] == "portafolio.co"]
        
        trace_price = go.Scatter(
            x=df_candlestick_filtered['date'],
            y=df_candlestick_filtered['normalized_price'],
            mode='lines',
            name='Precio de la acción (Normalizado)',
            hoverinfo='x+y',
        )

        trace_sentiment = go.Scatter(
            x=df_nlp['date'],
            y=df_nlp['smoothed_sentiment'],
            mode='lines',
            name=f'Sentimientos NLP (Promedio Móvil, Ventana={window_size})',
            hoverinfo='x+y',
        )

        trace_larepublica = go.Scatter(
            x=df_LR['date'],
            y=df_LR['smoothed_sentiment'],
            mode='lines',
            name=f'Sentimientos NLP (La República)(Promedio Móvil, Ventana={window_size})',
            hoverinfo='x+y',
        )

        trace_portafolio = go.Scatter(
            x=df_PF['date'],
            y=df_PF['smoothed_sentiment'],
            mode='lines',
            name=f'Sentimientos NLP (Portafolio.co)(Promedio Móvil, Ventana={window_size})',
            hoverinfo='x+y',
        )

        # Crear el layout con el rango ajustado
        layout = go.Layout(
            title='Precios de la acción y Sentimientos de las noticias normalizados a lo largo del tiempo',
            xaxis=dict(title='Fecha'),
            yaxis=dict(title='Valor Normalizado', range=[-1, 1]),
            hovermode='closest',
        )

        fig2 = go.Figure(data=[trace_price, trace_sentiment, trace_larepublica, trace_portafolio], layout=layout)
        st.plotly_chart(fig2)


        