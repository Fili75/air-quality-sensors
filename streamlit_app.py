import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.title("Air quality sensors")
if ("data" not in st.session_state):
    d = pd.read_csv("data_CT2.csv",decimal=",")
    d["timestamp"] = pd.to_datetime(d["timestamp"])
    st.session_state["data"] = d
if "date_min" not in st.session_state:
    st.session_state["date_min"] = datetime.strptime(st.session_state["data"]["timestamp"].min().strftime("%Y/%m/%d"),"%Y/%m/%d")
if "date_max" not in st.session_state:
    st.session_state["date_max"] = datetime.strptime(st.session_state["data"]["timestamp"].max().strftime("%Y/%m/%d"),"%Y/%m/%d")

print(st.session_state["date_min"])

date_min_input = st.date_input("data inizio", value = st.session_state["date_min"], min_value= st.session_state["date_min"], max_value= st.session_state["date_max"])
date_max_input = st.date_input("data fine", value = st.session_state["date_max"], min_value= st.session_state["date_min"], max_value= st.session_state["date_max"])
ind = (st.session_state["data"]["timestamp"] >= str(date_min_input)) & (st.session_state["data"]["timestamp"] <= str(date_max_input))
type_data = st.selectbox("tipo dati", options = ["PM2.5", "PM10", "Tutti"])
freq = st.selectbox("frequenza", options = ["Nessuna","Oraria", "Giornaliera", "Settimanale", "Mensile"])
freq_dict = {
    "Oraria": "H",
    "Giornaliera":"D",
    "Settimanale": "W",
    "Mensile": "M"
}

fig, ax = plt.subplots(1,1)

if type_data == "Tutti":
    for i in ["PM2.5", "PM10"]:
        d1 = st.session_state["data"].loc[(st.session_state["data"]["Parametro"] == i) & ind]
        if freq != "Nessuna":
            d1 = d1[["timestamp", "Valore"]].groupby(pd.Grouper(key="timestamp", freq= freq_dict[freq])).mean().reset_index()

        ax.plot(d1["timestamp"], d1["Valore"], label = i)
    ax.legend(labelcolor="w")
else:
    d1 = st.session_state["data"].loc[(st.session_state["data"]["Parametro"] == type_data) & ind]
    if freq != "Nessuna":
        d1 = d1[["timestamp", "Valore"]].groupby(pd.Grouper(key="timestamp", freq=freq_dict[freq])).mean().reset_index()
    ax.plot(d1["timestamp"], d1["Valore"], label =type_data)
    ax.legend(labelcolor = "w")

st.plotly_chart(fig)
