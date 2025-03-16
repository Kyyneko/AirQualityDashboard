import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import os
from streamlit_folium import folium_static

# Fungsi untuk menggabungkan semua dataset dalam folder 'data/'
@st.cache_data
def load_data():
    folder_path = "data/"
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    df_list = []
    for file in files:
        df_temp = pd.read_csv(os.path.join(folder_path, file))
        df_list.append(df_temp)

    df = pd.concat(df_list, ignore_index=True)

    # Konversi ke datetime
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])

    # Hapus kolom yang tidak diperlukan
    drop_cols = ["year", "month", "day", "hour", "No"]
    df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

    return df

# Load dataset
df = load_data()

# Sidebar: Pilih stasiun
st.sidebar.title("Filter Data")
station_selected = st.sidebar.selectbox("Pilih Stasiun", df["station"].unique())

# Filter data berdasarkan stasiun
df_filtered = df[df["station"] == station_selected]

# Header aplikasi
st.title("Dashboard Analisis Kualitas Udara")
st.write(f"Menampilkan data dari stasiun **{station_selected}**")

# Visualisasi Tren PM2.5
st.subheader("Tren PM2.5 dari Tahun ke Tahun")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_filtered["datetime"], df_filtered["PM2.5"], label="PM2.5", color='red')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Konsentrasi PM2.5")
ax.legend()
st.pyplot(fig)

# Statistik Deskriptif
def descriptive_stats(data, column):
    return {
        "Rata-rata": data[column].mean(),
        "Minimum": data[column].min(),
        "Maksimum": data[column].max()
    }

st.subheader("Statistik Deskriptif Polutan")
polutan = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
st.dataframe(pd.DataFrame({
    p: descriptive_stats(df_filtered, p) for p in polutan
}).T)

# Opsi untuk menampilkan polutan lain
st.subheader("Visualisasi Polutan Lain")
polutan_selected = st.selectbox("Pilih Polutan", polutan)
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_filtered["datetime"], df_filtered[polutan_selected], label=polutan_selected, color='blue')
ax2.set_xlabel("Tanggal")
ax2.set_ylabel(f"Konsentrasi {polutan_selected}")
ax2.legend()
st.pyplot(fig2)

# Menampilkan lokasi dengan polutan tertinggi
st.subheader("Peta Lokasi dengan PM2.5 Tertinggi")

# Kelompokkan data berdasarkan stasiun
df_grouped = df.groupby("station")[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].mean()

# Koordinat stasiun (contoh, bisa diperbarui dengan data yang benar)
station_coords = {
    "Aotizhongxin": [39.9828, 116.4074],
    "Changping": [40.2181, 116.2210],
    "Dingling": [40.2906, 116.2202],
    "Dongsi": [39.9289, 116.4173],
    "Guanyuan": [39.9336, 116.3655],
    "Gucheng": [39.9001, 116.2297],
    "Huairou": [40.4175, 116.6333],
    "Nongzhanguan": [39.9671, 116.4617],
    "Shunyi": [40.1279, 116.6535],
    "Tiantan": [39.8817, 116.4145],
    "Wanliu": [39.9793, 116.3077],
    "Wanshouxigong": [39.8737, 116.3528]
}

# Buat peta dengan folium
m = folium.Map(location=[39.9, 116.4], zoom_start=10)

# Tambahkan marker untuk setiap stasiun
for station, coords in station_coords.items():
    if station in df_grouped.index:
        folium.CircleMarker(
            location=coords,
            radius=df_grouped.loc[station, "PM2.5"] / 10,  # Skala radius
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=f"{station}: {df_grouped.loc[station, 'PM2.5']:.2f} µg/m³"
        ).add_to(m)

# Tampilkan peta di Streamlit
folium_static(m)

st.write("Sumber data: Air Quality Dataset")
