# Dashboard Analisis Kualitas Udara

## Deskripsi

Dashboard ini menampilkan analisis kualitas udara berdasarkan dataset PRSA yang mencakup beberapa stasiun pemantauan di berbagai lokasi. Dashboard dibuat menggunakan Streamlit dan menyajikan berbagai visualisasi data terkait polutan udara.

## Struktur Direktori

```
|-- dashboard/
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
git clone <repository_url>
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
