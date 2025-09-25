# Sistem Absensi Karyawan dengan Database MySQL

Sistem absensi berbasis face recognition menggunakan Flask dan PyMySQL untuk database MySQL.

## 🆕 Fitur Database Baru

- **Database MySQL** dengan PyMySQL
- **Nama Database**: `absensi_karyawan_db`
- **Tabel**: employees, attendance, activity_log
- **Kompatibel dengan Laragon**

## 📋 Struktur Database

### Tabel `employees`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `name` (VARCHAR(100), NOT NULL)
- `bagian` (VARCHAR(50), NOT NULL)
- `created_at`, `updated_at` (TIMESTAMP)

### Tabel `attendance`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)  
- `employee_id` (INT, FOREIGN KEY)
- `tanggal` (DATE, NOT NULL)
- `jam_masuk`, `jam_pulang`, `total_jam_kerja` (TIME)
- `status` (ENUM: 'hadir', 'tidak_hadir', 'terlambat')
- `created_at`, `updated_at` (TIMESTAMP)

### Tabel `activity_log`
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `employee_id` (INT, FOREIGN KEY)
- `activity_type` (ENUM: 'login', 'logout', 'add_employee', 'face_recognition')
- `description` (TEXT)
- `created_at` (TIMESTAMP)

## 🚀 Instalasi dan Setup

### 1. Install Dependencies
```bash
pip install pymysql flask opencv-python numpy scikit-learn pandas joblib
```

### 2. Setup Laragon MySQL
1. Buka Laragon
2. Start MySQL service
3. Pastikan MySQL berjalan di port 3306
4. User: `root`, Password: `` (kosong)

### 3. Inisialisasi Database
```bash
python init_database.py
```

Script ini akan:
- Membuat database `absensi_karyawan_db`
- Membuat tabel-tabel yang diperlukan
- Menambah data sample (opsional)

### 4. Jalankan Aplikasi
```bash
python app.py
```

Aplikasi akan berjalan di: `http://127.0.0.1:5001`

## 📁 File-File Baru

- `config.py` - Konfigurasi database dan aplikasi
- `database.py` - Database manager dengan PyMySQL
- `models.py` - Model untuk Employee, Attendance, ActivityLog
- `init_database.py` - Script inisialisasi database

## 🔧 Konfigurasi Database

Edit `config.py` untuk mengubah konfigurasi:

```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Laragon default
    'database': 'absensi_karyawan_db',  # Nama database baru
    'charset': 'utf8mb4',
    'autocommit': True
}
```

## 📊 Fitur Database

### ✅ Yang Sudah Terintegrasi:
- ✅ Penyimpanan data karyawan
- ✅ Pencatatan absensi masuk/pulang
- ✅ Perhitungan jam kerja otomatis
- ✅ Log aktivitas sistem
- ✅ Data mingguan dan harian

### 🔄 Migrasi dari CSV:
- Data absensi sekarang disimpan di database MySQL
- File CSV lama tetap ada untuk backup
- Sistem face recognition tetap sama

## 🛠️ Troubleshooting

### Database Connection Error:
1. Pastikan Laragon MySQL sudah running
2. Cek port MySQL (default: 3306)
3. Verifikasi user/password di `config.py`

### Inisialisasi Database Gagal:
```bash
# Jalankan ulang inisialisasi
python init_database.py
```

### Reset Database:
```sql
-- Login ke MySQL dan jalankan:
DROP DATABASE IF EXISTS absensi_karyawan_db;
```
Kemudian jalankan `python init_database.py` lagi.

## 📱 Cara Penggunaan

1. **Setup Database**: Jalankan `python init_database.py`
2. **Tambah Karyawan**: Gunakan form "Tambah Karyawan Baru"
3. **Absensi Masuk**: Klik "Absen Masuk" dan hadap kamera
4. **Absensi Pulang**: Klik "Absen Pulang" dan hadap kamera
5. **Lihat Data**: Data otomatis tampil di dashboard

## 🎯 Keunggulan Database MySQL

- **Performa Lebih Baik**: Query database lebih cepat dari CSV
- **Concurrent Access**: Multi-user bisa akses bersamaan
- **Data Integrity**: Foreign key dan constraint menjaga konsistensi
- **Scalability**: Mudah dikembangkan untuk fitur lanjutan
- **Backup & Recovery**: Sistem backup database yang robust
- **Query Flexibility**: SQL queries untuk laporan kompleks

## 🔮 Pengembangan Selanjutnya

- Dashboard admin dengan statistik
- Export laporan ke Excel/PDF  
- API endpoints untuk mobile app
- Integrasi dengan sistem payroll
- Notifikasi email/SMS
- Multi-location support

---

**Database**: `absensi_karyawan_db` | **Technology**: Flask + PyMySQL + OpenCV | **Compatible**: Laragon MySQL