# 🎯 Smart Absen - Face Recognition Attendance System

**Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication**

Kelompok 4 - Software Project 2025

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)

---

## 📚 Dokumentasi

| Dokumen | Deskripsi |
|---------|-----------|
| [README.md](README.md) | Overview dan quick start (dokumen ini) |
| [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap step-by-step |
| [USAGE.md](USAGE.md) | Panduan penggunaan sistem |
| [API.md](docs/API_DOCUMENTATION.md) | Dokumentasi API endpoints |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi |
| [CHANGELOG.md](CHANGELOG.md) | Riwayat perubahan |

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Quick Start](#quick-start)
5. [Project Structure](#project-structure)
6. [Technology Stack](#technology-stack)
7. [Roadmap](#roadmap)
8. [Team](#team)

---

## Overview

### Apa itu Smart Absen?

**Smart Absen** adalah sistem absensi berbasis web yang mengkombinasikan:
- **QR Code Authentication** - Untuk verifikasi akses
- **Face Recognition** - Untuk identifikasi karyawan
- **Real-time Processing** - Absensi langsung tercatat

### Mengapa Smart Absen?

| Masalah Tradisional | Solusi Smart Absen |
|---------------------|-------------------|
| Absensi manual bisa dipalsukan | Face recognition memastikan kehadiran asli |
| Antrian panjang saat absen | Proses cepat < 5 detik |
| Data tersebar di berbagai tempat | Centralized database |
| Sulit diakses remote | Cloud-ready dengan Cloudflare Tunnel |

### Demo Flow

```
STEP 1           STEP 2           STEP 3           STEP 4
[LAPTOP]  --->   [HP]     --->   [LAPTOP]  --->   [SUKSES]
 /auth          Verify          Absensi            Done

QR Code         HP sebagai      Face Scan         Data
ditampilkan     "kunci"         & Verify          tersimpan
```

---

## Features

### Core Features (v1.0)

| No | Feature | Deskripsi | Status |
|----|---------|-----------|--------|
| 1 | QR Authentication | Generate & scan QR untuk akses | Done |
| 2 | Face Detection | Deteksi wajah dengan Haar Cascade | Done |
| 3 | Face Recognition | Identifikasi dengan KNN Classifier | Done |
| 4 | Absen Masuk/Pulang | Dual mode attendance | Done |
| 5 | Admin Dashboard | Manage employees & reports | Done |
| 6 | Responsive UI | Optimal di laptop & mobile | Done |
| 7 | Cloudflare Tunnel | Public HTTPS access | Done |

### Planned Features (v2.0)

| No | Feature | Deskripsi | Priority |
|----|---------|-----------|----------|
| 1 | Dashboard Face Training | Capture foto langsung dari web | High |
| 2 | Upload Foto Manual | Drag & drop upload foto wajah | High |
| 3 | Model Re-training | Train ulang tanpa restart | Medium |
| 4 | Analytics Dashboard | Grafik & statistik kehadiran | Medium |
| 5 | Email Notifications | Alert keterlambatan | Low |

---

## System Requirements

### Minimum Requirements

| Component | Specification |
|-----------|--------------|
| OS | Windows 10 / Ubuntu 20.04 / macOS 10.15+ |
| Python | 3.8 atau lebih tinggi |
| MySQL | 8.0 atau lebih tinggi |
| RAM | 4 GB minimum |
| Storage | 500 MB free space |
| Camera | Webcam dengan resolusi min 720p |
| Browser | Chrome 90+ / Firefox 88+ / Edge 90+ |

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git
cd Smart_Absen_Facerecognation-2025-Kelompok4

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database (pastikan MySQL running)
mysql -u root -p -e "CREATE DATABASE absensi_karyawan_db;"

# 5. Configure (edit config.py dengan credentials MySQL Anda)

# 6. Run application
python app.py
```

Akses: http://localhost:5001

Untuk panduan instalasi lengkap, lihat [INSTALLATION.md](INSTALLATION.md)

---

## Project Structure

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
