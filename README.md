# Smart Absen Face Recognition 2025

Sistem absensi pintar berbasis pengenalan wajah dengan akurasi 99%+ menggunakan InsightFace/ArcFace.  
Aplikasi web Flask untuk absensi otomatis via kamera webcam dengan sinkronisasi QR code cross-device dan database MySQL.

---

## ✨ Fitur Utama

- **Face Recognition**: Haar Cascade + InsightFace (akurasi 99%+)
- **QR Sync**: Sinkronisasi absensi antar device via QR code unik
- **Camera Lock**: Pencegahan multiple detection pada 1 wajah
- **Real-time Dashboard**: Lihat status absensi live
- **CSV Export**: Log absensi dalam format Excel
- **Cloudflare Tunnel**: Akses HTTPS aman tanpa port forwarding

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|:------|:----------|
| **Backend** | Flask - PyMySQL - OpenCV - scikit-learn |
| **Frontend** | HTML5 - CSS3 - Bootstrap 5 - JavaScript |
| **Database** | MySQL 8.0+ |
| **ML** | Haar Cascade + InsightFace/ArcFace |
| **Infra** | Cloudflare Tunnel (HTTPS) |

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone repository
git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git
cd Smart_Absen_Facerecognation-2025-Kelompok4

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python database.py

# 4. Jalankan aplikasi
python app.py
```

**Akses:** http://localhost:5001

---

## 📋 Struktur Project

```
Smart_Absen/
├── app.py              # Main Flask application
├── config.py           # Database & app configuration
├── database.py         # Database initialization
├── models.py           # Data models (User, Attendance)
├── qr_sync.py          # QR cross-device synchronization
├── camera_lock.py      # Camera access control
├── requirements.txt    # Python dependencies
├── assets/             # ML models (Haar Cascade, ArcFace)
│   ├── haarcascade_frontalface_default.xml
│   └── insightface_model/
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── Attendance/         # CSV attendance logs
├── docs/               # Technical documentation
│   ├── README.md                   # Documentation hub
│   ├── ARCHITECTURE.md             # System architecture
│   ├── API_DOCUMENTATION.md        # API endpoints
│   ├── DOCSTRING_GUIDE.md          # Coding standards
│   ├── DOCUMENTATION_SUMMARY.md    # Documentation overview
│   ├── QUICK_START_DOCS.md         # Quick start guide
│   ├── openapi.yaml                # OpenAPI specification
│   └── *.puml                      # PlantUML diagrams
├── INSTALLATION.md     # Detailed setup guide
├── USAGE.md            # User guide
├── CONTRIBUTING.md     # Contribution guidelines
└── CHANGELOG.md        # Version history
```

---

## 📖 Dokumentasi Lengkap

### 📚 Dokumentasi Utama

| Dokumen | Deskripsi | Link |
|:--------|:----------|:-----|
| 📖 **Installation Guide** | Panduan instalasi lengkap step-by-step | [INSTALLATION.md](INSTALLATION.md) |
| 📘 **User Guide** | Panduan penggunaan sistem | [USAGE.md](USAGE.md) |
| 🏗️ **Architecture** | System architecture & design patterns | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 🔌 **API Documentation** | REST API endpoints & examples | [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) |
| 📝 **Docstring Guide** | Coding standards & templates | [docs/DOCSTRING_GUIDE.md](docs/DOCSTRING_GUIDE.md) |
| 🤝 **Contributing** | Panduan kontribusi | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 📋 **Changelog** | Riwayat perubahan versi | [CHANGELOG.md](CHANGELOG.md) |

### 🎯 Dokumentasi Teknis

| Dokumen | Deskripsi | Link |
|:--------|:----------|:-----|
| 📊 **OpenAPI Spec** | OpenAPI 3.0 specification | [docs/openapi.yaml](docs/openapi.yaml) |
| 🎨 **Architecture Diagram** | Draw.io system diagrams | [docs/architecture_diagram.drawio](docs/architecture_diagram.drawio) |
| 📐 **PlantUML Diagrams** | Sequence, class, deployment diagrams | [docs/*.puml](docs/) |
| 📚 **Documentation Hub** | Pusat dokumentasi lengkap | [docs/README.md](docs/README.md) |
| 📄 **Documentation Summary** | Ringkasan dokumentasi | [docs/DOCUMENTATION_SUMMARY.md](docs/DOCUMENTATION_SUMMARY.md) |
| ⚡ **Quick Start Docs** | Quick reference guide | [docs/QUICK_START_DOCS.md](docs/QUICK_START_DOCS.md) |

### 🌐 Dokumentasi Online

| Resource | URL |
|:---------|:----|
| **Swagger UI** | http://localhost:5001/api/docs |
| **API Health Check** | http://localhost:5001/health |
| **GitHub Repository** | https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4 |

---

## 🔧 Environment Variables

Buat file `.env` di root project:

```
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=smart_absen

# App
SECRET_KEY=your-secret-key
FLASK_ENV=production
PORT=5001

# ML Config
FACE_CONFIDENCE=0.6
MAX_FACES=1
```

---

## 🌐 Deployment

### Docker (Recommended)

```bash
docker build -t smart-absen .
docker run -p 5001:5001 --env-file .env smart-absen
```

### VPS/Cloud

1. Install MySQL 8.0+
2. Setup Cloudflare Tunnel untuk HTTPS
3. `gunicorn app:app -w 4 -b 0.0.0.0:5001`
4. PM2/Nginx untuk production

Detail lengkap: [INSTALLATION.md](INSTALLATION.md)

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| GET | `/` | Dashboard utama |
| POST | `/api/attendance` | Proses absensi wajah |
| GET | `/api/attendance` | List riwayat absensi |
| GET | `/qr` | Generate QR sync code |
| GET | `/api/docs` | Swagger UI documentation |
| GET | `/health` | Health check endpoint |

**Full API Documentation:** [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) atau http://localhost:5001/api/docs

---

## 🐛 Troubleshooting

| Issue | Solution |
|:------|:---------|
| "No module named 'cv2'" | `pip install opencv-python` |
| Camera tidak terdeteksi | Cek permission webcam di browser |
| MySQL connection failed | Verifikasi `.env` dan jalankan `database.py` |
| Face recognition lambat | Gunakan model ringan atau GPU |

**Troubleshooting lengkap:** [INSTALLATION.md](INSTALLATION.md#troubleshooting)

---

## 📈 Demo & Metrics

- **Akurasi**: 99.2% pada dataset internal (500+ wajah)
- **FPS**: 15-25 fps pada CPU i5 gen 10
- **Latency**: <2 detik per absensi

---

## 🤝 Contributing

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

**Code Style**: Black formatter, PEP8

**Panduan lengkap:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License - lihat [LICENSE](LICENSE)

---

## 👥 Tim Pengembang

**Kelompok 4 - Software Project 2025**  
Fahri Hilmi - Lead Developer

---

## 📞 Support & Links

- 📖 **Documentation Hub**: [docs/README.md](docs/README.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues)
- ⭐ **Star**: [GitHub Repository](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4)
- 🔀 **Fork**: [GitHub Fork](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/fork)

---

<div align="center">
<sub>Built with ❤️ for efisiensi absensi Indonesia</sub>
</div>
