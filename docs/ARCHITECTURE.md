# Architecture Documentation - Smart Absen

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Laptop Browser          │         Mobile Browser              │
│  (QR Display + Face)     │         (QR Scanner)                │
└──────────────┬───────────┴──────────────┬──────────────────────┘
               │                          │
               └──────────┬───────────────┘
                          │ HTTPS
               ┌──────────▼──────────────────────────────────────┐
               │      APPLICATION LAYER (Flask)                  │
               ├─────────────────────────────────────────────────┤
               │  • QR Auth Module (qr_sync.py)                  │
               │  • Face Recognition (OpenCV + InsightFace)      │
               │  • Camera Lock Manager (camera_lock.py)         │
               │  • Route Handlers (app.py)                      │
               └──────────┬──────────────────────────────────────┘
                          │
               ┌──────────▼──────────────────────────────────────┐
               │      DATA LAYER                                 │
               ├─────────────────────────────────────────────────┤
               │  MySQL Database  │  CSV Logs  │  ML Models      │
               │  (database.py)   │ (Attendance/) │ (assets/)    │
               └─────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Application Core (app.py)

**Responsibilities:**
- Route handling
- Request/response processing
- Session management
- Integration orchestration

**Key Routes:**
- `/auth` - QR authentication page
- `/verify_qr` - QR verification endpoint
- `/web_attendance` - Face recognition page
- `/process_attendance` - Attendance processing
- `/admin/*` - Admin dashboard routes

### 2. QR Sync Module (qr_sync.py)

**Purpose:** Cross-device authentication synchronization

```python
QRSyncManager
├── generate_qr_code()      # Generate QR with unique token
├── verify_qr_code()        # Validate scanned QR
├── cleanup_expired()       # Remove expired tokens
└── get_verification_status() # Check if verified
```

**Data Flow:**
```
Laptop → Generate QR → Display
Mobile → Scan QR → Verify → Update status
Laptop → Poll status → Redirect on success
```

### 3. Face Recognition Pipeline

**Detection:** Haar Cascade (OpenCV)
**Recognition:** InsightFace/ArcFace (99%+ accuracy)

```
Camera Frame → Face Detection → Face Alignment → 
Feature Extraction → KNN Matching → Identity
```

**Files:**
- `assets/haarcascade_frontalface_default.xml` - Detector
- `assets/model_knn.pkl` - Recognition model

### 4. Camera Lock Manager (camera_lock.py)

**Purpose:** Prevent concurrent camera access

```python
CameraLock
├── acquire()    # Lock camera for process
├── release()    # Release camera
└── is_locked()  # Check lock status
```

### 5. Database Layer (database.py)

**Schema:**

```sql
-- Karyawan Table
CREATE TABLE karyawan (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nama VARCHAR(100),
    jabatan VARCHAR(50),
    created_at TIMESTAMP
);

-- Absensi Table
CREATE TABLE absensi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    karyawan_id INT,
    tanggal DATE,
    jam_masuk TIME,
    jam_pulang TIME,
    status ENUM('Hadir', 'Terlambat', 'Izin', 'Sakit'),
    FOREIGN KEY (karyawan_id) REFERENCES karyawan(id)
);

-- QR Tokens Table
CREATE TABLE qr_tokens (
    token VARCHAR(64) PRIMARY KEY,
    created_at TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    expires_at TIMESTAMP
);
```

## Data Flow Diagrams

### Attendance Flow

```
┌─────────┐
│ START   │
└────┬────┘
     │
     ▼
┌─────────────────┐
│ Open /auth      │
│ (Laptop)        │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Generate QR     │
│ + Access Code   │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Scan QR (Mobile)│
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Verify Token    │
│ in Database     │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Redirect Laptop │
│ to /web_attendance
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Capture Face    │
│ from Webcam     │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Detect Face     │
│ (Haar Cascade)  │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Recognize Face  │
│ (InsightFace)   │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Save to DB      │
│ + CSV Log       │
└────┬────────────┘
     │
     ▼
┌─────────┐
│  DONE   │
└─────────┘
```

## Security Architecture

### Authentication Layers

1. **QR Token Validation**
   - 64-char random token
   - 10-minute expiration
   - One-time use

2. **Face Verification**
   - Liveness detection (planned)
   - 99%+ accuracy threshold
   - Anti-spoofing (planned)

3. **Session Management**
   - Flask session cookies
   - HTTPS only (production)

### Data Protection

- Passwords: Hashed (bcrypt)
- Face embeddings: Encrypted storage (planned)
- API tokens: Environment variables

## Deployment Architecture

### Development

```
localhost:5001 → Flask Dev Server → MySQL (localhost)
```

### Production (Cloudflare Tunnel)

```
Internet → Cloudflare Tunnel → Flask (Gunicorn) → MySQL
```

**Benefits:**
- HTTPS encryption
- DDoS protection
- No port forwarding needed

## Performance Considerations

### Bottlenecks

| Component | Latency | Optimization |
|-----------|---------|--------------|
| Face Detection | ~100ms | Use GPU acceleration |
| Face Recognition | ~200ms | Batch processing |
| Database Query | ~50ms | Connection pooling |
| QR Generation | ~10ms | Cache QR images |

### Scalability

**Current:** Single-threaded Flask
**Future:** 
- Gunicorn workers (4-8)
- Redis for session storage
- Load balancer

## Technology Decisions

### Why Flask?
- Lightweight
- Easy integration with OpenCV
- Python ML ecosystem

### Why MySQL?
- ACID compliance
- Relational data (employees ↔ attendance)
- Mature ecosystem

### Why InsightFace?
- State-of-the-art accuracy (99%+)
- Pre-trained models
- Active development

### Why Cloudflare Tunnel?
- Free HTTPS
- No firewall configuration
- Built-in security

## Future Architecture

### Phase 2: Microservices (Planned)

```
API Gateway → Auth Service
           → Face Recognition Service
           → Attendance Service
           → Notification Service
```

### Phase 3: Cloud Native (Planned)

- AWS Lambda for face processing
- RDS for database
- S3 for face images
- CloudFront CDN

---

**Last Updated:** 2025-12-07  
**Version:** 1.0
