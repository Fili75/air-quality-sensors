import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("Air quality sensors")
data_input = st.selectbox("Sensore",["CT2", "CT3","CT6","CT8"])
if (f"data_{data_input}" not in st.session_state):
    d = pd.read_csv(f"./data/data_{data_input}.csv",sep=";")
    d["timestamp"] = pd.to_datetime(d["timestamp"])
    st.session_state[f"data_{data_input}"] = d
if f"data_{data_input}_date_min" not in st.session_state:
    st.session_state[f"data_{data_input}_date_min"] = datetime.strptime(st.session_state[f"data_{data_input}"]["timestamp"].min().strftime("%Y/%m/%d"),"%Y/%m/%d")
if "date_max" not in st.session_state:
    st.session_state[f"data_{data_input}_date_max"] = datetime.strptime(st.session_state[f"data_{data_input}"]["timestamp"].max().strftime("%Y/%m/%d"),"%Y/%m/%d")

date_min_input = st.date_input("data inizio", value = st.session_state[f"data_{data_input}_date_min"], min_value= st.session_state[f"data_{data_input}_date_min"], max_value= st.session_state[f"data_{data_input}_date_max"])
date_max_input = st.date_input("data fine", value = st.session_state[f"data_{data_input}_date_max"], min_value= st.session_state[f"data_{data_input}_date_min"], max_value= st.session_state[f"data_{data_input}_date_max"])
date_max_input = date_max_input + timedelta(days=1)
ind = (st.session_state[f"data_{data_input}"]["timestamp"] >= str(date_min_input)) & (st.session_state[f"data_{data_input}"]["timestamp"] <= str(date_max_input))
type_data = st.selectbox("tipo dati", options = ["PM2.5", "PM10", "Tutti"])
freq = st.selectbox("frequenza", options = ["Nessuna","Oraria", "Giornaliera", "Settimanale", "Mensile"],index=3)
freq_dict = {
    "Oraria": "H",
    "Giornaliera":"D",
    "Settimanale": "W",
    "Mensile": "M"
}

fig, ax = plt.subplots(1,1)

if type_data == "Tutti":
    for i in ["PM2.5", "PM10"]:
        d1 = st.session_state[f"data_{data_input}"].loc[(st.session_state[f"data_{data_input}"]["Parametro"] == i) & ind]
        if freq != "Nessuna":
            d1 = d1[["timestamp", "Valore"]].groupby(pd.Grouper(key="timestamp", freq= freq_dict[freq])).mean().reset_index()

        ax.plot(d1["timestamp"], d1["Valore"], label = i)
    ax.legend(labelcolor="w")
else:
    d1 = st.session_state[f"data_{data_input}"].loc[(st.session_state[f"data_{data_input}"]["Parametro"] == type_data) & ind]
    if freq != "Nessuna":
        d1 = d1[["timestamp", "Valore"]].groupby(pd.Grouper(key="timestamp", freq=freq_dict[freq])).mean().reset_index()
    ax.plot(d1["timestamp"], d1["Valore"], label =type_data)
    ax.legend(labelcolor = "w")

st.plotly_chart(fig)
