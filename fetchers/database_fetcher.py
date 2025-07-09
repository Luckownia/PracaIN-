import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from pymongo import MongoClient

def fetch_data_from_db(connection_string, query, db_type, collection_name=None):
    try:
        if db_type == "MongoDB":
            if not collection_name:
                st.error("Musisz podać nazwę kolekcji MongoDB!")
                return pd.DataFrame()

            client = MongoClient(connection_string)
            db = client.get_database()
            collection = db[collection_name]
            data = pd.DataFrame(list(collection.find()))

            if "_id" in data.columns:
                data.drop("_id", axis=1, inplace=True)
        else:
            engine = create_engine(connection_string)
            data = pd.read_sql(query, engine)

        if "timestamp" in data.columns:
            data["timestamp"] = pd.to_datetime(data["timestamp"])
            data["timestamp"] = data["timestamp"].dt.round("1s")
            data = data.sort_values("timestamp")

        return data
    except Exception as e:
        print(e)
        st.error(f"Błąd bazy danych: {e}")
        return pd.DataFrame()
