# Docker Deployment Guide

## 🐳 Quick Start

### Local Development with Docker Compose

```bash
# 1. Build and run
docker-compose up -d

# 2. Check logs
docker-compose logs -f app

# 3. Stop
docker-compose down
```

**Access:** http://localhost:5001

---

## 📦 Build & Push to GitHub Container Registry

### Prerequisites

1. **GitHub Personal Access Token** dengan scope `write:packages`
   - Go to: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select: `write:packages`, `read:packages`, `delete:packages`

2. **Login to GHCR**

```bash
export CR_PAT=YOUR_TOKEN_HERE
echo $CR_PAT | docker login ghcr.io -u fahri-hilm --password-stdin
```

### Manual Build & Push

```bash
# 1. Build image
docker build -t smart-absen:2.0 .

# 2. Tag for GHCR (lowercase username required)
docker tag smart-absen:2.0 ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:2.0
docker tag smart-absen:2.0 ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# 3. Push to GHCR
docker push ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:2.0
docker push ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
```

### Automated Build (GitHub Actions)

GitHub Actions akan otomatis build & push saat:
- Push ke branch `main` → tag `latest`
- Push tag `v*` (e.g., `v2.0.0`) → tag `2.0.0`, `2.0`, `latest`

```bash
# Trigger automated build
git tag v2.0.0
git push origin v2.0.0
```

**Check build status:** https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/actions

---

## 🚀 Production Deployment

### Option 1: VPS/Cloud Server

```bash
# 1. Pull image from GHCR
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# 2. Create .env file
cat > .env << EOF
DB_HOST=your-mysql-host
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=smart_absen
SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
PORT=5001
EOF

# 3. Run container
docker run -d \
  --name smart-absen \
  -p 5001:5001 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/Attendance:/app/Attendance \
  -v $(pwd)/face_data:/app/face_data \
  --restart unless-stopped \
  ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# 4. Check logs
docker logs -f smart-absen
```

### Option 2: Docker Compose (Production)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
    ports:
      - "5001:5001"
    env_file: .env
    volumes:
      - ./logs:/app/logs
      - ./Attendance:/app/Attendance
      - ./face_data:/app/face_data
    restart: unless-stopped
```

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔧 Troubleshooting

### Image Size Too Large

```bash
# Check image size
docker images smart-absen:2.0

# Expected: ~800MB (Python + OpenCV + ML models)
```

### Container Won't Start

```bash
# Check logs
docker logs smart-absen

# Common issues:
# - Missing .env file
# - Database connection failed
# - Port 5001 already in use
```

### Database Connection Failed

```bash
# If using external MySQL, ensure:
# 1. MySQL allows remote connections
# 2. Firewall allows port 3306
# 3. DB_HOST in .env is correct IP/hostname

# Test connection from container
docker exec -it smart-absen python -c "from database import get_db_manager; print(get_db_manager())"
```

### Permission Issues

```bash
# Fix volume permissions
sudo chown -R 1000:1000 logs Attendance face_data
```

---

## 📊 Monitoring

### Health Check

```bash
# Manual check
curl http://localhost:5001/health

# Expected response:
# {"status":"healthy","timestamp":"2025-12-07T18:21:00","database":"connected"}
```

### Container Stats

```bash
# Real-time stats
docker stats smart-absen

# Expected usage:
# CPU: 5-15% (idle), 30-60% (active face recognition)
# Memory: 400-800MB
```

---

## 🔒 Security Notes

1. **Never commit .env** - Already in .gitignore
2. **Use secrets management** in production (AWS Secrets Manager, HashiCorp Vault)
3. **Enable HTTPS** via reverse proxy (Nginx, Cloudflare Tunnel)
4. **Limit container resources**:

```bash
docker run -d \
  --memory="1g" \
  --cpus="2" \
  --name smart-absen \
  ...
```

---

## 📦 Image Visibility

By default, GHCR images are **private**. To make public:

1. Go to: https://github.com/users/fahri-hilm/packages/container/smart_absen_facerecognation-2025-kelompok4/settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" → Public

---

## 🔄 Update Deployment

```bash
# Pull latest image
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# Restart container
docker-compose down
docker-compose up -d

# Or with docker run
docker stop smart-absen
docker rm smart-absen
docker run -d ... # (same command as before)
```

---

## 📝 CI/CD Pipeline

Current workflow (`.github/workflows/docker-publish.yml`):

1. **Trigger**: Push to `main` or tag `v*`
2. **Build**: Multi-stage Docker build
3. **Push**: To GHCR with tags
4. **Notify**: Check Actions tab for status

**Customize workflow**: Edit `.github/workflows/docker-publish.yml`

---

## 🎯 Next Steps

- [ ] Setup Kubernetes deployment (k8s manifests)
- [ ] Add Docker health check monitoring (Prometheus)
- [ ] Implement blue-green deployment
- [ ] Setup CDN for static assets
- [ ] Add container scanning (Trivy, Snyk)

---

**Need help?** Open issue: https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues
