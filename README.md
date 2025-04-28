# 🧑‍💼 Absensi Karyawan Makan Gratis - Badan Gizi Nasional

Aplikasi absensi karyawan berbasis **deteksi wajah** menggunakan **Python**, **Flask**, dan **OpenCV**. Dirancang untuk mempermudah proses kehadiran dengan kamera laptop, webcam eksternal, maupun kamera HP via USB.

---

## 📦 Fitur Unggulan

- 🎯 Deteksi wajah real-time (Haar Cascade + KNN)
- 📷 Pilihan kamera dari dropdown (0–5)
- 👤 Pendaftaran wajah otomatis (10 gambar)
- ⏱️ Absensi masuk dan pulang tercatat dengan waktu
- 🧪 Uji kamera langsung dari web
- 📊 Data absensi mingguan dalam format CSV
- 📱 Tampilan responsive (Bootstrap 5)

---

## 📥 Persiapan Awal

### 1. Aktifkan Virtual Environment (Opsional)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Instalasi Library
```bash
pip install flask opencv-python pandas scikit-learn joblib
# atau
pip install -r requirements.txt
```

---

## 💻 Cara Menjalankan Aplikasi

### Via Command Prompt
```bash
cd C:\Users\NamaKamu\Documents\absensi-flask
python app.py
```
Akses melalui browser: [http://localhost:5000](http://localhost:5000)

### Via Visual Studio Code
- Buka folder proyek
- Buka terminal (Ctrl + `)
- Jalankan: `python app.py`
- Klik link http://localhost:5000

---

## 📷 Penggunaan Kamera

- Kamera Laptop
- Webcam USB
- Kamera HP (via USB + DroidCam)

### 📱 Tutorial DroidCam via USB
1. Install DroidCam (HP & PC) dari [dev47apps.com](https://www.dev47apps.com)
2. Aktifkan USB Debugging di HP
3. Hubungkan HP ke laptop via kabel USB
4. Jalankan DroidCam → pilih koneksi USB → Start
5. Pilih ID kamera yang muncul di aplikasi

---

## 🧪 Uji Kamera

- Pilih kamera dari dropdown
- Klik **Uji Kamera**
- Tekan `ESC` untuk menutup

---

## ➕ Tambah Karyawan Baru

1. Isi **Nama** & **Bagian**
2. Klik **Tambah**
3. Kamera akan mengambil 10 gambar otomatis
4. Model akan dilatih ulang

⏱️ Proses membutuhkan ±6 detik.

---

## ⏱️ Absensi Masuk & Pulang

1. Pilih kamera
2. Klik **Absen Masuk** atau **Absen Pulang**
3. Kamera mengenali wajah
4. Data disimpan ke file CSV

⏱️ Durasi proses: ±6 detik.

---

## 🗂️ Struktur Folder

```
├── app.py
├── templates/
│   └── home.html
├── static/
│   ├── faces/
│   └── face_recognition_model.pkl
├── Attendance/
├── haarcascade_frontalface_default.xml
```

---

## 💡 Tips Penggunaan

- Gunakan pencahayaan yang cukup
- Pastikan wajah tidak buram/gelap
- Tutup aplikasi lain yang menggunakan kamera
- Pastikan webcam/HP sudah tersambung dengan baik

---

## 👤 Author

**Sri Rahayu Usnul Khotimah**  
Proyek: Aplikasi Absensi Karyawan - Badan Gizi Nasional  
📍 Kota Sorong, Papua