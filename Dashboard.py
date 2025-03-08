import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

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

day_df = pd.read_csv("https://raw.githubusercontent.com/Pragiptalrs/Belajar-Analisis-Data-dengan-Python/refs/heads/main/day_data.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/Pragiptalrs/Belajar-Analisis-Data-dengan-Python/refs/heads/main/hour_data.csv")

st.set_page_config(layout="wide")
st.header('Bike Sharing Dashboard 🚴‍♂️')

with st.sidebar:
    st.image("https://raw.githubusercontent.com/Pragiptalrs/Belajar-Analisis-Data-dengan-Python/main/Gambar%20Sepeda.png")

start_date, end_date = st.date_input(
    label="Rentang Waktu",
    min_value=day_df["dteday"].min().date(),  
    max_value=day_df["dteday"].max().date(),
    value=[
        day_df["dteday"].min().date(),
        day_df["dteday"].max().date()
    ]
)

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

day_df_filtered = day_df[(day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)]
hour_df_filtered = hour_df[(hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)]
day_df_filtered = clustering_kategori(day_df_filtered)

col1, col2 = st.columns(2)

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

    st.subheader('Heatmap Penyewaan Berdasarkan Jam dan Hari')
    fig, ax = plt.subplots(figsize=(10, 4))
    hourly_weekday_trend = hour_df_filtered.pivot_table(values="cnt", index="weekday", columns="hr", aggfunc="mean")
    sns.heatmap(hourly_weekday_trend, cmap="coolwarm", annot=False, ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Hari")
    ax.set_yticklabels(["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
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

    st.subheader('Pola Penyewaan Berdasarkan Jam')
    fig, ax = plt.subplots(figsize=(6, 3))
    hourly_trend = hour_df_filtered.groupby('hr').agg({'cnt': 'mean'}).reset_index()
    sns.lineplot(x='hr', y='cnt', data=hourly_trend, marker='o', ax=ax)
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

    st.subheader('Distribusi Kategori Penyewaan')
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.countplot(x=day_df_filtered["Kategori"], palette="coolwarm", order=["Low Demand", "Medium Demand", "High Demand"], ax=ax)
    ax.set_xlabel("Kategori Penyewaan")
    ax.set_ylabel("Jumlah Hari")
    st.pyplot(fig)

    st.subheader('Distribusi Suhu Berdasarkan Kategori Penyewaan')
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.boxplot(x="Kategori", y="temp", data=day_df_filtered, order=["Low Demand", "Medium Demand", "High Demand"], palette="coolwarm", ax=ax)
    ax.set_xlabel("Kategori Penyewaan")
    ax.set_ylabel("Suhu")
    st.pyplot(fig)

st.subheader('Clustering Penyewaan Sepeda Berdasarkan Kelembaban')
fig, ax = plt.subplots(figsize=(10, 4))
sns.scatterplot(x=day_df_filtered["hum"], y=day_df_filtered["cnt"], hue=day_df_filtered["Kategori"], palette="coolwarm", ax=ax)
ax.set_xlabel("Kelembaban")
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.caption('Copyright © pragiptaseptyaningrumlarasati 2025')
