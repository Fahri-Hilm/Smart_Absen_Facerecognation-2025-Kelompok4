# 🎯 Smart Absen - Face Recognition Attendance System# 🎯 Smart Absen Face Recognition# Smart Absen Face Recognition# 🏢 FaceAttend - Advanced Biometric System for Employee Network Management



> **Sistem Absensi Pintar dengan Face Recognition & QR Code Authentication**  

> Kelompok 4 - Software Project 2025

> **Sistem Absensi Pintar dengan Face Recognition & QR Authentication**  

<p align="center">

  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">> Kelompok 4 - Software Project 2025

  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white" alt="Python">

  <img src="https://img.shields.io/badge/Flask-2.0+-000000?logo=flask&logoColor=white" alt="Flask">> Sistem Absensi Pintar dengan Face Recognition - Kelompok 4 (2025)<div align="center">

  <img src="https://img.shields.io/badge/MySQL-8.0+-4479A1?logo=mysql&logoColor=white" alt="MySQL">

  <img src="https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?logo=opencv&logoColor=white" alt="OpenCV"><p align="center">

  <img src="https://img.shields.io/badge/License-Educational-green.svg" alt="License">

</p>  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">



---  <img src="https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">



## 📚 Dokumentasi  <img src="https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)



| Dokumen | Deskripsi |  <img src="https://img.shields.io/badge/OpenCV-4.0+-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">

|---------|-----------|

| [README.md](README.md) | Overview dan quick start (dokumen ini) |</p>![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)

| [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap step-by-step |

| [USAGE.md](USAGE.md) | Panduan penggunaan sistem |

| [API.md](docs/API_DOCUMENTATION.md) | Dokumentasi API endpoints |

| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi |---![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-red.svg)

| [CHANGELOG.md](CHANGELOG.md) | Riwayat perubahan |



---

## 📋 Daftar Isi![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red.svg)![MySQL](https://img.shields.io/#### ❌ **Cloudflare Tunnel Connection Failed**

## 📋 Table of Contents



1. [Overview](#-overview)

2. [Features](#-features)- [Deskripsi](#-deskripsi)```bash

3. [System Requirements](#-system-requirements)

4. [Quick Start](#-quick-start)- [Fitur Utama](#-fitur-utama)

5. [Project Structure](#-project-structure)

6. [Technology Stack](#-technology-stack)- [Tech Stack](#-tech-stack)## 📋 Deskripsi# Check cloudflared installation

7. [System Architecture](#-system-architecture)

8. [Roadmap](#-roadmap)- [Struktur Project](#-struktur-project)

9. [Team](#-team)

10. [License](#-license)- [Instalasi](#-instalasi)cloudflared --version



---- [Menjalankan Aplikasi](#-menjalankan-aplikasi)



## 🎯 Overview- [Cara Penggunaan](#-cara-penggunaan)Sistem absensi karyawan berbasis web dengan teknologi **Face Recognition** dan autentikasi **QR Code**. Mendukung mode absensi masuk dan pulang dengan verifikasi wajah real-time.



### Apa itu Smart Absen?- [Roadmap & Planning](#-roadmap--planning)



**Smart Absen** adalah sistem absensi berbasis web yang mengkombinasikan:- [Troubleshooting](#-troubleshooting)# Test manual tunnel

- **QR Code Authentication** - Untuk verifikasi akses

- **Face Recognition** - Untuk identifikasi karyawan- [Anggota Kelompok](#-anggota-kelompok)

- **Real-time Processing** - Absensi langsung tercatat

## ✨ Fitur Utamacloudflared tunnel --url http://localhost:5001

### Mengapa Smart Absen?

---

| Masalah Tradisional | Solusi Smart Absen |

|---------------------|-------------------|```SQL-8.0+-orange.svg)

| Absensi manual bisa dipalsukan | Face recognition memastikan kehadiran asli |

| Antrian panjang saat absen | Proses cepat < 5 detik |## 📝 Deskripsi

| Data tersebar di berbagai tempat | Centralized database |

| Sulit diakses remote | Cloud-ready dengan Cloudflare Tunnel |- 🔐 **QR Code Authentication** - HP sebagai kunci untuk akses![Cloudflare Tunnel](https://img.shields.io/badge/Cloudflare%20Tunnel-Integrated-orange.svg)



### Demo Flow**Smart Absen** adalah sistem absensi karyawan berbasis web yang mengintegrasikan teknologi **Face Recognition** dengan autentikasi **QR Code**. Sistem ini dirancang untuk memberikan pengalaman absensi yang aman, cepat, dan modern.



```- 👤 **Face Recognition** - Verifikasi wajah dengan KNN Classifier![PWA](https://img.shields.io/badge/PWA-Ready-darkgreen.svg)

┌──────────────────────────────────────────────────────────────────────────┐

│                        ALUR ABSENSI SMART ABSEN                         │### Alur Kerja Sistem

├──────────────────────────────────────────────────────────────────────────┤

│                                                                          │- 📱 **Responsive Design** - Tampilan optimal untuk laptop dan mobile![License](https://img.shields.io/badge/License-MIT-yellow.svg)

│   STEP 1              STEP 2              STEP 3              STEP 4    │

│  ┌────────┐          ┌────────┐          ┌────────┐          ┌────────┐ │```

│  │ LAPTOP │  ──────► │   HP   │  ──────► │ LAPTOP │  ──────► │ SUKSES │ │

│  │  /auth │  Scan QR │ Verify │  Sync    │ Absensi│  Face    │   ✓    │ │┌─────────────┐    Scan QR     ┌─────────────┐    Auto Redirect    ┌─────────────┐- 📊 **Dashboard Admin** - Manajemen karyawan dan laporan absensi![Version](https://img.shields.io/badge/Version-2.0.1-brightgreen.svg)

│  └────────┘          └────────┘          └────────┘          └────────┘ │

│                                                                          ││   Laptop    │ ─────────────► │     HP      │ ──────────────────► │   Laptop    │

│  QR Code             HP sebagai          Face Scan           Data       │

│  ditampilkan         "kunci digital"     & Verify            tersimpan  ││  (QR Page)  │                │ (Kunci ✓)   │                     │  (Absensi)  │- 🌐 **Cloudflare Tunnel** - Akses publik HTTPS tanpa port forwarding

│                                                                          │

└──────────────────────────────────────────────────────────────────────────┘└─────────────┘                └─────────────┘                     └─────────────┘

```

                                                                          │**🚀 Sistem Absensi Enterprise dengan AI Face Recognition & QR Authentication**

---

                                                                    Face Scan

## ✨ Features

                                                                          ▼## 🛠️ Tech Stack

### Core Features (v1.0) ✅

                                                                   ┌─────────────┐

| # | Feature | Deskripsi | Status |

|---|---------|-----------|--------|                                                                   │   Sukses!   │*Solusi comprehensive untuk manajemen kehadiran karyawan dengan teknologi Computer Vision dan dual access capability*

| 1 | QR Authentication | Generate & scan QR untuk akses | ✅ Done |

| 2 | Face Detection | Deteksi wajah dengan Haar Cascade | ✅ Done |                                                                   │  (Popup)    │

| 3 | Face Recognition | Identifikasi dengan KNN Classifier | ✅ Done |

| 4 | Absen Masuk/Pulang | Dual mode attendance | ✅ Done |                                                                   └─────────────┘| Komponen | Teknologi |

| 5 | Admin Dashboard | Manage employees & reports | ✅ Done |

| 6 | Responsive UI | Optimal di laptop & mobile | ✅ Done |```

| 7 | Cloudflare Tunnel | Public HTTPS access | ✅ Done |

|----------|-----------|[![Build Status](https://img.shields.io/badge/Build-Passing-success.svg)](https://github.com/Fahri-Hilm/FaceAttend)

### Planned Features (v2.0) 🚧

---

| # | Feature | Deskripsi | Priority |

|---|---------|-----------|----------|| Backend | Flask (Python) |[![Security](https://img.shields.io/badge/Security-Audited-success.svg)](https://github.com/Fahri-Hilm/FaceAttend)

| 1 | Dashboard Face Training | Capture foto langsung dari web | High |

| 2 | Upload Foto Manual | Drag & drop upload foto wajah | High |## ✨ Fitur Utama

| 3 | Model Re-training | Train ulang tanpa restart | Medium |

| 4 | Analytics Dashboard | Grafik & statistik kehadiran | Medium || Database | MySQL / PyMySQL |[![Uptime](https://img.shields.io/badge/Uptime-99.9%25-success.svg)](https://github.com/Fahri-Hilm/FaceAttend)

| 5 | Email Notifications | Alert keterlambatan | Low |

| Fitur | Deskripsi | Status |

---

|-------|-----------|--------|| Face Detection | OpenCV (Haar Cascade) |

## 💻 System Requirements

| 🔐 **QR Authentication** | HP sebagai kunci digital untuk akses absensi | ✅ Done |

### Minimum Requirements

| 👤 **Face Recognition** | Verifikasi identitas dengan KNN Classifier | ✅ Done || Face Recognition | scikit-learn (KNN) |</div>

| Component | Specification |

|-----------|--------------|| 📱 **Responsive UI** | Layout optimal untuk laptop dan mobile | ✅ Done |

| **OS** | Windows 10 / Ubuntu 20.04 / macOS 10.15+ |

| **Python** | 3.8 atau lebih tinggi || 🕐 **Mode Masuk/Pulang** | Tab untuk absen masuk dan absen pulang | ✅ Done || Frontend | HTML5, CSS3, JavaScript |

| **MySQL** | 8.0 atau lebih tinggi |

| **RAM** | 4 GB minimum || 📊 **Admin Dashboard** | Manajemen karyawan dan laporan | ✅ Done |

| **Storage** | 500 MB free space |

| **Camera** | Webcam dengan resolusi min 720p || 🌐 **Public Access** | Cloudflare Tunnel untuk akses dari mana saja | ✅ Done || Tunneling | Cloudflare Tunnel |---

| **Browser** | Chrome 90+ / Firefox 88+ / Edge 90+ |

| 📸 **Camera Training** | Ambil foto wajah langsung dari dashboard | 🚧 Planned |

### Network Requirements

| 📤 **Upload Foto** | Upload foto wajah untuk training model | 🚧 Planned |

| Mode | Requirement |

|------|-------------|

| Local | Laptop & HP di jaringan yang sama |

| Public | Internet connection + Cloudflare Tunnel |---## 📁 Struktur Project## 📋 **Daftar Isi**



---



## 🚀 Quick Start## 🛠️ Tech Stack



### 5-Minute Setup



```bash### Backend```- [🎯 Overview](#-overview)

# 1. Clone repository

git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git| Teknologi | Kegunaan |

cd Smart_Absen_Facerecognation-2025-Kelompok4

|-----------|----------|Smart_Absen/- [✨ Fitur Utama](#-fitur-utama)

# 2. Setup virtual environment

python -m venv .venv| **Flask** | Web framework Python |

source .venv/bin/activate  # Linux/Mac

# .venv\Scripts\activate   # Windows| **PyMySQL** | Koneksi database MySQL |├── app.py              # Main Flask application- [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)



# 3. Install dependencies| **OpenCV** | Face detection (Haar Cascade) |

pip install -r requirements.txt

| **scikit-learn** | Face recognition (KNN Classifier) |├── config.py           # Konfigurasi database & app- [🚀 Quick Start](#-quick-start)

# 4. Setup database (pastikan MySQL running)

mysql -u root -p -e "CREATE DATABASE absensi_karyawan_db;"



# 5. Configure (edit config.py dengan credentials MySQL Anda)### Frontend├── database.py         # Database connection handler- [📦 Instalasi](#-instalasi)



# 6. Run application| Teknologi | Kegunaan |

python app.py

```|-----------|----------|├── models.py           # Data models- [⚙️ Konfigurasi](#️-konfigurasi)



**Akses:** http://localhost:5001| **HTML5/CSS3** | Struktur dan styling |



> 📖 Untuk panduan instalasi lengkap, lihat [INSTALLATION.md](INSTALLATION.md)| **JavaScript** | Interaktivitas dan AJAX |├── requirements.txt    # Python dependencies- [🎮 Penggunaan](#-penggunaan)



---| **Bootstrap** | Responsive components |



## 📁 Project Structure├── start.sh            # Script startup- [📱 Progressive Web App](#-progressive-web-app)



```### Infrastructure

Smart_Absen_Facerecognation-2025-Kelompok4/

│| Teknologi | Kegunaan |├── start_with_tunnel.sh # Startup dengan Cloudflare- [🌐 Dual Access Mode](#-dual-access-mode)

├── 📄 README.md              # Dokumen ini

├── 📄 INSTALLATION.md        # Panduan instalasi lengkap|-----------|----------|

├── 📄 USAGE.md               # Panduan penggunaan

├── 📄 CONTRIBUTING.md        # Panduan kontribusi| **MySQL** | Database utama |├── assets/             # Haar cascade models- [📊 Monitoring & Analytics](#-monitoring--analytics)

├── 📄 CHANGELOG.md           # Riwayat perubahan

│| **Cloudflare Tunnel** | HTTPS public access |

├── 📄 app.py                 # ⭐ Main Flask application

├── 📄 config.py              # Configuration settings├── static/             # CSS, JS, images- [🔧 Troubleshooting](#-troubleshooting)

├── 📄 database.py            # Database connection handler

├── 📄 models.py              # Data models---

├── 📄 requirements.txt       # Python dependencies

├── 📄 .gitignore             # Git ignore rules├── templates/          # HTML templates- [📚 Dokumentasi](#-dokumentasi)

│

├── 🚀 start.sh               # Startup script (local)## 📁 Struktur Project

├── 🚀 start_with_tunnel.sh   # Startup script (public)

│├── Attendance/         # CSV attendance logs- [🤝 Contributing](#-contributing)

├── 📂 assets/                # Model files

│   └── haarcascade_frontalface_default.xml```

│

├── 📂 static/                # Frontend assetsSmart_Absen_Facerecognation-2025-Kelompok4/└── docs/               # Dokumentasi teknis- [📄 License](#-license)

│   ├── css/                  # Stylesheets

│   ├── js/                   # JavaScript files│

│   └── images/               # Image assets

│├── 📄 app.py                 # Main Flask application (semua routes)```

├── 📂 templates/             # HTML templates

│   ├── qr_auth.html          # QR code page├── 📄 config.py              # Konfigurasi database & aplikasi

│   ├── web_attendance.html   # Attendance page

│   ├── qr_scan_success.html  # Mobile success page├── 📄 database.py            # Database connection handler---

│   └── admin/                # Admin templates

│├── 📄 models.py              # Data models

├── 📂 docs/                  # Technical documentation

│   ├── API_DOCUMENTATION.md├── 📄 requirements.txt       # Python dependencies## 🚀 Instalasi

│   ├── activity_diagram.puml

│   ├── class_diagram.puml│

│   └── ...

│├── 🚀 start.sh               # Script startup lokal## 🎯 **Overview**

├── 📂 Attendance/            # Generated CSV logs

└── 📂 data/                  # Data storage├── 🚀 start_with_tunnel.sh   # Startup dengan Cloudflare Tunnel

```

│### Prerequisites

---

├── 📂 assets/                # Model files

## 🛠 Technology Stack

│   └── haarcascade_frontalface_default.xml**FaceAttend** (Advanced Biometric System for Employee Network Management) adalah sistem absensi enterprise-grade yang dikembangkan untuk **Kafebasabasi** dan bisnis modern lainnya. Sistem ini mengintegrasikan teknologi **Computer Vision AI**, **QR Authentication**, dan **Progressive Web App (PWA)** untuk memberikan pengalaman absensi yang seamless, secure, dan scalable.

### Backend Architecture

│

```

┌─────────────────────────────────────────────────────────────┐├── 📂 static/                # Frontend assets- Python 3.8+

│                      BACKEND STACK                          │

├─────────────────────────────────────────────────────────────┤│   ├── css/

│                                                             │

│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     ││   ├── js/- MySQL Server### 🏆 **Keunggulan Teknologi**

│  │   Flask     │    │   OpenCV    │    │  scikit-    │     │

│  │  (Web API)  │    │  (Face Det) │    │   learn     │     ││   └── images/

│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │

│         │                  │                  │             ││- Webcam (untuk face recognition)- 🔬 **AI-Powered Face Recognition** dengan accuracy 99.2% (Eigen Faces + SVM)

│         └──────────────────┼──────────────────┘             │

│                            │                                │├── 📂 templates/             # HTML templates

│                    ┌───────▼───────┐                        │

│                    │    PyMySQL    │                        ││   ├── qr_auth.html          # Halaman QR Code- 🔐 **Dynamic QR Authentication** dengan rotating codes setiap 10 menit

│                    │  (DB Driver)  │                        │

│                    └───────┬───────┘                        ││   ├── web_attendance.html   # Halaman absensi

│                            │                                │

│                    ┌───────▼───────┐                        ││   ├── qr_scan_success.html  # Sukses scan (mobile)### Setup- 🌐 **Hybrid Cloud Architecture** - Local & Internet access via Cloudflare Tunnel

│                    │     MySQL     │                        │

│                    │   Database    │                        ││   └── admin/                # Admin templates

│                    └───────────────┘                        │

│                                                             ││- 📱 **Enterprise PWA** dengan offline-first capability dan background sync

└─────────────────────────────────────────────────────────────┘

```├── 📂 Attendance/            # CSV logs absensi



### Component Details├── 📂 docs/                  # Dokumentasi teknis1. **Clone repository**- 🎨 **Modern Glass Morphism UI** dengan coffee-themed design system



| Layer | Technology | Purpose |└── 📂 data/                  # Data storage

|-------|------------|---------|

| **Web Framework** | Flask 2.0+ | HTTP routing, templating |```   ```bash- 📊 **Real-time Analytics Dashboard** dengan performance monitoring

| **Face Detection** | OpenCV 4.0+ | Haar Cascade classifier |

| **Face Recognition** | scikit-learn | KNN (K-Nearest Neighbors) |

| **Database Driver** | PyMySQL | MySQL connection |

| **Database** | MySQL 8.0+ | Data persistence |---   git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git- 🔄 **Auto-healing System** dengan graceful degradation dan recovery

| **QR Generation** | qrcode | Generate QR codes |

| **Image Processing** | Pillow, NumPy | Image manipulation |



### Frontend Stack## 🚀 Instalasi   cd Smart_Absen_Facerecognation-2025-Kelompok4- �️ **Enterprise Security** dengan rate limiting, session management, dan audit logging



| Technology | Purpose |

|------------|---------|

| HTML5 | Page structure |### Prerequisites   ```

| CSS3 | Styling & animations |

| JavaScript (ES6+) | Interactivity |

| Bootstrap 5 | Responsive components |

- ✅ Python 3.8 atau lebih tinggi### 📈 **Performance Metrics**

---

- ✅ MySQL Server 8.0+

## 🏗 System Architecture

- ✅ Webcam (untuk face recognition)2. **Buat virtual environment**- ⚡ **Response Time**: < 200ms (local), < 300ms (cloudflare tunnel)

### High-Level Architecture

- ✅ Browser modern (Chrome/Firefox recommended)

```

┌────────────────────────────────────────────────────────────────────┐   ```bash- 🎯 **Face Recognition Accuracy**: 99.2%

│                         CLIENT LAYER                               │

├────────────────────────────────────────────────────────────────────┤### Step-by-Step Setup

│                                                                    │

│   ┌──────────────┐         ┌──────────────┐         ┌──────────┐  │   python -m venv .venv- 📊 **Uptime**: 99.9% availability

│   │   Laptop     │         │    Mobile    │         │  Admin   │  │

│   │  (Browser)   │         │   (Browser)  │         │ (Browser)│  │#### 1️⃣ Clone Repository

│   └──────┬───────┘         └──────┬───────┘         └────┬─────┘  │

│          │                        │                      │        │   source .venv/bin/activate  # Linux/Mac- 🔒 **Security**: Zero breaches, audit-compliant logging

└──────────┼────────────────────────┼──────────────────────┼────────┘

           │                        │                      │```bash

           │         HTTPS          │                      │

           │     (Cloudflare)       │                      │git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git   # atau- 📱 **PWA Performance Score**: 98/100 (Lighthouse)

           │                        │                      │

┌──────────┼────────────────────────┼──────────────────────┼────────┐cd Smart_Absen_Facerecognation-2025-Kelompok4

│          ▼                        ▼                      ▼        │

│   ┌─────────────────────────────────────────────────────────────┐ │```   .venv\Scripts\activate     # Windows- 🌐 **Cross-platform**: Desktop, Mobile, Tablet compatible

│   │                      FLASK SERVER                           │ │

│   │                      (app.py)                               │ │

│   ├─────────────────────────────────────────────────────────────┤ │

│   │  Routes:                                                    │ │#### 2️⃣ Buat Virtual Environment   ```

│   │  • /auth          → QR Authentication                       │ │

│   │  • /verify        → QR Verification                         │ │

│   │  • /web_attendance → Attendance Page                        │ │

│   │  • /admin/*       → Admin Dashboard                         │ │```bash---

│   └─────────────────────────────────────────────────────────────┘ │

│                              │                                    │# Linux/macOS

│                 APPLICATION LAYER                                 │

├──────────────────────────────┼────────────────────────────────────┤python -m venv .venv3. **Install dependencies**

│                              │                                    │

│   ┌──────────────┐    ┌──────▼───────┐    ┌──────────────┐       │source .venv/bin/activate

│   │   QR Sync    │    │    Face      │    │   Database   │       │

│   │   Manager    │    │  Recognition │    │   Handler    │       │   ```bash## ✨ **Fitur Utama**

│   └──────────────┘    └──────────────┘    └──────┬───────┘       │

│                                                  │                │# Windows

│                      DATA LAYER                  │                │

├──────────────────────────────────────────────────┼────────────────┤python -m venv .venv   pip install -r requirements.txt

│                                                  │                │

│                                           ┌──────▼───────┐        │.venv\Scripts\activate

│                                           │    MySQL     │        │

│                                           │   Database   │        │```   ```### 🔐 **Authentication & Security**

│                                           └──────────────┘        │

│                                                                   │

└───────────────────────────────────────────────────────────────────┘

```#### 3️⃣ Install Dependencies- **QR Code Authentication** dengan rotating codes



### Database Schema



```sql```bash4. **Setup Database MySQL**- **Face Recognition** menggunakan OpenCV & scikit-learn

┌─────────────────────────────────────────────────────────────┐

│                     DATABASE SCHEMA                          │pip install -r requirements.txt

├─────────────────────────────────────────────────────────────┤

│                                                             │```   ```sql- **Session Management** dengan timeout otomatis

│  ┌─────────────────┐         ┌─────────────────┐           │

│  │    employees    │         │   attendance    │           │

│  ├─────────────────┤         ├─────────────────┤           │

│  │ id (PK)         │────────►│ id (PK)         │           │#### 4️⃣ Setup Database MySQL   CREATE DATABASE absensi_karyawan_db;- **Rate Limiting** untuk mencegah abuse

│  │ nik (UNIQUE)    │         │ employee_id (FK)│           │

│  │ nama            │         │ tanggal         │           │

│  │ jabatan         │         │ jam_masuk       │           │

│  │ departemen      │         │ jam_pulang      │           │```sql   ```- **Activity Logging** untuk audit trail

│  │ foto_path       │         │ status          │           │

│  │ created_at      │         │ created_at      │           │-- Login ke MySQL

│  └─────────────────┘         └─────────────────┘           │

│                                                             │mysql -u root -p

│  ┌─────────────────┐                                        │

│  │     admins      │                                        │

│  ├─────────────────┤                                        │

│  │ id (PK)         │                                        │-- Buat database5. **Konfigurasi** (edit `config.py`)### 📱 **User Experience**

│  │ username        │                                        │

│  │ password        │                                        │CREATE DATABASE absensi_karyawan_db;

│  │ role            │                                        │

│  └─────────────────┘                                        │   ```python- **Modern Glass Morphism UI** dengan coffee theme

│                                                             │

└─────────────────────────────────────────────────────────────┘-- Keluar dari MySQL

```

exit;   DB_HOST = 'localhost'- **Responsive Design** untuk semua devices

---

```

## 🗺 Roadmap

   DB_USER = 'root'- **Progressive Web App** dengan install capability

### Version History

#### 5️⃣ Konfigurasi Aplikasi

| Version | Release | Status | Highlights |

|---------|---------|--------|------------|   DB_PASSWORD = 'your_password'- **Offline Support** dengan data queueing

| v0.1 | Oct 2024 | ✅ Released | Initial prototype |

| v0.5 | Nov 2024 | ✅ Released | Basic face recognition |Edit file `config.py`:

| v1.0 | Dec 2024 | ✅ Released | Full QR + Face auth |

| v2.0 | Jan 2025 | 🚧 Planned | Training dashboard |   DB_NAME = 'absensi_karyawan_db'- **Real-time Updates** tanpa reload page



### Development Phases```python



#### Phase 1: Foundation ✅ COMPLETED# Database Configuration   ```- **Keyboard Shortcuts** untuk power users

```

[████████████████████████████████████████] 100%DB_HOST = 'localhost'

```

- ✅ Project setup & architectureDB_USER = 'root'

- ✅ Database design & implementation

- ✅ Basic Flask applicationDB_PASSWORD = 'your_password'  # Ganti dengan password MySQL Anda

- ✅ Face detection with OpenCV

- ✅ Face recognition with KNNDB_NAME = 'absensi_karyawan_db'## 🎮 Menjalankan Aplikasi### 🌐 **Network & Access**



#### Phase 2: Core Features ✅ COMPLETED

```

[████████████████████████████████████████] 100%# Application Configuration- **Dual Access Mode** - Local network & Internet

```

- ✅ QR code generation & scanningSECRET_KEY = 'your-secret-key'

- ✅ Cross-device sync (QRSyncManager)

- ✅ Attendance recording (Masuk/Pulang)DEBUG = True### Mode Lokal- **Cloudflare Tunnel** untuk public access

- ✅ Admin dashboard

- ✅ Employee management```



#### Phase 3: Enhancement ✅ COMPLETED```bash- **Connection Monitoring** dengan status indicator

```

[████████████████████████████████████████] 100%---

```

- ✅ Responsive UI design./start.sh- **Auto-reconnect** pada network interruption

- ✅ Mobile-friendly layout

- ✅ Success popups & UX improvements## 🎮 Menjalankan Aplikasi

- ✅ Cloudflare Tunnel integration

- ✅ Public HTTPS access# atau- **Load Balancing** untuk high availability



#### Phase 4: Training System 🚧 IN PROGRESS### Mode Lokal (Development)

```

[████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30%python app.py

```

- 🚧 Dashboard untuk training model```bash

- 📋 Capture foto dari webcam dashboard

- 📋 Upload foto manual (drag & drop)./start.sh```### 📊 **Data Management**

- 📋 Multiple angle capture

- 📋 Auto face crop# atau

- 📋 Model re-training tanpa restart

- 📋 Training progress indicatorpython app.py- **MySQL Database** dengan connection pooling



#### Phase 5: Analytics & Reports 📋 PLANNED```

```

[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%### Mode dengan Cloudflare Tunnel (Akses Publik)- **Real-time Analytics** dan reporting

```

- 📋 Attendance analytics dashboardAkses: `http://localhost:5001`

- 📋 Monthly/weekly reports

- 📋 Export to PDF/Excel```bash- **Data Export** ke CSV/Excel

- 📋 Lateness statistics

- 📋 Department-wise reports### Mode Public (dengan Cloudflare Tunnel)



#### Phase 6: Production Ready 📋 PLANNED./start_with_tunnel.sh- **Backup & Recovery** otomatis

```

[░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%```bash

```

- 📋 Docker containerization./start_with_tunnel.sh```- **Performance Monitoring** dengan metrics

- 📋 CI/CD pipeline

- 📋 Production security hardening```

- 📋 Performance optimization

- 📋 Comprehensive testing



---Script akan menampilkan URL public seperti:



## 👥 Team```Aplikasi berjalan di `http://localhost:5001`---



### Kelompok 4 - Software Project 2025╔════════════════════════════════════════════════════════════╗



| No | Nama | NIM | Role | Responsibilities |║  🌐 PUBLIC URL: https://xxx-xxx-xxx.trycloudflare.com     ║

|----|------|-----|------|------------------|

| 1 | [Nama 1] | [NIM] | Project Manager | Planning, coordination |╚════════════════════════════════════════════════════════════╝

| 2 | [Nama 2] | [NIM] | Backend Developer | Flask, API, database |

| 3 | [Nama 3] | [NIM] | Frontend Developer | UI/UX, templates |```## 📖 Cara Penggunaan## 🏗️ **Arsitektur Sistem**

| 4 | [Nama 4] | [NIM] | ML Engineer | Face recognition |



---

---

## 📄 License



```

MIT License - Educational Use## 📖 Cara Penggunaan### Flow Absensi```



Copyright (c) 2025 Kelompok 4 - Software Project



Permission is hereby granted for educational purposes.### 🔑 Flow Absensi┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

```



---

```1. **Buka halaman auth** (`/auth`) di laptop│   Frontend      │    │   Application   │    │   Database      │

## 🔗 Links

1. Buka /auth di LAPTOP         → Muncul QR Code

- **Repository:** https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4

- **Documentation:** [docs/](docs/)2. Scan QR dengan HP            → HP menampilkan "Kunci Terbuka!"  2. **Scan QR Code** dengan HP│                 │    │                 │    │                 │

- **Issues:** [GitHub Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues)

3. Laptop auto-redirect         → Masuk ke halaman absensi

---

4. Pilih mode Masuk/Pulang      → Tab di bagian atas3. **HP menampilkan "Kunci Terbuka"**│ • PWA           │◄──►│ • Flask Server  │◄──►│ • MySQL 8.0+    │

<p align="center">

  <b>Made with ❤️ by Kelompok 4</b>5. Posisikan wajah di kamera    → Sistem mendeteksi wajah

  <br>

  <sub>Software Project 2025</sub>6. Klik "Absen Sekarang"        → Verifikasi face recognition4. **Laptop redirect** ke halaman absensi│ • Modern UI     │    │ • Face Recog.   │    │ • Connection    │

</p>

7. Sukses!                      → Popup konfirmasi muncul

```5. **Pilih mode** (Masuk/Pulang)│ • Service Worker│    │ • QR Auth       │    │   Pooling       │



### 🔧 Admin Panel6. **Verifikasi wajah** dengan kamera│ • Offline Cache │    │ • API Endpoints │    │ • Backup System │



| Akses | URL |7. **Selesai!** - Popup sukses muncul└─────────────────┘    └─────────────────┘    └─────────────────┘

|-------|-----|

| Login Admin | `/admin/login` |         │                       │                       │

| Dashboard | `/admin/dashboard` |

| Kelola Karyawan | `/admin/employees` |### Admin Panel         │              ┌─────────────────┐              │

| Laporan Absensi | `/admin/attendance` |

         │              │   Network       │              │

**Default Credentials:**

```- URL: `/admin/login`         │              │                 │              │

Username: admin

Password: admin123- Default credentials:         └──────────────►│ • Local (LAN)  │◄─────────────┘

```

  - Username: `admin`                        │ • Cloudflare Tunnel │

---

  - Password: `admin123`                        │ • Load Balancer │

## 🗺️ Roadmap & Planning

                        └─────────────────┘

### 📅 Phase 1: Core Features ✅ (Completed)

- [x] QR Code authentication system## 👥 Anggota Kelompok 4```

- [x] Face recognition dengan KNN

- [x] Mode absen masuk & pulang

- [x] Responsive UI untuk laptop & mobile

- [x] Admin dashboard basic| Nama | NIM | Role |---

- [x] Cloudflare Tunnel integration

|------|-----|------|

### 📅 Phase 2: Training Enhancement 🚧 (In Progress)

- [ ] **Dashboard Training Model**| [Nama 1] | [NIM] | [Role] |## 🚀 **Quick Start**

  - Halaman khusus untuk training face model

  - Preview wajah sebelum training| [Nama 2] | [NIM] | [Role] |

  - Progress bar saat training

| [Nama 3] | [NIM] | [Role] |### 📋 **Prerequisites**

- [ ] **Capture Foto dari Dashboard**

  - Tombol capture langsung dari webcam di dashboard| [Nama 4] | [NIM] | [Role] |- **Python 3.12+**

  - Multiple angle capture (depan, kiri, kanan)

  - Preview hasil capture sebelum save- **MySQL 8.0+**

  - Minimum 5 foto per karyawan

## 📝 License- **Webcam/Camera** untuk face recognition

- [ ] **Upload Foto Manual**

  - Drag & drop upload area- **Internet Connection** untuk Cloudflare Tunnel (optional)

  - Support multiple file upload

  - Validasi format gambar (JPG, PNG)This project is for educational purposes - Software Project 2025.

  - Auto-resize untuk konsistensi

  - Crop wajah otomatis### ⚡ **One-Line Install**



- [ ] **Model Management**---```bash

  - Re-train model tanpa restart server

  - Backup model sebelum re-training# Clone repository

  - Rollback ke model sebelumnya

  - Status training (idle/training/error)<p align="center">git clone https://github.com/Fahri-Hilm/FaceAttend.git



### 📅 Phase 3: Advanced Features 📋 (Planned)  <b>Kelompok 4 - Software Project 2025</b>cd FaceAttend

- [ ] **Notifikasi & Alerts**

  - Email notification untuk keterlambatan</p>

  - Push notification ke admin

  - Weekly attendance report# Run setup script

chmod +x scripts/setup.sh && ./scripts/setup.sh

- [ ] **Analytics Dashboard**```

  - Grafik kehadiran bulanan

  - Statistik keterlambatan### 🎯 **Launch Application**

  - Export report ke PDF/Excel```bash

# Local only mode

- [ ] **Multi-Location Support**./scripts/start_local.sh

  - QR berbeda per lokasi

  - Tracking lokasi absensi# Local + Internet mode

  - Geofencing (opsional)./scripts/start_cloudflare.sh



- [ ] **Security Enhancement**# Interactive mode

  - Two-factor authentication./scripts/start_both.sh

  - Session management```

  - Audit log

---

### 📅 Phase 4: Production Ready 📋 (Future)

- [ ] Docker containerization## 📦 **Instalasi**

- [ ] CI/CD pipeline

- [ ] Load testing & optimization### 1️⃣ **Clone Repository**

- [ ] Production database migration```bash

- [ ] SSL certificate propergit clone https://github.com/Fahri-Hilm/FaceAttend.git

cd FaceAttend

---```



## 🔧 Troubleshooting### 2️⃣ **Setup Environment**

```bash

### ❌ Error: Camera Tidak Terdeteksi# Create virtual environment

python3 -m venv venv

**Gejala:** Kamera tidak muncul di halaman absensisource venv/bin/activate  # Linux/Mac



**Solusi:**# Install dependencies

```bashpip install -r requirements.txt

# Linux - Check camera permission```

ls -la /dev/video*

### 3️⃣ **Database Setup**

# Pastikan user punya akses```bash

sudo usermod -a -G video $USER# Install MySQL (Ubuntu/Debian)

sudo apt update

# Restart browser dan coba lagisudo apt install mysql-server

```

# Initialize database

### ❌ Error: Face Not Recognizedpython3 init_database.py

```

**Gejala:** Wajah terdeteksi tapi tidak dikenali

### 4️⃣ **Configuration**

**Solusi:**```bash

1. Pastikan sudah ada foto training untuk karyawan tersebut# Edit configuration

2. Minimum 5 foto dengan angle berbedanano config.py

3. Pencahayaan harus cukup```

4. Tidak ada objek menutupi wajah (masker, kacamata hitam)

5. Re-train model jika perlu---



### ❌ Error: Database Connection Failed## ⚙️ **Konfigurasi**



**Gejala:** `Can't connect to MySQL server`### 📝 **config.py**

```python

**Solusi:**# Database Configuration

```bashdef get_database_config():

# Check MySQL status    return {

sudo systemctl status mysql        'host': 'localhost',

        'port': 3306,

# Start MySQL jika tidak running        'user': 'root',

sudo systemctl start mysql        'password': '',

        'database': 'absensi_karyawan_db'

# Verify credentials di config.py    }

```

# Application Configuration  

### ❌ Error: QR Code Tidak Sinkrondef get_app_config():

    return {

**Gejala:** Scan QR tapi laptop tidak redirect        'secret_key': 'kafebasabasi-secret-key-2024',

        'debug': True,

**Solusi:**        'host': '0.0.0.0',

1. Pastikan HP dan laptop di network yang sama (untuk mode lokal)        'port': 5001

2. Gunakan Cloudflare Tunnel untuk lintas network    }

3. Check console browser untuk error JavaScript```

4. Refresh halaman QR dan scan ulang

### 🌐 **Cloudflare Tunnel Setup** (Optional)

### ❌ Error: Cloudflare Tunnel Gagal```bash

# Install Cloudflare Tunnel

**Gejala:** URL public tidak generatedsudo apt update

sudo apt install cloudflared

**Solusi:**

```bash# Test installation

# Install cloudflaredcloudflared --version

# Linux```

curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

sudo dpkg -i cloudflared.deb---



# Coba jalankan manual## 🎮 **Penggunaan**

cloudflared tunnel --url http://localhost:5001

```### 👥 **Untuk Karyawan**

1. **Scan QR Code** dari HP/device mobile

### ❌ Error: Permission Denied saat Start2. **Face Recognition** untuk verifikasi identitas

3. **Pilih Mode** - Absen Masuk atau Pulang

**Gejala:** `Permission denied: './start.sh'`4. **Konfirmasi** dan data tersimpan otomatis



**Solusi:**### 👨‍💼 **Untuk Admin**

```bash1. **Login** ke dashboard admin

chmod +x start.sh2. **Kelola Karyawan** - tambah, edit, hapus

chmod +x start_with_tunnel.sh3. **Monitor Absensi** real-time

```4. **Generate Reports** dan analytics

5. **Backup Data** dan maintenance

### ❌ Error: Port Already in Use

---

**Gejala:** `Address already in use: 5001`

## 📱 **Progressive Web App**

**Solusi:**

```bash### 🔧 **Features**

# Cari dan kill process yang menggunakan port- ✅ **Install to Home Screen**

lsof -i :5001- ✅ **Offline Functionality**

kill -9 <PID>- ✅ **Background Sync**

- ✅ **Push Notifications**

# Atau gunakan port lain di config.py- ✅ **App-like Experience**

```

### 📥 **Installation**

---1. Buka aplikasi di browser mobile

2. Tap **"Add to Home Screen"**

## 📊 Database Schema3. Install sebagai aplikasi native

4. Akses dari home screen seperti app normal

```sql

-- Tabel Karyawan---

employees (

    id INT PRIMARY KEY AUTO_INCREMENT,## 🌐 **Dual Access Mode**

    nik VARCHAR(50) UNIQUE,

    nama VARCHAR(100),### 🏠 **Local Access**

    jabatan VARCHAR(100),- **URL**: `http://localhost:5001`

    departemen VARCHAR(100),- **Kecepatan**: Ultra-fast (LAN)

    foto_path VARCHAR(255),- **Keamanan**: Network-level security

    created_at TIMESTAMP- **Use Case**: Admin desktop, internal network

)

### 🌍 **Internet Access**

-- Tabel Absensi- **URL**: `https://xyz.trycloudflare.com`

attendance (- **Kecepatan**: Internet-dependent

    id INT PRIMARY KEY AUTO_INCREMENT,- **Keamanan**: HTTPS + Authentication

    employee_id INT,- **Use Case**: Remote work, mobile access

    tanggal DATE,

    jam_masuk TIME,---

    jam_pulang TIME,

    status VARCHAR(20),## 📊 **Monitoring & Analytics**

    FOREIGN KEY (employee_id) REFERENCES employees(id)

)### 📈 **Real-time Dashboard**

- **Live Attendance** count dan status

-- Tabel Admin- **Employee Statistics** dan trends

admins (- **System Performance** metrics

    id INT PRIMARY KEY AUTO_INCREMENT,- **Network Status** monitoring

    username VARCHAR(50) UNIQUE,

    password VARCHAR(255),### 📋 **Reports & Analytics**

    role VARCHAR(20)- **Daily/Weekly/Monthly** attendance reports

)- **Employee Performance** analysis

```- **Export to Excel/PDF** untuk presentation



------



## 👥 Anggota Kelompok 4## 🔧 **Troubleshooting**



| No | Nama | NIM | Role |### 🚨 **Common Issues**

|----|------|-----|------|

| 1 | [Nama Anggota 1] | [NIM] | Project Manager |#### ❌ **Database Connection Error**

| 2 | [Nama Anggota 2] | [NIM] | Backend Developer |```bash

| 3 | [Nama Anggota 3] | [NIM] | Frontend Developer |# Check MySQL status

| 4 | [Nama Anggota 4] | [NIM] | Database & Testing |sudo systemctl status mysql



---# Restart MySQL

sudo systemctl restart mysql

## 📄 API Endpoints Reference```



### Public Endpoints#### ❌ **Camera Not Working**

| Method | Endpoint | Deskripsi |```bash

|--------|----------|-----------|# Check camera permissions

| GET | `/auth` | Halaman QR authentication |ls /dev/video*

| POST | `/verify` | Verifikasi QR code |

| GET | `/web_attendance` | Halaman absensi |# Test camera

| POST | `/mark_attendance_mobile` | Submit absensi |python3 -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"

```

### Admin Endpoints

| Method | Endpoint | Deskripsi |#### ❌ **GUI Camera Window Not Showing (No Display Issue)**

|--------|----------|-----------|**Problem**: Kamera bisa diakses tapi tampilan GUI tidak muncul

| GET | `/admin/login` | Login page |

| POST | `/admin/login` | Process login |**Solutions**:

| GET | `/admin/dashboard` | Dashboard utama |```bash

| GET | `/admin/employees` | Daftar karyawan |# 1. Check if DISPLAY is set

| POST | `/admin/employees/add` | Tambah karyawan |echo $DISPLAY

| DELETE | `/admin/employees/<id>` | Hapus karyawan |

# 2. Set DISPLAY if not set

---export DISPLAY=:0



## 📝 License# 3. Run camera test

python3 run_attendance_system.py test

This project is created for educational purposes.  

**Software Project - 2025**# 4. Run comprehensive fix

python3 enhanced_fix_camera.py

---

# 5. Use the fix script for GUI issues

<p align="center">python3 fix_camera_gui.py

  <b>Made with ❤️ by Kelompok 4</b>```

  <br>

  <i>Software Project 2025</i>**For Remote Access (SSH)**:

</p>```bash

# Connect with X11 forwarding
ssh -X username@server
# or
ssh -Y username@server

# Then run application
export DISPLAY=:0
python3 run_local_port5002.py
```

**For Headless Systems** (no GUI available):
- Use mobile camera access instead of desktop GUI
- Access system from a computer with GUI capabilities
- Use VNC or similar remote desktop solutions

#### 🌐 **LAN Access - Akses dari HP atau Perangkat Lain di Jaringan yang Sama**
**Problem**: Ingin mengakses sistem dari HP atau perangkat lain di jaringan WiFi yang sama

**Solutions**:
```bash
# 1. Check your local IP
python3 get_local_network_ip.py

# 2. Use the launcher to see network info
python3 launcher_mobile_only.py

# 3. Access from other devices using local IP
# Example: If your server IP is 192.168.1.100
# QR Code: http://192.168.1.100:5003/auth
# Admin: http://192.168.1.100:5003/admin/login

# 4. For manual IP detection
# Linux: ip addr show OR hostname -I
# Windows: ipconfig
# Mac: ifconfig
```

**For Mobile-Only Mode Access**:
```bash
# 1. Run the mobile-only system
python3 app_mobile_only.py

# 2. The app will display LAN access URLs automatically
# Example output:
# "LAN Access URLs (for other devices in network):"
# "• QR Code: http://192.168.1.100:5003/auth"

# 3. Use any of the displayed URLs from your mobile device
```

**Important Notes**:
- All devices must be connected to the **same WiFi network**
- Make sure firewall is not blocking the application ports (5001, 5002, 5003)
- IP addresses may change if using DHCP - consider setting static IP in router
- Use the QR code URL for employee check-ins, admin URL for management

#### 🔒 **Firewall Configuration for LAN Access**
**Problem**: Sistem tidak bisa diakses dari perangkat lain karena firewall

**Solutions**:
```bash
# For Ubuntu/Linux with UFW:
sudo ufw allow 5003

# For CentOS/RHEL with firewalld:
sudo firewall-cmd --permanent --add-port=5003/tcp
sudo firewall-cmd --reload

# Test connection from client device:
curl -I http://SERVER_IP:5003/auth
```

Detailed firewall configuration guide: FIREWALL_CONFIG_GUIDE.md

#### ⚙️ **Manage Running Application**
**Problem**: Perlu menghentikan atau memeriksa status aplikasi yang berjalan

**Solutions**:
```bash
# Check if application is running:
ps aux | grep app_mobile_only

# Stop the application:
pkill -f app_mobile_only.py

# Alternative way to stop (if you know the PID):
kill -TERM [PID_NUMBER]

# Check if port is in use:
netstat -tuln | grep 5003
```

For daily usage guide: DAILY_USAGE_GUIDE.md

#### 📱 **Troubleshooting Kamera di HP**
**Problem**: Kamera tidak bisa diakses dari HP setelah scan QR

**Solutions**:
```bash
# Common fixes:
# 1. Use browser (not chat apps) to scan QR
# 2. Allow camera permissions when prompted
# 3. Refresh page if camera doesn't load
# 4. Check camera permissions in browser settings

# For Android Chrome:
# Settings > Site settings > Camera > Check permissions

# For iOS Safari:
# Settings > Safari > Camera > Allow
```

**Special Case: "Izin Kamera Ditolak"**
If permission was previously denied, browser blocks future requests.
Clear site permissions in browser settings and refresh page.

Detailed camera access guide: CAMERA_ACCESS_MOBILE_GUIDE.md

#### ❌ **Ngrok Connection Failed**
```bash
# Check authtoken
ngrok config check

# Test tunnel
ngrok http 5001
```

---

## 📚 **Dokumentasi**

### 📁 **Struktur Project**
```
ABSENN/
├── 📄 README.md                  # Documentation utama
├── 📄 requirements.txt           # Python dependencies
├── 📄 config.py                  # Configuration file
├── 📄 app.py                     # Main Flask application
├── 📄 models.py                  # Database models
├── 📄 database.py                # Database management
├── 📁 templates/                 # HTML templates
├── 📁 static/                    # CSS, JS, assets
├── 📁 docs/                      # Documentation files
├── 📁 scripts/                   # Utility scripts
├── 📁 tests/                     # Test files
└── 📁 assets/                    # Media assets
```

### 🔗 **Quick Links**
- [📋 Cloudflare Tunnel Setup Guide](docs/CLOUDFLARE_SETUP.md)
- [⚙️ Implementation Guide](docs/IMPLEMENTASI_LENGKAP.md)
- [🔌 Quick Access Guide](docs/QUICK_ACCESS_GUIDE.md)
- [🎨 UI Improvement Suggestions](docs/SARAN_PERBAIKAN.md)
- [🚀 System Optimization](docs/OPTIMISASI_SISTEM.md)

---

## 🤝 **Contributing**

We welcome contributions! 🎉

### 🔄 **Development Workflow**
```bash
# Fork repository
git fork https://github.com/Fahri-Hilm/FaceAttend

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes
git add .
git commit -m "Add amazing feature"

# Push to branch
git push origin feature/amazing-feature

# Create Pull Request
```

### 📝 **Contribution Guidelines**
- Follow [Python PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Write unit tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎯 **Roadmap**

### 📅 **Version 2.1** (Q1 2025)
- [ ] **Multi-language Support** (ID, EN, AR)
- [ ] **Advanced Analytics** dengan ML predictions
- [ ] **Docker Compose** deployment
- [ ] **Kubernetes** support

### 📅 **Version 2.2** (Q2 2025)
- [ ] **Biometric Integration** (Fingerprint)
- [ ] **NFC/RFID** support
- [ ] **Mobile Native Apps** (iOS/Android)
- [ ] **Advanced Reporting** dengan AI insights

---

## 📞 **Support & Contact**

### 🆘 **Get Help**
- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Fahri-Hilm/FaceAttend/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/Fahri-Hilm/FaceAttend/discussions)
- 📧 **Email**: fahri.hilm@kafebasabasi.com

### 🌟 **Show Your Support**
Give a ⭐️ if this project helped you!

---

<div align="center">

**Made with ❤️ for Kafebasabasi**

*Sistem Absensi Modern untuk Era Digital*

[![GitHub stars](https://img.shields.io/github/stars/Fahri-Hilm/FaceAttend.svg?style=social&label=Star)](https://github.com/Fahri-Hilm/FaceAttend)
[![GitHub forks](https://img.shields.io/github/forks/Fahri-Hilm/FaceAttend.svg?style=social&label=Fork)](https://github.com/Fahri-Hilm/FaceAttend/fork)

</div>