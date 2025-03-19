import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# =========================================================
# 📂 MEMUAT DATA
# =========================================================

file_paths = [
    "data/PRSA_Data_Aotizhongxin_20130301-20170228.csv",
    "data/PRSA_Data_Changping_20130301-20170228.csv",
    "data/PRSA_Data_Dingling_20130301-20170228.csv",
    "data/PRSA_Data_Dongsi_20130301-20170228.csv"
]

@st.cache_data
def load_data(files):
    df_list = []
    for file in files:
        df_temp = pd.read_csv(file)
        df_list.append(df_temp)

    df = pd.concat(df_list, ignore_index=True)
    df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]])

    drop_cols = ["year", "month", "day", "hour", "No"]
    df.drop(columns=[col for col in drop_cols if col in df.columns], inplace=True)

    # ✅ Tambahkan kolom 'month_year' agar tersedia di semua tampilan
    df["month_year"] = df["datetime"].dt.to_period("M").astype(str)

    return df

df = load_data(file_paths)

# =========================================================
# 📌 SIDEBAR NAVIGASI
# =========================================================
st.sidebar.title("📌 Navigasi Dashboard")
menu = st.sidebar.radio("Pilih Visualisasi", [
    "📈 Analisis PM2.5 di Beijing",
    "📊 Analisis Polutan Ditiap Stasiun",
    "🌍 Tren Polutan di Seluruh Beijing"
])

st.sidebar.markdown("---")
st.sidebar.info("Dashboard ini hanya mengambil data stasiun pemantauan udara di **Beijing, Tiongkok**.")

# =========================================================
# 📈 TAMPILAN 1: Tren PM2.5 (Rata-rata & Polusi Tertinggi/Terendah)
# =========================================================
if menu == "📈 Analisis PM2.5 di Beijing":
    st.title("📈 Tren Rata-rata PM2.5 di Beijing")

    df_avg_pm25 = df.groupby(["month_year", "station"])["PM2.5"].mean().reset_index()

    fig = px.line(df_avg_pm25, x="month_year", y="PM2.5", color="station", markers=True,
                  title="Tren Rata-rata PM2.5 di Beijing",
                  labels={"month_year": "Tahun - Bulan", "PM2.5": "Kadar PM2.5"})
    fig.update_layout(xaxis=dict(tickangle=45), legend_title="Stasiun")
    st.plotly_chart(fig)

    st.markdown("---")
    st.subheader("📍 Lokasi dengan Polusi Tertinggi dan Terendah")

    avg_pm25 = df.groupby("station")["PM2.5"].mean().sort_values(ascending=False)
    highest_pollution = avg_pm25.idxmax()
    lowest_pollution = avg_pm25.idxmin()

    st.write(f"🌆 **Stasiun dengan Polusi Tertinggi:** {highest_pollution} ({avg_pm25.max():.2f} µg/m³)")
    st.write(f"🌿 **Stasiun dengan Polusi Terendah:** {lowest_pollution} ({avg_pm25.min():.2f} µg/m³)")

    fig3 = px.bar(avg_pm25, x=avg_pm25.index, y=avg_pm25.values, color=avg_pm25.index,
                  title="Rata-rata PM2.5 di Berbagai Stasiun",
                  labels={"x": "Stasiun", "y": "PM2.5"})
    fig3.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig3)

    st.write("Sumber data: Air Quality Dataset")

# =========================================================
# 📊 TAMPILAN 2: Analisis Polutan Ditiap Stasiun (Pilihan Stasiun di Dalam)
# =========================================================
elif menu == "📊 Analisis Polutan Ditiap Stasiun":
    st.title("📊 Analisis Polutan Ditiap Stasiun")

    # Pilihan Stasiun ADA DI DALAM HALAMAN INI
    station_selected = st.selectbox("📍 Pilih Stasiun", df["station"].unique())
    df_filtered = df[df["station"] == station_selected]

    st.subheader("📋 Statistik Deskriptif Polutan")
    polutan = ["PM2.5","PM10", "SO2", "NO2", "CO", "O3"]
    st.dataframe(df_filtered[polutan].describe().T)

    st.subheader(f"📈 Tren Rata-rata Polutan Lain di {station_selected}")
    polutan_selected = st.selectbox("Pilih Polutan", polutan)

    df_avg_polutan = df_filtered.groupby(["month_year"])[polutan_selected].mean().reset_index()

    fig2 = px.line(df_avg_polutan, x="month_year", y=polutan_selected, markers=True,
                   title=f"Tren Rata-rata {polutan_selected} di {station_selected}",
                   labels={"month_year": "Tahun - Bulan", polutan_selected: f"Kadar {polutan_selected}"})
    fig2.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig2)

    st.write("Sumber data: Air Quality Dataset")

# =========================================================
# 🌍 TAMPILAN 3: Tren Polutan di Seluruh Beijing
# =========================================================
elif menu == "🌍 Tren Polutan di Seluruh Beijing":
    st.title("🌍 Tren Rata-rata Polutan di Seluruh Beijing")

    polutan_all_selected = st.selectbox("Pilih Polutan untuk Semua Stasiun", ["PM2.5","PM10", "SO2", "NO2", "CO", "O3"])

    df_avg_polutan_all = df.groupby(["month_year", "station"])[polutan_all_selected].mean().reset_index()

    fig4 = px.line(df_avg_polutan_all, x="month_year", y=polutan_all_selected, color="station", markers=True,
                   title=f"Tren Rata-rata {polutan_all_selected} di Seluruh Beijing",
                   labels={"month_year": "Tahun - Bulan", polutan_all_selected: f"Kadar {polutan_all_selected}"})
    fig4.update_layout(xaxis=dict(tickangle=45), legend_title="Stasiun")
    st.plotly_chart(fig4)

    st.markdown("---")
    st.subheader("🗺️ Peta Lokasi Stasiun Pemantauan")

    station_coords = {
        "Aotizhongxin": [39.9828, 116.4074],
        "Changping": [40.2181, 116.2210],
        "Dingling": [40.2906, 116.2202],
        "Dongsi": [39.9289, 116.4173]
    }

    m = folium.Map(location=[39.9, 116.4], zoom_start=10)
    for station, coords in station_coords.items():
        folium.Marker(location=coords, popup=station).add_to(m)

    folium_static(m)

    st.write("Sumber data: Air Quality Dataset")
