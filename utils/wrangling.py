from io import BytesIO
import pandas as pd 
import requests 
import streamlit as st
from datetime import timedelta

CACHE_DURATION = timedelta(hours=24)
URL = st.secrets["EDA_DATA_URL"]

@st.cache_resource(ttl=CACHE_DURATION, show_spinner=True, max_entries=10)
def load_eda_data():
    response = requests.get(URL).content
    df = pd.read_csv(BytesIO(response))

    df = df.rename(columns={
        "mean_temp_2m": "Mean Temperature",
        "humidity_2m": "Humidity",
        "total_rain": "Rainfall",
        "enso_status": "ENSO"
    })

    return df

def dataset_info(df):
    df_1 = df.drop(columns=["Unnamed: 0"], errors="ignore")
    summary = pd.DataFrame([{
        "Column": col,
        "Count": df_1[col].count(),
        "Type": df_1[col].dtype
    } for col in df_1.columns])

    summary["Type"] = summary["Type"].astype(str)
    return summary

def enso_status_decoder(oni_index):
    if oni_index == 0:
        return "Neutral"
    elif oni_index == 1:
        return "Weak La Niña"
    elif oni_index == 2:
        return "Moderate La Niña"
    elif oni_index == 3:
        return "Strong La Niña"
    elif oni_index == 4:
        return "Very Strong La Niña"
    elif oni_index == 5:
        return "Weak El Niño"
    elif oni_index == 6:
        return "Moderate El Niño"
    elif oni_index == 7:
        return "Strong El Niño"
    elif oni_index == 8:
        return "Very Strong El Niño"
    else:
        return "Unknown"