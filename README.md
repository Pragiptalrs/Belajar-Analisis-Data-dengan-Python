Analisis Bike Sharing Dataset 

Ringkasan Analisis
Dataset ini berisi data penyewaan sepeda tahun 2011-2012. Analisis menunjukkan bahwa:
- Peminjaman tertinggi terjadi pada musim gugur dan saat cuaca cerah.
- Pola harian menunjukkan lonjakan penyewaan pada jam 08.00 dan 17.00.
- Hari kerja lebih tinggi jumlah penyewa dibanding akhir pekan.
- Pelanggan terdaftar lebih mendominasi dibanding penyewa kasual.

Kesimpulan:
- Fokus promosi pada jam sibuk dan musim dengan peminjaman rendah.
- Menarik lebih banyak pelanggan dengan promo khusus akhir pekan.

Dashboard Bike Sharing
Cara Menjalankan Dashboard

1. Instalasi Dependensi (Shell/Terminal)
mkdir bike_sharing_analysis
cd bike_sharing_analysis
pipenv install
pipenv shell
pip install -r requirements.txt

2. Menjalankan Dashboard
streamlit run dashboard.py

3. Deploy ke Streamlit Community Cloud
- Buat repository di GitHub dengan nama Belajar Analisis Data dengan Python.
- Push kode proyek ke repository tersebut.
- Buka Streamlit Community Cloud, login, dan hubungkan dengan repository.
- Deploy dan jalankan dashboard secara online.

