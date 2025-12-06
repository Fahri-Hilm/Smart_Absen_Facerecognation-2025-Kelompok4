<div align="center">

# 🎯 Smart Absen

**Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://mysql.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?logo=opencv)](https://opencv.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[![GitHub Stars](https://img.shields.io/github/stars/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4?style=social)](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4?style=social)](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4)](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues)

**Kelompok 4 - Software Project 2025**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-dokumentasi) • [Team](#-tim-pengembang)

</div>

---

## 📋 Overview

Smart Absen adalah sistem absensi berbasis web yang menggunakan teknologi **Face Recognition** dan **QR Code Authentication** untuk menggantikan absensi manual yang rentan kecurangan dengan proses yang cepat, akurat, dan aman.

### Alur Penggunaan

```
┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  LAPTOP  │ ───► │    HP    │ ───► │  LAPTOP  │ ───► │   DONE   │
│  /auth   │      │ Scan QR  │      │Face Scan │      │  Sukses  │
└──────────┘      └──────────┘      └──────────┘      └──────────┘
 QR Display       Verify Access     Absensi Wajah     Data Tersimpan
```

---

## ✨ Features

| Fitur | Deskripsi |
|:------|:----------|
| 🔐 **QR Authentication** | Scan QR untuk akses, auto-refresh setiap 10 menit |
| 👤 **Face Recognition** | Deteksi & identifikasi wajah dengan InsightFace/ArcFace (99%+ accuracy) |
| ⏰ **Absensi Masuk/Pulang** | Dual mode dengan tracking jam kerja |
| 📊 **Admin Dashboard** | Kelola karyawan, laporan & data absensi |
| 📱 **Responsive Design** | Optimal di laptop & mobile |
| 🌐 **Cloudflare Tunnel** | Public HTTPS access |

---

## ⚡ Quick Start

```bash
# 1. Clone repository
git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git
cd Smart_Absen_Facerecognation-2025-Kelompok4

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database (MySQL harus running)
mysql -u root -e "CREATE DATABASE absensi_karyawan_db;"

# 5. Run aplikasi
python app.py
```

**Akses:** http://localhost:5001

> Untuk panduan lengkap, lihat [INSTALLATION.md](INSTALLATION.md)

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|:------|:----------|
| **Backend** | Flask • PyMySQL • OpenCV • scikit-learn |
| **Frontend** | HTML5 • CSS3 • JavaScript • Bootstrap 5 |
| **Database** | MySQL 8.0+ |
| **ML** | Haar Cascade (detection) • InsightFace/ArcFace (recognition - 99%+ accuracy) |
| **Infrastructure** | Cloudflare Tunnel (HTTPS) |

---

## 📁 Struktur Project

```
Smart_Absen/
├── app.py              # Main Flask application
├── config.py           # Konfigurasi database & app
├── database.py         # Database handler
├── models.py           # Data models
├── qr_sync.py          # QR cross-device sync manager
├── camera_lock.py      # Camera lock manager
├── requirements.txt    # Python dependencies
├── assets/             # ML model files
├── static/             # CSS, JS, images
├── templates/          # HTML templates
└── Attendance/         # CSV logs
```

---

## ⚙️ Konfigurasi

Edit `config.py` sesuai environment:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',              # Sesuaikan password MySQL
    'db': 'absensi_karyawan_db'
}

QR_VALIDITY_MINUTES = 10         # QR refresh setiap 10 menit
```

---

## 💻 System Requirements

| Komponen | Minimum |
|:---------|:--------|
| **OS** | Windows 10 / Ubuntu 20.04 / macOS |
| **Python** | 3.8+ |
| **MySQL** | 8.0+ |
| **RAM** | 4 GB |
| **Camera** | 720p webcam |
| **Browser** | Chrome / Firefox / Edge (terbaru) |

---

## 📖 Dokumentasi

| Dokumen | Deskripsi |
|:--------|:----------|
| [README.md](README.md) | Overview dan quick start (dokumen ini) |
| [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap step-by-step |
| [USAGE.md](USAGE.md) | Panduan penggunaan sistem |
| [API.md](docs/API_DOCUMENTATION.md) | Dokumentasi API endpoints |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture & design diagrams |
| [DOCSTRING_GUIDE.md](docs/DOCSTRING_GUIDE.md) | Docstring templates |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi |
| [CHANGELOG.md](CHANGELOG.md) | Riwayat perubahan |

---

## 👥 Tim Pengembang

**Kelompok 4 - Software Project 2025**

| Nama | Role |
|:-----|:-----|
| Fahri Hilmi | Lead Developer |

---

## 📜 License

MIT License © 2025 Kelompok 4 - Software Project

---

<div align="center">

**Made with ❤️ by Kelompok 4**

[⭐ Star](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4) • [🐛 Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues) • [📖 Docs](USAGE.md)

</div>
