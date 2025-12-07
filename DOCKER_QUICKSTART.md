# Docker Quick Reference 🐳

## 🚀 One-Command Deploy

```bash
# Login to GHCR (one-time setup)
echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u fahri-hilm --password-stdin

# Build & Push
./deploy.sh 2.0
```

---

## 📦 Common Commands

### Build
```bash
docker build -t smart-absen:2.0 .
```

### Run Locally
```bash
docker run -d -p 5001:5001 --env-file .env smart-absen:2.0
```

### Push to GHCR
```bash
docker tag smart-absen:2.0 ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:2.0
docker push ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:2.0
```

### Pull from GHCR
```bash
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
```

---

## 🔧 Docker Compose

### Development
```bash
docker-compose up -d          # Start
docker-compose logs -f app    # View logs
docker-compose down           # Stop
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Debug

```bash
# View logs
docker logs -f smart-absen

# Enter container
docker exec -it smart-absen bash

# Check health
curl http://localhost:5001/health

# Container stats
docker stats smart-absen
```

---

## 🔄 Update

```bash
# Pull latest
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest

# Restart
docker stop smart-absen && docker rm smart-absen
docker run -d -p 5001:5001 --env-file .env \
  ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
```

---

## 📊 Image Info

```bash
# List images
docker images | grep smart-absen

# Image size
docker images smart-absen:2.0 --format "{{.Size}}"

# Image history
docker history smart-absen:2.0
```

---

**Full Guide:** [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)
