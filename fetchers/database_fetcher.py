import pandas as pd
import datetime
import streamlit as st
from sqlalchemy import create_engine
from pymongo import MongoClient

def fetch_data_from_db(connection_string, query, db_type, collection_name=None):
    try:
        if db_type == "MongoDB":
            client = MongoClient(connection_string)
            db = client.get_database()
            collection = db[collection_name]
            data = pd.DataFrame(list(collection.find()))
            if "_id" in data.columns:
                data.drop("_id", axis=1, inplace=True)
        else:
            engine = create_engine(connection_string)
            data = pd.read_sql(query, engine)
        data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return data
    except Exception as e:
        st.error(f"Błąd bazy danych: {e}")
        return pd.DataFrame()
