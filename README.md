<div align="center">

# 🚀 CashPilot
### *Project & Finance Management Desktop App*

CashPilot adalah aplikasi desktop modern berbasis Python dan CustomTkinter yang dirancang untuk memudahkan manajemen proyek dan pencatatan keuangan bisnis secara profesional, cepat, dan terstruktur[cite: 1, 2, 5].

</div>

---

## ✨ Fitur Utama

* **🔐 Autentikasi Pengguna**: Halaman login yang aman dengan fitur *show/hide* password dan pengelolaan sesi[cite: 5].
* **📊 Dashboard Interaktif**: Menampilkan ringkasan total proyek, total pemasukan, pengeluaran, saldo, serta grafik *cashflow* bulanan secara *real-time*.
* **📁 Pengelompokan Transaksi**: Manajemen transaksi pemasukan dan pengeluaran yang dikelompokkan otomatis berdasarkan tanggal, lengkap dengan detail barang, kategori, dan pratinjau nota[cite: 1].
* **📤 Ekspor Multi-Format**: Fitur ekspor laporan keuangan instan ke format **Excel (`.xlsx`)**, **PDF (`.pdf`)**, dan **Word (`.docx`)**[cite: 1].
* **⚙️ Pengaturan Profil & Keamanan**: Ubah nama, username, foto profil dengan *crop* lingkaran otomatis, serta pembaruan kata sandi yang dilengkapi validasi keamanan[cite: 3].
* **🌙 Dynamic Dark & Light Mode**: Mendukung mode tampilan terang dan gelap yang langsung memperbarui antarmuka aplikasi secara *real-time*[cite: 1, 2, 3].

---

## 🛠️ Teknologi yang Digunakan

Aplikasi ini dibangun menggunakan ekosistem Python modern:
* **UI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) & Tkinter[cite: 1, 2, 3, 5]
* **Visualisasi Grafik**: Matplotlib
* **Pengolahan Gambar**: Pillow (PIL)[cite: 1, 2, 3]
* **Generator Laporan**: 
  * OpenPyXL (Excel)[cite: 1]
  * ReportLab (PDF)[cite: 1]
  * python-docx (Word)[cite: 1]
* **Komponen Pendukung**: tkcalendar[cite: 1]

---

## ⚙️ Cara Instalasi & Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di komputer lokal Anda:

1. **Clone repository ini:**
   ```bash
   git clone [https://github.com/username/cashpilot.git](https://github.com/username/cashpilot.git)
   cd cashpilot
pip install customtkinter pillow matplotlib reportlab openpyxl python-docx tkcalendar
python main.py
