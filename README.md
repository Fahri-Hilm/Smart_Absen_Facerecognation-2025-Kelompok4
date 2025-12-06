# 🎯 Smart Absen - Face Recognition Attendance System# 🎯 Smart Absen - Face Recognition Attendance System



> Sistem Absensi Pintar berbasis Face Recognition & QR Code Authentication**Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication**



[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)Kelompok 4 - Software Project 2025

[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)](https://flask.palletsprojects.com)

[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://mysql.com)![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?logo=opencv)](https://opencv.org)![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)

---

---

## ⚡ Quick Start

## 📚 Dokumentasi

```bash

# Clone & Setup| Dokumen | Deskripsi |

git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git|---------|-----------|

cd Smart_Absen_Facerecognation-2025-Kelompok4| [README.md](README.md) | Overview dan quick start (dokumen ini) |

python -m venv .venv && source .venv/bin/activate| [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap step-by-step |

pip install -r requirements.txt| [USAGE.md](USAGE.md) | Panduan penggunaan sistem |

| [API.md](docs/API_DOCUMENTATION.md) | Dokumentasi API endpoints |

# Database (MySQL harus running)| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi |

mysql -u root -e "CREATE DATABASE absensi_karyawan_db;"| [CHANGELOG.md](CHANGELOG.md) | Riwayat perubahan |



# Run---

python app.py

```## 📋 Table of Contents

🌐 Akses: **http://localhost:5001**

1. [Overview](#overview)

---2. [Features](#features)

3. [System Requirements](#system-requirements)

## 🎯 Fitur Utama4. [Quick Start](#quick-start)

5. [Project Structure](#project-structure)

| Fitur | Deskripsi |6. [Technology Stack](#technology-stack)

|-------|-----------|7. [Roadmap](#roadmap)

| 🔐 **QR Authentication** | Scan QR untuk akses (auto-refresh setiap 10 menit) |8. [Team](#team)

| 👤 **Face Recognition** | Deteksi & identifikasi wajah dengan KNN Classifier |

| ⏰ **Absensi Masuk/Pulang** | Dual mode dengan tracking jam kerja |---

| 📊 **Admin Dashboard** | Kelola karyawan, laporan & data absensi |

| 📱 **Responsive** | Optimal di laptop & mobile |## Overview

| 🌐 **Cloudflare Tunnel** | Public HTTPS access |

### Apa itu Smart Absen?

---

**Smart Absen** adalah sistem absensi berbasis web yang mengkombinasikan:

## 🔄 Alur Penggunaan- **QR Code Authentication** - Untuk verifikasi akses

- **Face Recognition** - Untuk identifikasi karyawan

```- **Real-time Processing** - Absensi langsung tercatat

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐

│  1. LAPTOP  │───▶│   2. HP     │───▶│  3. LAPTOP  │───▶│  4. DONE    │### Mengapa Smart Absen?

│   /auth     │    │  Scan QR    │    │  Face Scan  │    │  Tersimpan  │

│ QR + Code   │    │  Verify     │    │  Absensi    │    │  Database   │| Masalah Tradisional | Solusi Smart Absen |

└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘|---------------------|-------------------|

```| Absensi manual bisa dipalsukan | Face recognition memastikan kehadiran asli |

| Antrian panjang saat absen | Proses cepat < 5 detik |

---| Data tersebar di berbagai tempat | Centralized database |

| Sulit diakses remote | Cloud-ready dengan Cloudflare Tunnel |

## 🛠️ Tech Stack

### Demo Flow

| Layer | Teknologi |

|-------|-----------|```

| **Backend** | Flask, PyMySQL, OpenCV, scikit-learn |STEP 1           STEP 2           STEP 3           STEP 4

| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |[LAPTOP]  --->   [HP]     --->   [LAPTOP]  --->   [SUKSES]

| **Database** | MySQL 8.0+ | /auth          Verify          Absensi            Done

| **ML** | Haar Cascade (detection), KNN (recognition) |

| **Infra** | Cloudflare Tunnel (HTTPS) |QR Code         HP sebagai      Face Scan         Data

ditampilkan     "kunci"         & Verify          tersimpan

---```



## 📁 Struktur Project---



```## Features

├── app.py              # Main Flask application

├── config.py           # Konfigurasi database & app### Core Features (v1.0)

├── database.py         # Database handler

├── models.py           # Data models| No | Feature | Deskripsi | Status |

├── qr_sync.py          # QR cross-device sync|----|---------|-----------|--------|

├── camera_lock.py      # Camera lock manager| 1 | QR Authentication | Generate & scan QR untuk akses | Done |

├── requirements.txt    # Dependencies| 2 | Face Detection | Deteksi wajah dengan Haar Cascade | Done |

├── start.sh            # Startup script| 3 | Face Recognition | Identifikasi dengan KNN Classifier | Done |

├── assets/             # Model files (haarcascade, KNN)| 4 | Absen Masuk/Pulang | Dual mode attendance | Done |

├── static/             # CSS, JS, images| 5 | Admin Dashboard | Manage employees & reports | Done |

├── templates/          # HTML templates| 6 | Responsive UI | Optimal di laptop & mobile | Done |

└── Attendance/         # CSV logs| 7 | Cloudflare Tunnel | Public HTTPS access | Done |

```

### Planned Features (v2.0)

---

| No | Feature | Deskripsi | Priority |

## ⚙️ Konfigurasi|----|---------|-----------|----------|

| 1 | Dashboard Face Training | Capture foto langsung dari web | High |

Edit `config.py`:| 2 | Upload Foto Manual | Drag & drop upload foto wajah | High |

```python| 3 | Model Re-training | Train ulang tanpa restart | Medium |

DB_CONFIG = {| 4 | Analytics Dashboard | Grafik & statistik kehadiran | Medium |

    'host': '127.0.0.1',| 5 | Email Notifications | Alert keterlambatan | Low |

    'user': 'root',

    'password': '',  # Sesuaikan---

    'db': 'absensi_karyawan_db'

}## System Requirements

```

### Minimum Requirements

---

| Component | Specification |

## 📖 Dokumentasi|-----------|--------------|

| OS | Windows 10 / Ubuntu 20.04 / macOS 10.15+ |

| Dokumen | Deskripsi || Python | 3.8 atau lebih tinggi |

|---------|-----------|| MySQL | 8.0 atau lebih tinggi |

| [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap || RAM | 4 GB minimum |

| [USAGE.md](USAGE.md) | Panduan penggunaan || Storage | 500 MB free space |

| [API Documentation](docs/API_DOCUMENTATION.md) | REST API endpoints || Camera | Webcam dengan resolusi min 720p |

| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi || Browser | Chrome 90+ / Firefox 88+ / Edge 90+ |

| [CHANGELOG.md](CHANGELOG.md) | Riwayat perubahan |

---

---

## Quick Start

## 💻 System Requirements

### 5-Minute Setup

| Komponen | Minimum |

|----------|---------|```bash

| OS | Windows 10 / Ubuntu 20.04 / macOS |# 1. Clone repository

| Python | 3.8+ |git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git

| MySQL | 8.0+ |cd Smart_Absen_Facerecognation-2025-Kelompok4

| RAM | 4 GB |

| Camera | 720p webcam |# 2. Setup virtual environment

python -m venv .venv

---source .venv/bin/activate  # Linux/Mac

# .venv\Scripts\activate   # Windows

## 👥 Tim Pengembang

# 3. Install dependencies

**Kelompok 4 - Software Project 2025**pip install -r requirements.txt



| Nama | NIM | Role |# 4. Setup database (pastikan MySQL running)

|------|-----|------|mysql -u root -p -e "CREATE DATABASE absensi_karyawan_db;"

| Fahri Hilmi | - | Lead Developer |

| - | - | - |# 5. Configure (edit config.py dengan credentials MySQL Anda)



---# 6. Run application

python app.py

## 📜 License```



MIT License © 2025 Kelompok 4Akses: http://localhost:5001



---Untuk panduan instalasi lengkap, lihat [INSTALLATION.md](INSTALLATION.md)



<p align="center">---

  <a href="https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4">⭐ Star this repo</a> •

  <a href="https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues">🐛 Report Bug</a>## Project Structure

</p>

```
Smart_Absen/
├── README.md              # Dokumen ini
├── INSTALLATION.md        # Panduan instalasi
├── USAGE.md               # Panduan penggunaan
├── CONTRIBUTING.md        # Panduan kontribusi
├── CHANGELOG.md           # Riwayat perubahan
├── app.py                 # Main Flask application
├── config.py              # Configuration
├── database.py            # Database handler
├── models.py              # Data models
├── requirements.txt       # Dependencies
├── start.sh               # Startup script
├── start_with_tunnel.sh   # Startup dengan tunnel
├── assets/                # Model files
├── static/                # Frontend assets
├── templates/             # HTML templates
├── docs/                  # Documentation
└── Attendance/            # CSV logs
```

---

## Technology Stack

### Backend

| Teknologi | Kegunaan |
|-----------|----------|
| Flask | Web framework Python |
| PyMySQL | Database connection |
| OpenCV | Face detection |
| scikit-learn | Face recognition (KNN) |

### Frontend

| Teknologi | Kegunaan |
|-----------|----------|
| HTML5/CSS3 | Structure & styling |
| JavaScript | Interactivity |
| Bootstrap | Responsive components |

### Infrastructure

| Teknologi | Kegunaan |
|-----------|----------|
| MySQL | Database |
| Cloudflare Tunnel | Public HTTPS access |

---

## Roadmap

### Phase 1: Foundation - COMPLETED
- Project setup & architecture
- Database design
- Basic Flask application
- Face detection & recognition

### Phase 2: Core Features - COMPLETED
- QR code authentication
- Cross-device sync
- Attendance recording
- Admin dashboard

### Phase 3: Enhancement - COMPLETED
- Responsive UI
- Mobile-friendly layout
- Cloudflare Tunnel integration

### Phase 4: Training System - IN PROGRESS
- Dashboard untuk training model
- Capture foto dari webcam
- Upload foto manual

### Phase 5: Analytics - PLANNED
- Analytics dashboard
- Reports export

---

## Team

### Kelompok 4 - Software Project 2025

| No | Nama | NIM | Role |
|----|------|-----|------|
| 1 | [Nama 1] | [NIM] | Project Manager |
| 2 | [Nama 2] | [NIM] | Backend Developer |
| 3 | [Nama 3] | [NIM] | Frontend Developer |
| 4 | [Nama 4] | [NIM] | ML Engineer |

---

## License

MIT License - Educational Use

Copyright (c) 2025 Kelompok 4 - Software Project

---

## Links

- Repository: https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4
- Issues: https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues

---

Made with love by Kelompok 4 - Software Project 2025
