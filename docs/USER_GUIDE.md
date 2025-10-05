# 🏢 Panduan Penggunaan Sistem Absensi Face Recognition

## 📋 **Daftar Isi**
1. [Halaman Utama (User)](#halaman-utama-user)
2. [Halaman Admin](#halaman-admin)
3. [Fitur-Fitur](#fitur-fitur)
4. [Troubleshooting](#troubleshooting)

---

## 🏠 **Halaman Utama (User)**

### Akses
- **URL**: `http://127.0.0.1:5001/`
- **Untuk**: Semua karyawan

### Fitur
✅ **Absen Masuk** - Rekam waktu kedatangan  
✅ **Absen Pulang** - Rekam waktu kepulangan  
✅ **Pilih Kamera** - Dropdown untuk memilih kamera yang akan digunakan  
✅ **Statistik Real-time** - Lihat total karyawan dan absensi minggu ini  

### Cara Penggunaan
1. **Pilih Kamera**
   - Gunakan dropdown untuk memilih kamera (Default: 0)
   - Kamera akan otomatis tersimpan untuk sesi selanjutnya

2. **Absen Masuk**
   - Klik tombol "ABSEN MASUK" (hijau)
   - Posisikan wajah di depan kamera
   - Tunggu sampai wajah terdeteksi dan data tersimpan
   - Tekan ESC untuk keluar manual

3. **Absen Pulang**
   - Klik tombol "ABSEN PULANG" (merah)
   - Posisikan wajah di depan kamera
   - Tunggu sampai wajah terdeteksi dan data tersimpan
   - Tekan ESC untuk keluar manual

---

## 🛡️ **Halaman Admin**

### Akses
- **URL**: `http://127.0.0.1:5001/admin/login`
- **Username Default**: `admin`
- **Password Default**: `admin123`
- **Username Alternatif**: `supervisor` / `super123`

### Dashboard Admin
Setelah login, admin dapat mengakses:

#### 📊 **Statistik Dashboard**
- Total karyawan terdaftar
- Total absensi minggu ini  
- Jumlah hadir hari ini
- Status kamera aktif

#### 👥 **Manajemen Karyawan**
- **Tambah Karyawan Baru**: Form untuk menambah karyawan
- **Lihat Data Karyawan**: Daftar semua karyawan terdaftar
- **Training Model**: Otomatis saat menambah karyawan baru

#### 📅 **Manajemen Absensi**
- **Lihat Data Absensi**: Tabel absensi dengan filter
- **Hapus Data Absensi**: Hapus record individual
- **Export Data**: Download laporan dalam format CSV/PDF
- **Clear All Data**: Hapus semua data absensi (HATI-HATI!)

#### 🎥 **Manajemen Kamera**
- **Test Kamera**: Uji semua kamera yang tersedia
- **Pilih Kamera Default**: Set kamera untuk sistem

#### 🗃️ **Manajemen Database**
- **Status Database**: Cek koneksi dan status
- **Backup Data**: Backup database (manual)
- **Reset Database**: Reset semua tabel (HATI-HATI!)

---

## 🚀 **Fitur-Fitur Utama**

### 🎯 **Face Recognition**
- **Teknologi**: OpenCV + Machine Learning (KNN)
- **Akurasi**: Tinggi dengan training yang baik
- **Real-time**: Deteksi wajah langsung
- **Multi-face**: Bisa mendeteksi beberapa wajah sekaligus

### 📱 **Responsive Design**
- **Mobile-Friendly**: Tampilan optimal di semua device
- **Professional**: Desain clean dan modern
- **Fast Loading**: Optimized untuk performa

### 🔒 **Security**
- **Admin Authentication**: Login terproteksi
- **Session Management**: Auto logout
- **Role-based Access**: Pemisahan user dan admin

### 📊 **Real-time Dashboard**
- **Live Statistics**: Update otomatis setiap 30 detik
- **Weekly Reports**: Laporan mingguan otomatis
- **Data Visualization**: Grafik dan chart interaktif

---

## 🛠️ **Troubleshooting**

### ❌ **Masalah Umum**

#### **1. Kamera Tidak Terdeteksi**
```
✅ Solusi:
- Pastikan kamera terhubung dengan baik
- Coba ganti kamera ID (0, 1, 2)
- Restart aplikasi
- Cek permission kamera di sistem
```

#### **2. Wajah Tidak Terdeteksi**
```
✅ Solusi:
- Pastikan pencahayaan cukup terang
- Posisikan wajah langsung ke kamera
- Jarak ideal: 30-50 cm dari kamera
- Pastikan tidak ada objek menghalangi wajah
```

#### **3. Database Connection Error**
```
✅ Solusi:
- Pastikan Devilbox/MariaDB sudah running
- Cek konfigurasi database di config.py
- Restart database service
- Cek log error di terminal
```

#### **4. Model Belum Dilatih**
```
✅ Solusi:
- Login sebagai admin
- Tambahkan minimal 1 karyawan
- Sistem akan otomatis training model
- Refresh halaman setelah training selesai
```

#### **5. Total Jam Kerja NULL**
```
✅ Solusi:
- Jalankan script: python3 fix_total_jam_kerja.py
- Pastikan ada jam masuk DAN jam pulang
- Restart aplikasi
```

### 📞 **Support**
Jika masih ada masalah:
1. Cek log error di terminal
2. Screenshot error message
3. Cek file log di folder `logs/` (jika ada)

---

## 📝 **Changelog**

### Version 2.0 (Current)
- ✅ Pemisahan halaman user dan admin
- ✅ Professional UI/UX design
- ✅ Admin authentication system
- ✅ Responsive design untuk mobile
- ✅ Real-time statistics dashboard
- ✅ Improved database management
- ✅ Better error handling

### Version 1.0 (Previous)
- ✅ Basic face recognition
- ✅ Simple attendance recording
- ✅ Basic web interface
- ✅ MySQL database integration

---

## 🎯 **Tips Penggunaan**

### Untuk User:
1. **Posisi Optimal**: Duduk/berdiri tegak menghadap kamera
2. **Pencahayaan**: Pastikan wajah terkena cahaya yang cukup
3. **Konsistensi**: Gunakan posisi yang sama setiap hari
4. **Sabar**: Tunggu 2-3 detik untuk deteksi wajah

### Untuk Admin:
1. **Backup Rutin**: Export data secara berkala
2. **Monitor Performance**: Cek dashboard statistics secara rutin
3. **Update Model**: Re-training jika akurasi menurun
4. **Security**: Ganti password default admin

---

**📧 Support**: Hubungi administrator sistem untuk bantuan lebih lanjut.