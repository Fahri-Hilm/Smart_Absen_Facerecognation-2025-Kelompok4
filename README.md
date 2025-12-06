<div align="center"># 🎯 Smart Absen - Face Recognition Attendance System# 🎯 Smart Absen# 🎯 Smart Absen - Face Recognition Attendance System# 🎯 Smart Absen - Face Recognition Attendance System



<img src="static/images/logo.png" alt="Smart Absen Logo" width="120"/>



# Smart Absen```



**Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication**╔══════════════════════════════════════════════════════════════════════════════╗



[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)║  Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication      ║**Sistem Absensi Pintar dengan Face Recognition & QR Code**

[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)

[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)║  Kelompok 4 - Software Project 2025                                          ║

[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)](https://opencv.org)

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)╚══════════════════════════════════════════════════════════════════════════════╝



[Panduan Instalasi](INSTALLATION.md) · [Dokumentasi API](docs/API_DOCUMENTATION.md) · [Panduan Penggunaan](USAGE.md)```



</div>[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)> Sistem Absensi Pintar berbasis Face Recognition & QR Code Authentication**Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication**



---[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)



## Overview[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)](https://flask.palletsprojects.com)[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)](https://flask.palletsprojects.com)



Smart Absen adalah sistem absensi berbasis web yang menggunakan teknologi Face Recognition dan QR Code Authentication. Sistem ini dirancang untuk menggantikan absensi manual yang rentan terhadap kecurangan dengan proses yang cepat dan akurat.[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://mysql.com)



Fitur utama:[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?logo=opencv)](https://opencv.org)[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://mysql.com)

- **QR Code Authentication** - Scan QR untuk verifikasi akses dengan auto-refresh setiap 10 menit

- **Face Recognition** - Identifikasi wajah menggunakan KNN Classifier

- **Admin Dashboard** - Kelola data karyawan, laporan, dan statistik kehadiran

- **Responsive Design** - Optimal di laptop dan perangkat mobile---[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?logo=opencv)](https://opencv.org)



## Installation



```bash## 📋 Daftar Isi[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)Kelompok 4 - Software Project 2025

# Clone repository

git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git

cd Smart_Absen_Facerecognation-2025-Kelompok4

```---

# Setup virtual environment

python -m venv .venv┌──────────────────────────────────────────────────────────────────────────────┐

source .venv/bin/activate  # Linux/Mac

# .venv\Scripts\activate   # Windows│  01. Quick Start ............................................. [ ⚡ ]        │[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?logo=flask)](https://flask.palletsprojects.com)



# Install dependencies│  02. Fitur Utama ............................................. [ ✨ ]        │

pip install -r requirements.txt

│  03. Alur Penggunaan ......................................... [ 🔄 ]        │## ⚡ Quick Start

# Setup database (MySQL harus running)

mysql -u root -e "CREATE DATABASE absensi_karyawan_db;"│  04. Tech Stack .............................................. [ 🛠️ ]        │



# Run│  05. Struktur Project ........................................ [ 📁 ]        │[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white)](https://mysql.com)![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

python app.py

```│  06. Konfigurasi ............................................. [ ⚙️ ]        │



Akses aplikasi di: **http://localhost:5001**│  07. Dokumentasi ............................................. [ 📖 ]        │```bash



Untuk panduan lengkap, lihat [INSTALLATION.md](INSTALLATION.md)│  08. Requirements ............................................ [ 💻 ]        │



## Usage Flow│  09. Tim Pengembang .......................................... [ 👥 ]        │# 1. Clone repository[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?logo=opencv)](https://opencv.org)![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)



```└──────────────────────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐

│  LAPTOP  │ ──► │    HP    │ ──► │  LAPTOP  │ ──► │   DONE   │```git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git

│  /auth   │     │ Scan QR  │     │Face Scan │     │  Sukses  │

└──────────┘     └──────────┘     └──────────┘     └──────────┘

```

---cd Smart_Absen_Facerecognation-2025-Kelompok4[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

1. Buka halaman `/auth` di laptop - QR Code ditampilkan

2. Scan QR Code menggunakan HP untuk verifikasi

3. Laptop redirect ke halaman absensi - Face scan dilakukan

4. Data absensi tersimpan ke database## ⚡ 01. Quick Start



## Configuration



Edit `config.py` sesuai environment:```bash# 2. Setup environment![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)



```python# ┌─────────────────────────────────────────────────────────────────────────────

DB_CONFIG = {

    'host': '127.0.0.1',# │ INSTALASIpython -m venv .venv

    'user': 'root',

    'password': '',  # Sesuaikan# └─────────────────────────────────────────────────────────────────────────────

    'db': 'absensi_karyawan_db'

}source .venv/bin/activate      # Linux/Mac---



QR_VALIDITY_MINUTES = 10  # QR refresh interval# Clone repository

```

git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git# .venv\Scripts\activate       # Windows

## Tech Stack

cd Smart_Absen_Facerecognation-2025-Kelompok4

| Layer | Technology |

|-------|------------|---

| Backend | Flask, PyMySQL, OpenCV, scikit-learn |

| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |# Setup virtual environment

| Database | MySQL 8.0+ |

| ML | Haar Cascade (detection), KNN (recognition) |python -m venv .venv# 3. Install dependencies

| Infrastructure | Cloudflare Tunnel |

source .venv/bin/activate      # Linux/Mac

## Project Structure

# .venv\Scripts\activate       # Windowspip install -r requirements.txt## ⚡ Quick Start

```

├── app.py              # Main Flask application

├── config.py           # Configuration

├── database.py         # Database handler# Install dependencies

├── models.py           # Data models

├── qr_sync.py          # QR cross-device syncpip install -r requirements.txt

├── camera_lock.py      # Camera lock manager

├── requirements.txt    # Dependencies# 4. Setup database (MySQL harus running)## 📚 Dokumentasi

├── assets/             # ML model files

├── static/             # CSS, JS, images# Setup database (MySQL harus running)

├── templates/          # HTML templates

└── Attendance/         # CSV logsmysql -u root -e "CREATE DATABASE absensi_karyawan_db;"mysql -u root -e "CREATE DATABASE absensi_karyawan_db;"

```



## Requirements

# Jalankan aplikasi```bash

| Component | Version |

|-----------|---------|python app.py

| Python | 3.8+ |

| MySQL | 8.0+ |```# 5. Run aplikasi

| OS | Windows 10 / Ubuntu 20.04 / macOS |

| RAM | 4 GB minimum |

| Webcam | 720p |

```python app.py# Clone & Setup| Dokumen | Deskripsi |

## Documentation

┌─────────────────────────────────────────────────────────────────────────────┐

- [INSTALLATION.md](INSTALLATION.md) - Panduan instalasi lengkap

- [USAGE.md](USAGE.md) - Panduan penggunaan│  🌐 AKSES: http://localhost:5001                                            │```

- [API Documentation](docs/API_DOCUMENTATION.md) - REST API endpoints

- [CONTRIBUTING.md](CONTRIBUTING.md) - Panduan kontribusi└─────────────────────────────────────────────────────────────────────────────┘

- [CHANGELOG.md](CHANGELOG.md) - Riwayat perubahan

```git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git|---------|-----------|

## Contributing



Kontribusi sangat diterima! Silakan baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan.

---**Akses:** http://localhost:5001

## Team



**Kelompok 4 - Software Project 2025**

## ✨ 02. Fitur Utamacd Smart_Absen_Facerecognation-2025-Kelompok4| [README.md](README.md) | Overview dan quick start (dokumen ini) |

| Name | Role |

|------|------|

| Fahri Hilmi | Lead Developer |

```---

## License

┌─────────────────────────────────────────────────────────────────────────────┐

MIT License © 2025 Kelompok 4

│  FITUR                    │  DESKRIPSI                                      │python -m venv .venv && source .venv/bin/activate| [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap step-by-step |

---

├───────────────────────────┼─────────────────────────────────────────────────┤

<div align="center">

│  🔐 QR Authentication     │  Scan QR untuk akses (auto-refresh 10 menit)    │## ✨ Fitur

Made with ❤️ by Kelompok 4

│  👤 Face Recognition      │  Identifikasi wajah dengan KNN Classifier       │

[⭐ Star](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4) · [🐛 Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues) · [📖 Docs](USAGE.md)

│  ⏰ Absensi Masuk/Pulang  │  Dual mode dengan tracking jam kerja            │pip install -r requirements.txt| [USAGE.md](USAGE.md) | Panduan penggunaan sistem |

</div>

│  📊 Admin Dashboard       │  Kelola karyawan, laporan & data absensi        │

│  📱 Responsive Design     │  Optimal di laptop & mobile                     │| Fitur | Deskripsi |

│  🌐 Cloudflare Tunnel     │  Public HTTPS access                            │

└───────────────────────────┴─────────────────────────────────────────────────┘|:------|:----------|| [API.md](docs/API_DOCUMENTATION.md) | Dokumentasi API endpoints |

```

| 🔐 QR Authentication | Scan QR untuk akses, auto-refresh tiap 10 menit |

---

| 👤 Face Recognition | Identifikasi wajah dengan KNN Classifier |# Database (MySQL harus running)| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi |

## 🔄 03. Alur Penggunaan

| ⏰ Absensi Masuk/Pulang | Dual mode dengan tracking jam kerja |

```

┌─────────────────────────────────────────────────────────────────────────────┐| 📊 Admin Dashboard | Kelola karyawan, laporan & data |mysql -u root -e "CREATE DATABASE absensi_karyawan_db;"| [CHANGELOG.md](CHANGELOG.md) | Riwayat perubahan |

│                           FLOW ABSENSI                                      │

├─────────────────────────────────────────────────────────────────────────────┤| 📱 Responsive | Optimal di laptop & mobile |

│                                                                             │

│   ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐       │| 🌐 Cloudflare Tunnel | Public HTTPS access |

│   │    1     │      │    2     │      │    3     │      │    4     │       │

│   │  LAPTOP  │ ───► │    HP    │ ───► │  LAPTOP  │ ───► │   DONE   │       │

│   │  /auth   │      │ Scan QR  │      │Face Scan │      │ Sukses!  │       │

│   └──────────┘      └──────────┘      └──────────┘      └──────────┘       │---# Run---

│       │                  │                 │                 │              │

│       ▼                  ▼                 ▼                 ▼              │

│   QR Code &          Verify            Absensi           Data              │

│   Kode Input         Access            Wajah            Tersimpan          │## 🔄 Cara Kerjapython app.py

│                                                                             │

└─────────────────────────────────────────────────────────────────────────────┘

```

``````## 📋 Table of Contents

---

[1. LAPTOP]      [2. HP]        [3. LAPTOP]      [4. DONE]

## 🛠️ 04. Tech Stack

   /auth    -->  Scan QR   -->  Face Scan   -->  Tersimpan🌐 Akses: **http://localhost:5001**

```

┌─────────────────────────────────────────────────────────────────────────────┐  QR Code        Verify         Absensi          Database

│  LAYER              │  TEKNOLOGI                                            │

├─────────────────────┼───────────────────────────────────────────────────────┤```1. [Overview](#overview)

│  Backend            │  Flask • PyMySQL • OpenCV • scikit-learn              │

│  Frontend           │  HTML5 • CSS3 • JavaScript • Bootstrap 5              │

│  Database           │  MySQL 8.0+                                           │

│  Machine Learning   │  Haar Cascade (detection) • KNN (recognition)         │------2. [Features](#features)

│  Infrastructure     │  Cloudflare Tunnel (HTTPS)                            │

└─────────────────────┴───────────────────────────────────────────────────────┘

```

## 🛠️ Tech Stack3. [System Requirements](#system-requirements)

---



## 📁 05. Struktur Project

**Backend:** Flask • PyMySQL • OpenCV • scikit-learn  ## 🎯 Fitur Utama4. [Quick Start](#quick-start)

```

┌─────────────────────────────────────────────────────────────────────────────┐**Frontend:** HTML5 • CSS3 • JavaScript • Bootstrap 5  

│  Smart_Absen/                                                               │

├─────────────────────────────────────────────────────────────────────────────┤**Database:** MySQL 8.0+  5. [Project Structure](#project-structure)

│  ├── app.py                 # Main Flask application                        │

│  ├── config.py              # Konfigurasi database & app                    │**ML:** Haar Cascade (detection) • KNN (recognition)

│  ├── database.py            # Database handler                              │

│  ├── models.py              # Data models                                   │| Fitur | Deskripsi |6. [Technology Stack](#technology-stack)

│  ├── qr_sync.py             # QR cross-device sync manager                  │

│  ├── camera_lock.py         # Camera lock manager                           │---

│  ├── requirements.txt       # Python dependencies                           │

│  ├── start.sh               # Startup script                                │|-------|-----------|7. [Roadmap](#roadmap)

│  │                                                                          │

│  ├── assets/                # ML model files                                │## 📁 Struktur

│  │   ├── haarcascade_frontalface_default.xml                                │

│  │   └── model_knn.pkl                                                      │| 🔐 **QR Authentication** | Scan QR untuk akses (auto-refresh setiap 10 menit) |8. [Team](#team)

│  │                                                                          │

│  ├── static/                # Frontend assets                               │```

│  │   ├── css/                                                               │

│  │   ├── js/                                                                │├── app.py              # Main Flask app| 👤 **Face Recognition** | Deteksi & identifikasi wajah dengan KNN Classifier |

│  │   └── images/                                                            │

│  │                                                                          │├── config.py           # Konfigurasi

│  ├── templates/             # HTML templates                                │

│  │   ├── qr_auth.html                                                       │├── database.py         # Database handler| ⏰ **Absensi Masuk/Pulang** | Dual mode dengan tracking jam kerja |---

│  │   ├── web_attendance.html                                                │

│  │   └── admin_*.html                                                       │├── models.py           # Data models

│  │                                                                          │

│  └── Attendance/            # CSV attendance logs                           │├── qr_sync.py          # QR sync manager| 📊 **Admin Dashboard** | Kelola karyawan, laporan & data absensi |

└─────────────────────────────────────────────────────────────────────────────┘

```├── camera_lock.py      # Camera lock



---├── requirements.txt    # Dependencies| 📱 **Responsive** | Optimal di laptop & mobile |## Overview



## ⚙️ 06. Konfigurasi├── assets/             # ML models



```python├── static/             # CSS, JS| 🌐 **Cloudflare Tunnel** | Public HTTPS access |

# ┌─────────────────────────────────────────────────────────────────────────────

# │ config.py - Edit sesuai environment Anda├── templates/          # HTML

# └─────────────────────────────────────────────────────────────────────────────

└── Attendance/         # CSV logs### Apa itu Smart Absen?

DB_CONFIG = {

    'host': '127.0.0.1',```

    'user': 'root',

    'password': '',              # Sesuaikan password MySQL---

    'db': 'absensi_karyawan_db'

}---



# QR Code Settings**Smart Absen** adalah sistem absensi berbasis web yang mengkombinasikan:

QR_VALIDITY_MINUTES = 10         # QR refresh setiap 10 menit

```## ⚙️ Konfigurasi



---## 🔄 Alur Penggunaan- **QR Code Authentication** - Untuk verifikasi akses



## 📖 07. DokumentasiEdit `config.py`:



```- **Face Recognition** - Untuk identifikasi karyawan

┌─────────────────────────────────────────────────────────────────────────────┐

│  DOKUMEN                         │  DESKRIPSI                               │```python

├──────────────────────────────────┼──────────────────────────────────────────┤

│  📄 INSTALLATION.md              │  Panduan instalasi lengkap               │DB_CONFIG = {```- **Real-time Processing** - Absensi langsung tercatat

│  📄 USAGE.md                     │  Panduan penggunaan sistem               │

│  📄 docs/API_DOCUMENTATION.md    │  REST API endpoints                      │    'host': '127.0.0.1',

│  📄 CONTRIBUTING.md              │  Panduan kontribusi                      │

│  📄 CHANGELOG.md                 │  Riwayat perubahan                       │    'user': 'root',┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐

└──────────────────────────────────┴──────────────────────────────────────────┘

```    'password': '',



---    'db': 'absensi_karyawan_db'│  1. LAPTOP  │───▶│   2. HP     │───▶│  3. LAPTOP  │───▶│  4. DONE    │### Mengapa Smart Absen?



## 💻 08. System Requirements}



``````│   /auth     │    │  Scan QR    │    │  Face Scan  │    │  Tersimpan  │

┌─────────────────────────────────────────────────────────────────────────────┐

│  KOMPONEN           │  MINIMUM                                              │

├─────────────────────┼───────────────────────────────────────────────────────┤

│  Operating System   │  Windows 10 / Ubuntu 20.04 / macOS                    │---│ QR + Code   │    │  Verify     │    │  Absensi    │    │  Database   │| Masalah Tradisional | Solusi Smart Absen |

│  Python             │  3.8 atau lebih tinggi                                │

│  MySQL              │  8.0 atau lebih tinggi                                │

│  RAM                │  4 GB                                                 │

│  Webcam             │  720p resolution                                      │## 📖 Dokumentasi└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘|---------------------|-------------------|

│  Browser            │  Chrome / Firefox / Edge (terbaru)                    │

└─────────────────────┴───────────────────────────────────────────────────────┘

```

- [INSTALLATION.md](INSTALLATION.md) — Panduan instalasi lengkap```| Absensi manual bisa dipalsukan | Face recognition memastikan kehadiran asli |

---

- [USAGE.md](USAGE.md) — Panduan penggunaan

## 👥 09. Tim Pengembang

- [API Documentation](docs/API_DOCUMENTATION.md) — REST API| Antrian panjang saat absen | Proses cepat < 5 detik |

```

╔═════════════════════════════════════════════════════════════════════════════╗- [CONTRIBUTING.md](CONTRIBUTING.md) — Panduan kontribusi

║                     KELOMPOK 4 - SOFTWARE PROJECT 2025                      ║

╠═════════════════════════════════════════════════════════════════════════════╣- [CHANGELOG.md](CHANGELOG.md) — Riwayat perubahan---| Data tersebar di berbagai tempat | Centralized database |

║  NAMA                        │  ROLE                                        ║

╠──────────────────────────────┼──────────────────────────────────────────────╣

║  Fahri Hilmi                 │  Lead Developer                              ║

╚══════════════════════════════╧══════════════════════════════════════════════╝---| Sulit diakses remote | Cloud-ready dengan Cloudflare Tunnel |

```



---

## 💻 Requirements## 🛠️ Tech Stack

## 📜 License



```

┌─────────────────────────────────────────────────────────────────────────────┐| Komponen | Versi |### Demo Flow

│  MIT License © 2025 Kelompok 4 - Software Project                           │

└─────────────────────────────────────────────────────────────────────────────┘|:---------|:------|

```

| OS | Windows 10 / Ubuntu 20.04 / macOS || Layer | Teknologi |

---

| Python | 3.8+ |

<div align="center">

| MySQL | 8.0+ ||-------|-----------|```

```

┌─────────────────────────────────────────────────────────────────────────────┐| RAM | 4 GB |

│  ⭐ Star this repo  •  🐛 Report Bug  •  💡 Request Feature                 │

│                                                                             │| Camera | 720p || **Backend** | Flask, PyMySQL, OpenCV, scikit-learn |STEP 1           STEP 2           STEP 3           STEP 4

│  https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4   │

└─────────────────────────────────────────────────────────────────────────────┘

```

---| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |[LAPTOP]  --->   [HP]     --->   [LAPTOP]  --->   [SUKSES]

</div>



## 👥 Tim| **Database** | MySQL 8.0+ | /auth          Verify          Absensi            Done



**Kelompok 4 — Software Project 2025**| **ML** | Haar Cascade (detection), KNN (recognition) |



| Nama | Role || **Infra** | Cloudflare Tunnel (HTTPS) |QR Code         HP sebagai      Face Scan         Data

|:-----|:-----|

| Fahri Hilmi | Lead Developer |ditampilkan     "kunci"         & Verify          tersimpan



------```



## 📜 License



MIT License © 2025 Kelompok 4## 📁 Struktur Project---



---



<div align="center">```## Features



[⭐ Star](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4) · [🐛 Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues)├── app.py              # Main Flask application



</div>├── config.py           # Konfigurasi database & app### Core Features (v1.0)


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
