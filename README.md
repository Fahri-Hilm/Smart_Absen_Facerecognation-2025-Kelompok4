# Smart Absen Face Recognition 2025

Sistem absensi pintar berbasis pengenalan wajah dengan akurasi 99%+ menggunakan InsightFace/ArcFace.  
Aplikasi web Flask untuk absensi otomatis via kamera webcam dengan sinkronisasi QR code cross-device dan database MySQL.

**Version:** 2.1 | **Status:** Production Ready ✅ | **Security Score:** 9/10 🛡️

---

## 📸 Screenshots & Demo

<table>
  <tr>
    <td width="50%">
      <h3 align="center">Face Recognition - Absensi Wajah</h3>
      <img src="https://i.imgur.com/3yTqzba.png" alt="Face Recognition" width="100%"/>
      <p align="center"><em>Deteksi wajah otomatis dengan akurasi 99%+ menggunakan InsightFace</em></p>
    </td>
    <td width="50%">
      <h3 align="center">QR Code Sync</h3>
      <img src="https://i.imgur.com/AQsO5Q6.png" alt="QR Sync" width="100%"/>
      <p align="center"><em>Sinkronisasi absensi cross-device via QR code unik</em></p>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <h3 align="center">Dashboard Admin</h3>
      <img src="https://i.imgur.com/MBgDed4.png" alt="Dashboard Admin" width="100%"/>
      <p align="center"><em>Manajemen karyawan dan laporan absensi</em></p>
    </td>
  </tr>
</table>

---

## ✨ Fitur Utama

- **Face Recognition**: InsightFace/ArcFace (akurasi 99%+)
- **QR Sync**: Sinkronisasi absensi antar device via QR code unik
- **Camera Lock**: Pencegahan multiple detection pada 1 wajah
- **Real-time Dashboard**: Lihat status absensi live
- **CSV Export**: Log absensi dalam format Excel
- **Security**: Environment variables, input validation, error handling
- **Docker Ready**: One-command deployment with CI/CD
- **Cloudflare Tunnel**: Akses HTTPS aman tanpa port forwarding

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|:------|:----------|
| **Backend** | Flask 2.3.3 - PyMySQL - OpenCV - scikit-learn |
| **Frontend** | HTML5 - CSS3 - Bootstrap 5 - Vanilla JavaScript |
| **Database** | MySQL 8.0+ |
| **ML** | InsightFace/ArcFace (99%+ accuracy) |
| **Security** | python-dotenv - Flask-WTF - Flask-Limiter |
| **Infra** | Cloudflare Tunnel (HTTPS) |

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone repository
git clone https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git
cd Smart_Absen_Facerecognation-2025-Kelompok4

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
nano .env  # Edit with your database credentials

# 4. Setup database
python database.py

# 5. Jalankan aplikasi
python app.py
```

**Akses:** http://localhost:5001

---

## 📋 Struktur Project

```
Smart_Absen/
├── app.py              # Main Flask application
├── config.py           # Database & app configuration (with .env support)
├── database.py         # Database initialization
├── models.py           # Data models (User, Attendance)
├── helpers.py          # API response standardization ✨ NEW
├── validators.py       # Input validation decorators ✨ NEW
├── qr_sync.py          # QR cross-device synchronization
├── camera_lock.py      # Camera access control
├── requirements.txt    # Python dependencies (updated)
├── .env.example        # Environment variables template ✨ NEW
├── .env                # Environment configuration (create from .env.example)
├── assets/             # ML models (Haar Cascade, ArcFace)
│   ├── haarcascade_frontalface_default.xml
│   └── insightface_model/
├── static/             # CSS, JS, images
│   ├── css/
│   │   └── theme.css   # Centralized theme styles
│   └── js/
│       └── capture-simple.js  # Face capture module ✨ NEW
├── templates/          # HTML templates
│   ├── base.html       # Base template ✨ NEW
│   ├── admin_base.html # Admin base template ✨ NEW
│   ├── error.html      # Error page template ✨ NEW
│   └── ...
├── logs/               # Application logs ✨ NEW
├── Attendance/         # CSV attendance logs
├── docs/               # Technical documentation
│   ├── README.md                   # Documentation hub
│   ├── ARCHITECTURE.md             # System architecture
│   ├── API_DOCUMENTATION.md        # API endpoints
│   ├── UI_UX_IMPROVEMENTS.md       # UI/UX improvements ✨ NEW
│   ├── FRONTEND_IMPROVEMENTS.md    # Frontend improvements ✨ NEW
│   ├── COMPONENT_REFERENCE.md      # Component reference ✨ NEW
│   ├── TEMPLATE_ARCHITECTURE.md    # Template structure ✨ NEW
│   └── ...
├── SECURITY_IMPROVEMENTS.md  # Security guide ✨ NEW
├── VERIFICATION_REPORT.txt   # Verification report ✨ NEW
├── INSTALLATION.md     # Detailed setup guide
├── USAGE.md            # User guide
├── CONTRIBUTING.md     # Contribution guidelines
└── CHANGELOG.md        # Version history
```

---

## 📖 Dokumentasi

| Dokumen | Deskripsi |
|---------|-----------|
| 📖 [INSTALLATION.md](INSTALLATION.md) | Panduan instalasi lengkap |
| 📘 [USAGE.md](USAGE.md) | Panduan penggunaan sistem |
| 🔒 [SECURITY.md](SECURITY.md) | Security best practices |
| ✅ [STATUS.md](STATUS.md) | System status & verification |
| 🏗️ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| 🔌 [docs/API.md](docs/API.md) | REST API documentation |
| 💻 [docs/FRONTEND.md](docs/FRONTEND.md) | Frontend development guide |
| 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| 📋 [CHANGELOG.md](CHANGELOG.md) | Version history |

**Documentation Hub:** [docs/README.md](docs/README.md)

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

### Docker (Recommended) 🐳

```bash
# Local development
docker-compose up -d

# Production (pull from GHCR)
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
docker run -d -p 5001:5001 --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/face_data:/app/face_data \
  ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
```

**Docker Hub:** `ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4`

### VPS/Cloud

1. Install MySQL 8.0+
2. Setup Cloudflare Tunnel untuk HTTPS
3. `gunicorn app:app -w 4 -b 0.0.0.0:5001`
4. PM2/Nginx untuk production

**Detail lengkap:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) | [INSTALLATION.md](INSTALLATION.md)

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
