# 🚀 Kafebasabasi Attendance System - Dual Mode Guide

## 📋 Cara Menjalankan Aplikasi

### 🎯 **Quick Start (Recommended)**

```bash
# Jalankan dengan launcher interaktif
python3 launcher.py
```

### 🔧 **Manual Mode**

#### 1. **DUAL MODE (Local + Ngrok) - Default**
```bash
# Otomatis coba ngrok, fallback ke local jika gagal
python3 app.py
```

#### 2. **LOCAL ONLY Mode**
```bash
# Hanya akses lokal, tanpa ngrok
LOCAL_ONLY=true python3 app.py
```

#### 3. **NGROK FORCED Mode**
```bash
# Paksa ngrok aktif
USE_NGROK=true python3 app.py
```

#### 4. **CAMERA TEST Mode**
```bash
# Test kamera saja (port 5002)
python3 launcher.py
# Pilih opsi 4
```

---

## 🌐 **URL Access**

### **Local Access (Selalu Tersedia)**
- 🏠 **Main App**: `http://localhost:5001`
- 👨‍💼 **Admin**: `http://localhost:5001/admin/login`
- 📷 **Camera Test**: `http://localhost:5001/camera-test`
- 📱 **QR Auth**: `http://localhost:5001/auth`

### **Public Access (Jika Ngrok Aktif)**
- 🌐 **Public URL**: `https://xxxxx.ngrok-free.dev`
- 📱 **Mobile**: `https://xxxxx.ngrok-free.dev/mobile`
- 👨‍💼 **Admin Public**: `https://xxxxx.ngrok-free.dev/admin/login`

---

## 🔑 **Login Credentials**

### **Admin Access**
- **Username**: `admin`
- **Password**: `admin123`

---

## 🎥 **Camera Features**

### **Konfigurasi Kamera (Admin)**
1. Login ke admin panel
2. Pilih "Konfigurasi Kamera"
3. Fitur tersedia:
   - ✅ **Request Permission** - Minta izin kamera browser
   - ✅ **Debug Kamera** - Analisis masalah kamera
   - ✅ **Reload Kamera** - Refresh daftar kamera
   - ✅ **Aktifkan Kamera** - Start camera preview

### **Troubleshooting Kamera**
1. **Jika error permission**: Klik "Request Permission"
2. **Jika kamera tidak terdeteksi**: Klik "Debug Kamera"
3. **Untuk test sederhana**: Gunakan Camera Test mode

---

## 📱 **Mobile Usage**

### **Untuk Karyawan (Mobile)**
1. Buka `https://xxxxx.ngrok-free.dev/mobile` (URL public)
2. Scan QR code untuk autentikasi
3. Kamera akan aktif otomatis untuk face recognition
4. Absensi masuk/pulang otomatis

### **QR Code Authentication**
- **Local**: `http://localhost:5001/auth`
- **Public**: `https://xxxxx.ngrok-free.dev/auth`

---

## ⚙️ **Environment Variables**

```bash
# Dual mode configuration
USE_NGROK=true          # Enable/disable ngrok (default: true)
LOCAL_ONLY=false        # Force local only (default: false)

# Database configuration  
DB_HOST=localhost       # MySQL host
DB_PORT=3306           # MySQL port
DB_USER=root           # MySQL username
DB_PASSWORD=password   # MySQL password
DB_NAME=absensi_karyawan_db  # Database name
```

---

## 🛠️ **Development Tips**

### **Local Development**
```bash
# Untuk development, gunakan local only
LOCAL_ONLY=true python3 app.py
```

### **Production Deployment**
```bash
# Untuk production dengan ngrok
USE_NGROK=true python3 app.py
```

### **Camera Testing**
```bash
# Test kamera terpisah di port 5002
python3 launcher.py
# Pilih opsi 4: Camera Test
```

---

## 🚨 **Common Issues & Solutions**

### **Ngrok Issues**
- **Error**: `ngrok not found`
  - **Solution**: Install ngrok atau gunakan `LOCAL_ONLY=true`

### **Camera Issues**  
- **Error**: `Permission denied`
  - **Solution**: Klik "Request Permission" di admin camera
- **Error**: `Camera not found`
  - **Solution**: Pastikan kamera terhubung, gunakan "Debug Kamera"

### **Database Issues**
- **Error**: `MySQL connection failed`
  - **Solution**: Pastikan MySQL running dan credentials benar

---

## 📊 **Monitoring & Logs**

### **Ngrok Dashboard**
- URL: `http://localhost:4040`
- Monitor traffic, requests, dan performance

### **Application Logs**
- Real-time logs di terminal
- Error handling dengan detail lengkap
- Debug mode tersedia

---

## 🎯 **Best Practices**

1. **Untuk Demo**: Gunakan dual mode (default)
2. **Untuk Development**: Gunakan LOCAL_ONLY=true
3. **Untuk Mobile Testing**: Gunakan ngrok HTTPS URL
4. **Untuk Camera Issues**: Gunakan Camera Test mode dulu

---

*Made with ❤️ for Kafebasabasi*