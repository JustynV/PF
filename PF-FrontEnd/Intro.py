import streamlit as st
import os
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = "stock"

@st.cache_resource
def get_database():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db

@st.cache_data
def fetch_stockAmounts():
    db = get_database()
    collection_names = db.list_collection_names()
    collection_counts = {}
    for collection_name in collection_names:
        if "Sentimientos" not in collection_name:  
            collection = db[collection_name]
            document = collection.find_one()
            document['_id'] = str(document['_id'])
            collection_counts[collection_name] = len(document)
    return collection_counts

@st.cache_data
def fetch_sentimentAmounts():
    db = get_database()
    collection_names = db.list_collection_names()
    collection_counts = {}
    for collection_name in collection_names:
        if "Sentimientos" in collection_name:  
            collection = db[collection_name]
            count = collection.count_documents({})
            collection_counts[collection_name] = count
    return collection_counts

st.set_page_config(page_title="EasyStock",
                   page_icon="imgs/EasyStockS2.jpg")


st.title('Inicio')

st.header('Para acceder al modelo de análisis de sentimiento o al análisis interno, usa la sidebar a la izquierda')

st.title("Datos actuales")

stocks_counts = fetch_stockAmounts()
sentiments_count = fetch_sentimentAmounts()

df1 = pd.DataFrame(list(stocks_counts.items()), columns=['Collection', 'Count'])
df2 = pd.DataFrame(list(sentiments_count.items()), columns=['Collection', 'Count'])

fig1 = px.pie(df1, names='Collection', values='Count', title='Proporciones de datos de Stock')
fig2 = px.pie(df2, names='Collection', values='Count', title='Proporciones de datos de análisis de sentimientos')

st.plotly_chart(fig1)
st.plotly_chart(fig2)

st.title("Referencias a librerías usadas")


