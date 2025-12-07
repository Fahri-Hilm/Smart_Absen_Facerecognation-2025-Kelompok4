# 📦 Installation Guide

> Panduan instalasi lengkap Smart Absen Face Recognition System

**Version:** 2.1 | **Last Updated:** 2025-12-07

---

## 🚀 Quick Start (Choose One)

### Option A: Docker (Recommended) 🐳

**Fastest way to get started - No Python/MySQL setup needed!**

```bash
# Pull & run
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
docker run -d -p 5001:5001 --env-file .env \
  ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
```

**Full Docker Guide:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

---

### Option B: Manual Installation

Traditional Python + MySQL setup (for development or non-Docker environments)

---

## 📋 Table of Contents

### Docker Installation
1. [Docker Prerequisites](#docker-prerequisites)
2. [Docker Quick Start](#docker-quick-start)
3. [Docker with MySQL](#docker-with-mysql)

### Manual Installation
4. [Manual Prerequisites](#manual-prerequisites)
5. [Step 1: Clone Repository](#step-1-clone-repository)
6. [Step 2: Setup Python Environment](#step-2-setup-python-environment)
7. [Step 3: Install Dependencies](#step-3-install-dependencies)
8. [Step 4: Setup MySQL Database](#step-4-setup-mysql-database)
9. [Step 5: Configure Application](#step-5-configure-application)
10. [Step 6: Initialize Database](#step-6-initialize-database)
11. [Step 7: Run Application](#step-7-run-application)
12. [Step 8: Verify Installation](#step-8-verify-installation)

### Additional Setup
13. [Optional: Setup Cloudflare Tunnel](#optional-setup-cloudflare-tunnel)
14. [Troubleshooting](#-troubleshooting)

---

## 🐳 Docker Installation

### Docker Prerequisites

| # | Requirement | Cara Cek | Status |
|---|-------------|----------|--------|
| 1 | Docker 20.10+ | `docker --version` | ☐ |
| 2 | Docker Compose (optional) | `docker-compose --version` | ☐ |

**Install Docker:**

```bash
# Linux (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify
docker --version
```

---

### Docker Quick Start

```bash
# 1. Create .env file
cat > .env << 'EOF'
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=smart_absen
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
PORT=5001
EOF

# 2. Pull image
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# 3. Run container
docker run -d \
  --name smart-absen \
  -p 5001:5001 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/face_data:/app/face_data \
  --restart unless-stopped \
  ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# 4. Verify
docker ps
docker logs -f smart-absen
curl http://localhost:5001/health
```

**Access:** http://localhost:5001

---

### Docker with MySQL

Use Docker Compose for complete stack (app + database):

```bash
# 1. Clone repository
git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git
cd Smart_Absen_Facerecognation-2025-Kelompok4

# 2. Create .env
cp .env.example .env
nano .env  # Edit credentials

# 3. Start services
docker-compose up -d

# 4. Check status
docker-compose ps
docker-compose logs -f app
```

**Full Docker Documentation:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)

---

## 🔧 Manual Installation

### Manual Prerequisites

---

## 📋 Manual Prerequisites

### Checklist Sebelum Instalasi

| # | Requirement | Cara Cek | Status |
|---|-------------|----------|--------|
| 1 | Python 3.8+ | `python --version` | ☐ |
| 2 | pip (package manager) | `pip --version` | ☐ |
| 3 | MySQL Server 8.0+ | `mysql --version` | ☐ |
| 4 | Git | `git --version` | ☐ |
| 5 | Webcam | Device Manager | ☐ |
| 6 | Browser modern | Chrome/Firefox/Edge | ☐ |

### Install Prerequisites (Jika Belum Ada)

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3 python3-pip python3-venv

# Install MySQL
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

# Install Git
sudo apt install git

# Install OpenCV dependencies
sudo apt install libgl1-mesa-glx libglib2.0-0
```

#### Windows
1. **Python:** Download dari https://www.python.org/downloads/
   - ✅ Centang "Add Python to PATH" saat instalasi
2. **MySQL:** Download dari https://dev.mysql.com/downloads/installer/
   - Pilih "MySQL Server" dan "MySQL Workbench"
3. **Git:** Download dari https://git-scm.com/download/win

#### macOS
```bash
# Install Homebrew (jika belum ada)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install MySQL
brew install mysql
brew services start mysql

# Install Git
brew install git
```

---

## Step 1: Clone Repository

### 1.1 Buka Terminal/Command Prompt

```bash
# Navigasi ke folder project Anda
cd ~/Documents/Projects  # atau folder pilihan Anda
```

### 1.2 Clone Repository

```bash
git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git
```

### 1.3 Masuk ke Folder Project

```bash
cd Smart_Absen_Facerecognation-2025-Kelompok4
```

### ✅ Verifikasi Step 1

```bash
ls -la
# Harus muncul file: app.py, config.py, requirements.txt, dll
```

---

## Step 2: Setup Python Environment

### 2.1 Buat Virtual Environment

```bash
python -m venv .venv
```

> **Mengapa Virtual Environment?**
> - Isolasi dependencies per project
> - Menghindari konflik package
> - Mudah di-reproduce di komputer lain

### 2.2 Aktivasi Virtual Environment

#### Linux/macOS
```bash
source .venv/bin/activate
```

#### Windows (Command Prompt)
```cmd
.venv\Scripts\activate
```

#### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

### ✅ Verifikasi Step 2

```bash
which python  # Linux/macOS
# atau
where python  # Windows

# Output harus menunjukkan path di folder .venv
```

Prompt terminal akan berubah:
```
(.venv) user@computer:~/project$
```

---

## Step 3: Install Dependencies

### 3.1 Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

### 3.2 Install Requirements

```bash
pip install -r requirements.txt
```

### 3.3 Daftar Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | ≥2.0.0 | Web framework |
| PyMySQL | ≥1.0.0 | MySQL driver |
| opencv-python | ≥4.5.0 | Face detection |
| insightface | ≥0.7.0 | Face recognition (ArcFace - 99%+ accuracy) |
| onnxruntime | ≥1.10.0 | InsightFace runtime |
| numpy | ≥1.20.0 | Array operations |
| Pillow | ≥8.0.0 | Image processing |
| qrcode | ≥7.0 | QR generation |

### ✅ Verifikasi Step 3

```bash
pip list | grep -E "(Flask|PyMySQL|opencv|insightface|onnx)"
```

Output yang diharapkan:
```
Flask                    2.x.x
PyMySQL                  1.x.x
opencv-python            4.x.x
insightface              0.x.x
onnxruntime              1.x.x
```

---

## Step 4: Setup MySQL Database

### 4.1 Start MySQL Service

#### Linux
```bash
sudo systemctl start mysql
sudo systemctl status mysql  # Pastikan "active (running)"
```

#### macOS
```bash
brew services start mysql
```

#### Windows
- Buka "Services" (services.msc)
- Cari "MySQL80"
- Pastikan status "Running"

### 4.2 Login ke MySQL

```bash
mysql -u root -p
# Masukkan password MySQL Anda
```

### 4.3 Buat Database

```sql
-- Buat database baru
CREATE DATABASE absensi_karyawan_db;

-- Verifikasi
SHOW DATABASES;

-- Keluar
EXIT;
```

### 4.4 (Optional) Buat User Khusus

```sql
-- Buat user baru (lebih aman daripada pakai root)
CREATE USER 'smartabsen'@'localhost' IDENTIFIED BY 'password123';

-- Berikan akses ke database
GRANT ALL PRIVILEGES ON absensi_karyawan_db.* TO 'smartabsen'@'localhost';

-- Apply privileges
FLUSH PRIVILEGES;

EXIT;
```

### ✅ Verifikasi Step 4

```bash
mysql -u root -p -e "SHOW DATABASES;" | grep absensi
# Output: absensi_karyawan_db
```

---

## Step 5: Configure Application

### 5.1 Buka File Config

```bash
# Gunakan editor favorit Anda
nano config.py   # Linux/macOS
# atau
code config.py   # VS Code
# atau
notepad config.py  # Windows
```

### 5.2 Edit Konfigurasi Database

```python
# config.py

# ============================================
# DATABASE CONFIGURATION
# ============================================

DB_HOST = 'localhost'           # Host MySQL
DB_USER = 'root'                # Username MySQL (atau 'smartabsen')
DB_PASSWORD = 'your_password'   # ⚠️ GANTI dengan password Anda
DB_NAME = 'absensi_karyawan_db' # Nama database

# ============================================
# APPLICATION CONFIGURATION
# ============================================

SECRET_KEY = 'your-secret-key-here'  # ⚠️ GANTI dengan random string
DEBUG = True                          # Set False untuk production
HOST = '0.0.0.0'                      # Listen semua interface
PORT = 5001                           # Port aplikasi
```

### 5.3 Generate Secret Key (Recommended)

```python
# Jalankan di Python untuk generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy output dan paste ke `SECRET_KEY`.

### ✅ Verifikasi Step 5

```bash
python -c "import config; print(f'DB: {config.DB_NAME}')"
# Output: DB: absensi_karyawan_db
```

---

## Step 6: Initialize Database

### 6.1 Jalankan Aplikasi (Auto-Create Tables)

```bash
python app.py
```

Aplikasi akan otomatis membuat tabel-tabel yang diperlukan saat pertama kali dijalankan.

### 6.2 Verifikasi Tabel

```bash
mysql -u root -p absensi_karyawan_db -e "SHOW TABLES;"
```

Output yang diharapkan:
```
+------------------------------+
| Tables_in_absensi_karyawan_db|
+------------------------------+
| admins                       |
| attendance                   |
| employees                    |
+------------------------------+
```

### ✅ Verifikasi Step 6

```bash
mysql -u root -p absensi_karyawan_db -e "SELECT * FROM admins;"
# Harus ada default admin user
```

---

## Step 7: Run Application

### 7.1 Mode Development (Local)

```bash
# Pastikan virtual environment aktif
source .venv/bin/activate  # Linux/macOS

# Jalankan aplikasi
python app.py
```

### 7.2 Menggunakan Script

```bash
# Berikan permission (Linux/macOS)
chmod +x start.sh

# Jalankan
./start.sh
```

### 7.3 Output yang Diharapkan

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.x.x:5001
```

### ✅ Verifikasi Step 7

Buka browser dan akses:
- http://localhost:5001 → Harus muncul halaman home
- http://localhost:5001/auth → Harus muncul QR code

---

## Step 8: Verify Installation

### 8.1 Checklist Verifikasi

| # | Test | URL | Expected Result |
|---|------|-----|-----------------|
| 1 | Home Page | http://localhost:5001 | Halaman utama muncul |
| 2 | QR Auth | http://localhost:5001/auth | QR code ditampilkan |
| 3 | Admin Login | http://localhost:5001/admin/login | Form login muncul |
| 4 | Camera Access | http://localhost:5001/web_attendance | Browser minta izin kamera |

### 8.2 Test Admin Login

1. Buka http://localhost:5001/admin/login
2. Login dengan:
   - Username: `admin`
   - Password: `admin123`
3. Harus redirect ke dashboard

### 8.3 Test Face Detection

1. Buka http://localhost:5001/web_attendance
2. Allow camera access
3. Wajah harus terdeteksi (kotak hijau di wajah)

### ✅ Installation Complete! 🎉

---

## Optional: Setup Cloudflare Tunnel

### Mengapa Cloudflare Tunnel?
- Akses dari mana saja via internet
- HTTPS otomatis (required untuk camera di HP)
- Tidak perlu port forwarding

### Install Cloudflared

#### Linux
```bash
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
```

#### macOS
```bash
brew install cloudflare/cloudflare/cloudflared
```

#### Windows
Download dari: https://github.com/cloudflare/cloudflared/releases

### Jalankan dengan Tunnel

```bash
# Berikan permission
chmod +x start_with_tunnel.sh

# Jalankan
./start_with_tunnel.sh
```

Output:
```
╔════════════════════════════════════════════════════════════╗
║  🌐 PUBLIC URL: https://xxx-xxx-xxx.trycloudflare.com      ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🔧 Troubleshooting

### Error: ModuleNotFoundError

**Problem:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Pastikan virtual environment aktif
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Error: MySQL Connection Failed

**Problem:**
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
```

**Solution:**
```bash
# Check MySQL status
sudo systemctl status mysql

# Start MySQL jika tidak running
sudo systemctl start mysql

# Verify credentials
mysql -u root -p
```

---

### Error: Permission Denied

**Problem:**
```
bash: ./start.sh: Permission denied
```

**Solution:**
```bash
chmod +x start.sh
chmod +x start_with_tunnel.sh
```

---

### Error: Port Already in Use

**Problem:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Cari process yang menggunakan port
lsof -i :5001

# Kill process
kill -9 <PID>
```

---

### Error: Camera Not Found

**Problem:**
```
Camera tidak muncul di browser
```

**Solution:**
1. Pastikan browser punya izin kamera
2. Check di browser settings → Privacy → Camera
3. Gunakan HTTPS (Cloudflare Tunnel) untuk akses dari HP
4. Linux: Pastikan user ada di group `video`
   ```bash
   sudo usermod -a -G video $USER
   # Logout dan login kembali
   ```

---

### Error: Face Not Recognized

**Problem:**
```
Wajah terdeteksi tapi tidak dikenali
```

**Solution:**
1. Pastikan sudah ada data training untuk karyawan
2. Minimal 5 foto dengan angle berbeda
3. Pencahayaan harus cukup
4. Re-train model jika diperlukan

---

## 📞 Need Help?

Jika masih mengalami masalah:
1. Cek [GitHub Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues)
2. Buat issue baru dengan detail error
3. Hubungi tim pengembang

---

<p align="center">
  <b>Happy Coding! 🚀</b>
</p>
