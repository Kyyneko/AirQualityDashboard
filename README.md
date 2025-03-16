# Dashboard Analisis Kualitas Udara

## Deskripsi Proyek

Dashboard ini bertujuan untuk menganalisis kualitas udara di Beijing berdasarkan data dari berbagai stasiun pemantauan dalam periode 2013 hingga 2017. Data yang digunakan berasal dari dataset PRSA, yang mencakup parameter polusi udara seperti PM2.5, PM10, SO2, NO2, CO, dan O3. Dengan menggunakan Streamlit, proyek ini menyajikan berbagai visualisasi data interaktif yang membantu dalam memahami tren kualitas udara serta faktor-faktor yang mempengaruhi polusi.

## Tujuan Analisis

1. **Mengetahui tren kualitas udara (PM2.5) dari tahun ke tahun.**
2. **Mengidentifikasi lokasi dengan tingkat polusi tertinggi dan terendah.**
3. **Menganalisis hubungan antara variabel meteorologi (suhu, kelembaban, tekanan udara) dengan tingkat polusi.**
4. **Menyediakan visualisasi interaktif untuk eksplorasi data lebih lanjut.**

## Fitur Dashboard

- **Tren Polusi:** Menampilkan grafik tren PM2.5 dari waktu ke waktu.
- **Perbandingan Antar Lokasi:** Diagram boxplot yang membandingkan tingkat polusi antar stasiun pemantauan.
- **Analisis Musiman:** Grafik yang menunjukkan pola polusi berdasarkan musim.
- **Peta Interaktif:** Heatmap lokasi polusi tertinggi dan terendah menggunakan Folium.

## Struktur Direktori

```
|-- dashboard/
    |-- main_data.csv # Dataset hasil gabungan dari seluruh dataset
    |-- dashboard.py  # Script utama Streamlit
    |-- data/
        |-- PRSA_Data_Aotizhongxin_20130301-20170228.csv
        |-- PRSA_Data_Changping_20130301-20170228.csv
        |-- ... (dataset lainnya)
    |-- requirements.txt  # Daftar dependensi
    |-- README.md  # Dokumentasi proyek
    |-- url.txt  # URL setelah deploy
```

## Instalasi dan Menjalankan Dashboard

### 1. Clone Repository (Jika menggunakan Git)

```bash
git clone <https://github.com/Kyyneko/AirQualityDashboard.git>
cd dashboard
```

### 2. Install Dependensi

Pastikan Anda menggunakan Python 3.8 ke atas.

```bash
pip install -r requirements.txt
```

### 3. Jalankan Streamlit

```bash
streamlit run dashboard.py
```

## Deployment ke Streamlit Cloud

1. **Upload Kode ke GitHub**
2. **Buka [Streamlit Cloud](https://share.streamlit.io/)**
3. **Hubungkan Repository GitHub**
4. **Set Environment (jika diperlukan)**
5. **Deploy dan dapatkan URL dashboard**

## URL Dashboard

Setelah deploy, URL dashboard akan tersedia di `url.txt`.

---

## `url.txt`

```
https://your-dashboard-url.streamlit.app/
```
