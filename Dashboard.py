import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from datetime import datetime

sns.set(style='dark')

# Load dataset safely
def load_data():
    if os.path.exists("day_data.csv") and os.path.exists("hour_data.csv"):
        day_df = pd.read_csv("day_data.csv")
        hour_df = pd.read_csv("hour_data.csv")
    else:
        st.error("File CSV tidak ditemukan. Pastikan file day_data.csv dan hour_data.csv tersedia.")
        return None, None
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

# Function to categorize rental demand
def categorize_demand(cnt):
    if cnt < 3000:
        return "Low Demand"
    elif 3000 <= cnt <= 6000:
        return "Medium Demand"
    else:
        return "High Demand"

def clustering_kategori(df):
    df['Kategori'] = df['cnt'].apply(categorize_demand)
    return df

# Load data
day_df, hour_df = load_data()
if day_df is None or hour_df is None:
    st.stop()

st.set_page_config(layout="wide")
st.header('Bike Sharing Dashboard 🚴‍♂️')

# Sidebar
with st.sidebar:
    if os.path.exists("Gambar Sepeda.png"):
        st.image("Gambar Sepeda.png")
    else:
        st.warning("Gambar tidak ditemukan")
    
    # Ensure min and max values are in correct format
    min_date = day_df["dteday"].min().date()
    max_date = day_df["dteday"].max().date()
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Convert date inputs
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data
day_df_filtered = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]
hour_df_filtered = hour_df[(hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)]
day_df_filtered = clustering_kategori(day_df_filtered)

col1, col2 = st.columns(2)

# Visualizations
with col1:
    st.subheader('Total Penyewaan Harian')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(day_df_filtered['dteday'], day_df_filtered['cnt'], marker='o', linewidth=2, color='#90CAF9')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Rentals')
    st.pyplot(fig)

    st.subheader('Persentase Penyewaan Berdasarkan Cuaca')
    fig, ax = plt.subplots(figsize=(6, 3))
    weather_trend = day_df_filtered.groupby("weathersit")["cnt"].mean().reset_index()
    weather_trend["weathersit"] = weather_trend["weathersit"].map({1: "Cerah", 2: "Mendung", 3: "Hujan"})
    ax.pie(weather_trend["cnt"], labels=weather_trend["weathersit"], autopct="%1.1f%%", colors=["#D6E4F0", "#EED3C6", "#DA9075"])
    st.pyplot(fig)

with col2:
    st.subheader('Performa Penyewaan Berdasarkan Musim')
    fig, ax = plt.subplots(figsize=(6, 3))
    seasonal_trend = day_df_filtered.groupby("season")["cnt"].mean().reset_index()
    seasonal_trend["season"] = seasonal_trend["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
    sns.barplot(x='season', y='cnt', data=seasonal_trend, palette='coolwarm', ax=ax)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

st.subheader('Clustering Penyewaan Sepeda Berdasarkan Kelembaban')
fig, ax = plt.subplots(figsize=(10, 4))
sns.scatterplot(x=day_df_filtered["hum"], y=day_df_filtered["cnt"], hue=day_df_filtered["Kategori"], palette="coolwarm", ax=ax)
ax.set_xlabel("Kelembaban")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.caption('Copyright © pragiptaseptyaningrumlarasati 2025')
