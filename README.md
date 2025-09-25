# 👥 SISTEM ABSENSI FACE RECOGNITION

Sistem absensi karyawan berbasis teknologi **Face Recognition** menggunakan **Python Flask** dan **MySQL Database** dengan **PyMySQL**. Sistem ini dapat mendeteksi wajah karyawan secara otomatis untuk mencatat absensi masuk dan pulang.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-red.svg)

## 🌟 **Fitur Utama**

### 🎯 **Face Recognition**
- ✅ Deteksi wajah real-time menggunakan OpenCV
- ✅ Machine Learning dengan K-Nearest Neighbors (KNN)
- ✅ Training model otomatis dari foto karyawan
- ✅ Akurasi tinggi untuk identifikasi wajah

### 📊 **Database MySQL**
- ✅ **Database**: `absensi_karyawan_db`
- ✅ **PyMySQL** untuk koneksi database
- ✅ **3 Tabel**: employees, attendance, activity_log
- ✅ **Foreign Key Constraints** untuk data integrity
- ✅ **Auto-increment** dan **timestamps**

### 📱 **Web Interface**
- ✅ Interface yang user-friendly
- ✅ Dashboard dengan statistik real-time
- ✅ Form untuk menambah karyawan baru
- ✅ Tampilan data absensi mingguan
- ✅ Multi-camera support

### 🕒 **Sistem Absensi**
- ✅ **Absensi Masuk** dan **Absensi Pulang**
- ✅ **Perhitungan jam kerja** otomatis
- ✅ **Log aktivitas** lengkap
- ✅ **Data mingguan** dan **harian**

## 🏗️ **Struktur Database**

### 📋 **Tabel `employees`**
```sql
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- name (VARCHAR(100), NOT NULL)
- bagian (VARCHAR(50), NOT NULL)  
- created_at, updated_at (TIMESTAMP)
```

### 📅 **Tabel `attendance`**
```sql
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- employee_id (INT, FOREIGN KEY)
- tanggal (DATE, NOT NULL)
- jam_masuk, jam_pulang, total_jam_kerja (TIME)
- status (ENUM: 'hadir', 'tidak_hadir', 'terlambat')
- created_at, updated_at (TIMESTAMP)
```

### 📝 **Tabel `activity_log`**
```sql
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- employee_id (INT, FOREIGN KEY)
- activity_type (ENUM: 'login', 'logout', 'add_employee', 'face_recognition')
- description (TEXT)
- created_at (TIMESTAMP)
```

## 🚀 **Instalasi & Setup**

### 1️⃣ **Clone Repository**
```bash
git clone https://github.com/[username]/SISTEM-ABSENSI-FACE.git
cd SISTEM-ABSENSI-FACE
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Setup Database MySQL**
**Untuk Laragon:**
- Start MySQL service di Laragon
- Default: User `root`, Password kosong
- Port: `3306`

**Untuk XAMPP/MySQL lainnya:**
- Sesuaikan konfigurasi di `config.py`

### 4️⃣ **Inisialisasi Database**
```bash
python init_database.py
```

### 5️⃣ **Jalankan Aplikasi**
```bash
python app.py
```

Aplikasi berjalan di: **http://127.0.0.1:5001**

## 📁 **Struktur Project**

```
SISTEM-ABSENSI-FACE/
├── 🐍 app.py                 # Aplikasi Flask utama
├── ⚙️ config.py              # Konfigurasi database & aplikasi
├── 🗄️ database.py           # Database manager PyMySQL
├── 📊 models.py              # Model data (Employee, Attendance, ActivityLog)
├── 🔧 init_database.py       # Script inisialisasi database
├── 🧪 test_database.py       # Script testing database
├── 🗑️ clear_database.py      # Script untuk mengosongkan database
├── 📋 requirements.txt       # Dependencies Python
├── 🤖 haarcascade_frontalface_default.xml # Face detection model
├── 📁 static/
│   ├── 🤖 face_recognition_model.pkl     # Trained ML model
│   └── 📸 faces/                         # Foto training karyawan
├── 📁 templates/
│   └── 🌐 home.html                      # Template web interface
├── 📁 Attendance/
│   └── 📄 *.csv                          # File backup absensi
└── 📖 README.md                          # Dokumentasi ini
```

## 🎮 **Cara Penggunaan**

### 👤 **Menambah Karyawan Baru**
1. Klik **"Tambah Karyawan Baru"**
2. Isi **Nama** dan **Bagian**
3. **Hadap kamera** untuk mengambil 10 foto training
4. System akan **training model** otomatis

### 🕐 **Absensi Masuk**
1. Klik **"Absen Masuk"**
2. **Hadap kamera** sampai wajah terdeteksi
3. System **otomatis mencatat** jam masuk

### 🕔 **Absensi Pulang**
1. Klik **"Absen Pulang"**
2. **Hadap kamera** sampai wajah terdeteksi  
3. System **otomatis menghitung** jam kerja

## 🛠️ **Konfigurasi**

### 📝 **Edit `config.py`**
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Sesuaikan dengan setup MySQL Anda
    'database': 'absensi_karyawan_db',
    'charset': 'utf8mb4'
}
```

## 🔧 **Troubleshooting**

### ❌ **Database Connection Error**
```bash
# Pastikan MySQL running
# Cek konfigurasi di config.py
# Test koneksi:
python test_database.py
```

### 🗑️ **Reset Database**
```bash
# Kosongkan semua data:
python clear_database.py

# Inisialisasi ulang:
python init_database.py
```

### 📷 **Kamera Tidak Terdeteksi**
- Pastikan webcam terpasang
- Coba ganti ID kamera di dropdown
- Restart aplikasi

## 🎯 **Teknologi yang Digunakan**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Backend programming |
| **Flask** | 2.3.3 | Web framework |
| **PyMySQL** | 1.1.2 | MySQL database connector |
| **OpenCV** | 4.8.0 | Computer vision & face detection |
| **scikit-learn** | 1.3.0 | Machine learning (KNN) |
| **NumPy** | 1.24.3 | Numerical computing |
| **Pandas** | 2.0.3 | Data manipulation |
| **MySQL** | 8.0+ | Database management |

## 🚀 **Fitur Mendatang**

- 📊 **Dashboard Analytics** dengan grafik
- 📱 **Mobile App** (Android/iOS)
- 📧 **Email Notifications** untuk keterlambatan
- 📄 **Export Reports** (PDF/Excel)
- 🌐 **Multi-branch Support**
- 🔐 **User Authentication & Authorization**
- 🎨 **Custom Themes**

## 📞 **Support**

Jika Anda mengalami masalah:
1. 📖 Baca dokumentasi ini dengan teliti
2. 🧪 Jalankan `python test_database.py` untuk diagnosis
3. 🗑️ Reset database dengan `python clear_database.py`
4. 📱 Hubungi developer untuk support lanjutan

## 📄 **Lisensi**

MIT License - Bebas digunakan untuk keperluan komersial dan non-komersial.

---

**🎉 Sistem Absensi Face Recognition - Solusi Absensi Modern untuk Era Digital!**

*Dibuat dengan ❤️ menggunakan Python, Flask, dan MySQL*