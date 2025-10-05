# 🚀 Deployment Guide - ABSENN

## 📋 **Overview**

Panduan deployment lengkap untuk ABSENN (Advanced Biometric System for Employee Network Management) dalam berbagai environment: Development, Staging, dan Production.

---

## 🏗️ **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   CDN/      │    │  Load       │    │  Application│     │
│  │   Cloudflare│◄──►│  Balancer   │◄──►│  Servers    │     │
│  │             │    │  (Nginx)    │    │  (Flask)    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                             │                  │            │
│                             ▼                  ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Ngrok     │    │  Database   │    │  Redis      │     │
│  │   Tunnel    │    │  (MySQL)    │    │  Cache      │     │
│  │             │    │             │    │             │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Requirements**

### 🖥️ **System Requirements**

#### Minimum (Development)
- **OS**: Ubuntu 20.04+ / CentOS 8+ / macOS 11+
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 10 GB SSD
- **Python**: 3.12+
- **MySQL**: 8.0+

#### Recommended (Production)
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 4 cores, 3.0 GHz
- **RAM**: 8 GB
- **Storage**: 50 GB SSD
- **Python**: 3.12+
- **MySQL**: 8.0+
- **Redis**: 7.0+ (for caching)
- **Nginx**: 1.20+ (reverse proxy)

---

## 🚀 **Deployment Methods**

### 1️⃣ **Quick Deployment (Development)**

#### Auto Setup Script
```bash
# Clone repository
git clone https://github.com/Fahri-Hilm/ABSENN.git
cd ABSENN

# Run one-command setup
chmod +x scripts/quick_deploy.sh
./scripts/quick_deploy.sh
```

#### Manual Setup
```bash
# 1. Python Environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Database setup
sudo mysql -u root -p
CREATE DATABASE absensi_karyawan_db;
python3 init_database.py

# 4. Configuration
cp config.py.example config.py
nano config.py

# 5. Run application
python3 app.py
```

---

### 2️⃣ **Docker Deployment**

#### Create Dockerfile
```dockerfile
# Create Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 absenn && chown -R absenn:absenn /app
USER absenn

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5001/health || exit 1

# Run application
CMD ["python", "app.py"]
```

#### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  absenn-app:
    build: .
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - DATABASE_HOST=absenn-db
      - DATABASE_USER=absenn
      - DATABASE_PASSWORD=secure_password
      - DATABASE_NAME=absensi_karyawan_db
    depends_on:
      - absenn-db
      - absenn-redis
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - absenn-network

  absenn-db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=absensi_karyawan_db
      - MYSQL_USER=absenn
      - MYSQL_PASSWORD=secure_password
    volumes:
      - mysql_data:/var/lib/mysql
      - ./db_init:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"
    restart: unless-stopped
    networks:
      - absenn-network

  absenn-redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - absenn-network

  absenn-nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - absenn-app
    restart: unless-stopped
    networks:
      - absenn-network

volumes:
  mysql_data:
  redis_data:

networks:
  absenn-network:
    driver: bridge
```

#### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f absenn-app

# Scale application
docker-compose up -d --scale absenn-app=3
```

---

### 3️⃣ **Cloud Deployment**

#### AWS EC2 Deployment
```bash
# 1. Launch EC2 instance (Ubuntu 22.04 LTS)
# 2. Configure security groups (ports 22, 80, 443, 5001)
# 3. Connect to instance

# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv mysql-server nginx -y

# Clone and setup
git clone https://github.com/Fahri-Hilm/ABSENN.git
cd ABSENN
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure MySQL
sudo mysql_secure_installation
sudo mysql -u root -p
CREATE DATABASE absensi_karyawan_db;
CREATE USER 'absenn'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON absensi_karyawan_db.* TO 'absenn'@'localhost';
FLUSH PRIVILEGES;

# Initialize database
python3 init_database.py

# Configure Nginx
sudo cp nginx/absenn.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/absenn.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Setup systemd service
sudo cp scripts/absenn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable absenn
sudo systemctl start absenn
```

#### Digital Ocean Droplet
```bash
# Create droplet via CLI
doctl compute droplet create absenn-prod \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --region sgp1 \
  --ssh-keys your-ssh-key-id

# Follow AWS EC2 steps above
```

---

### 4️⃣ **Kubernetes Deployment**

#### Kubernetes Manifests
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: absenn

---
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: absenn-app
  namespace: absenn
spec:
  replicas: 3
  selector:
    matchLabels:
      app: absenn-app
  template:
    metadata:
      labels:
        app: absenn-app
    spec:
      containers:
      - name: absenn
        image: fahrihilm/absenn:latest
        ports:
        - containerPort: 5001
        env:
        - name: DATABASE_HOST
          value: "absenn-mysql"
        - name: DATABASE_USER
          valueFrom:
            secretKeyRef:
              name: absenn-secrets
              key: db-user
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: absenn-secrets
              key: db-password
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5001
          initialDelaySeconds: 5
          periodSeconds: 5

---
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: absenn-service
  namespace: absenn
spec:
  selector:
    app: absenn-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5001
  type: ClusterIP

---
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: absenn-ingress
  namespace: absenn
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - absenn.yourdomain.com
    secretName: absenn-tls
  rules:
  - host: absenn.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: absenn-service
            port:
              number: 80
```

#### Deploy to Kubernetes
```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n absenn
kubectl get services -n absenn
kubectl get ingress -n absenn

# Scale deployment
kubectl scale deployment absenn-app --replicas=5 -n absenn
```

---

## ⚙️ **Environment Configuration**

### Development Environment
```python
# config.py
class DevelopmentConfig:
    DEBUG = True
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = 3306
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = ''
    DATABASE_NAME = 'absensi_karyawan_db'
    SECRET_KEY = 'dev-secret-key-2024'
    NGROK_ENABLED = True
    NGROK_AUTH_TOKEN = 'your-ngrok-token'
    LOG_LEVEL = 'DEBUG'
```

### Production Environment
```python
# config.py
class ProductionConfig:
    DEBUG = False
    DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE_PORT = int(os.environ.get('DATABASE_PORT', 3306))
    DATABASE_USER = os.environ.get('DATABASE_USER', 'absenn')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'absensi_karyawan_db')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    NGROK_ENABLED = os.environ.get('NGROK_ENABLED', 'false').lower() == 'true'
    NGROK_AUTH_TOKEN = os.environ.get('NGROK_AUTH_TOKEN')
    LOG_LEVEL = 'INFO'
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
```

---

## 🔒 **Security Configuration**

### SSL/TLS Setup
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration
```bash
# UFW setup
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 3306  # MySQL (internal only)
```

### Environment Variables
```bash
# Production environment variables
export FLASK_ENV=production
export SECRET_KEY="your-super-secret-key-here"
export DATABASE_PASSWORD="secure-database-password"
export NGROK_AUTH_TOKEN="your-ngrok-auth-token"
export LOG_LEVEL=INFO
```

---

## 📊 **Monitoring & Logging**

### Logging Configuration
```python
# Enhanced logging
import logging
from logging.handlers import RotatingFileHandler

# Setup rotating logs
handler = RotatingFileHandler('logs/absenn.log', maxBytes=10000000, backupCount=5)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
```

### Health Monitoring
```bash
# Setup monitoring script
#!/bin/bash
# scripts/health_monitor.sh

URL="http://localhost:5001/health"
WEBHOOK_URL="https://hooks.slack.com/your-webhook"

if ! curl -f $URL > /dev/null 2>&1; then
    curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"🚨 ABSENN is DOWN!"}' \
        $WEBHOOK_URL
fi
```

### Performance Monitoring
```python
# Add to app.py
from flask import g
import time

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    app.logger.info(f'Request took {duration:.2f}s')
    return response
```

---

## 🚀 **CI/CD Pipeline**

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy ABSENN

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /opt/absenn
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart absenn
```

---

## 📋 **Deployment Checklist**

### Pre-deployment
- [ ] Code review completed
- [ ] Unit tests passing (100% coverage)
- [ ] Integration tests passing
- [ ] Security scan completed
- [ ] Performance testing done
- [ ] Documentation updated
- [ ] Database migrations prepared
- [ ] Backup strategy confirmed

### Deployment
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database credentials secured
- [ ] Firewall rules configured
- [ ] Monitoring setup completed
- [ ] Health checks configured
- [ ] Logging configured
- [ ] Error tracking setup

### Post-deployment
- [ ] Application accessible
- [ ] Database connectivity verified
- [ ] Face recognition working
- [ ] QR authentication functional
- [ ] Ngrok tunnel active (if enabled)
- [ ] Performance metrics normal
- [ ] Error logs clean
- [ ] Backup verification

---

## 🔧 **Maintenance**

### Regular Tasks
```bash
# Weekly maintenance script
#!/bin/bash
# scripts/weekly_maintenance.sh

echo "Starting weekly maintenance..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean up logs
find /var/log -name "*.log" -mtime +30 -delete

# Database maintenance
mysql -u absenn -p absensi_karyawan_db -e "OPTIMIZE TABLE karyawan, absensi;"

# Restart services
sudo systemctl restart absenn nginx mysql

echo "Weekly maintenance completed"
```

### Backup Strategy
```bash
# Daily backup script
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/absenn"

# Database backup
mysqldump -u absenn -p absensi_karyawan_db > $BACKUP_DIR/db_$DATE.sql

# Application backup
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/absenn

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

---

## 🆘 **Troubleshooting**

### Common Issues

#### Application Won't Start
```bash
# Check logs
journalctl -u absenn -f

# Check dependencies
source venv/bin/activate
pip check

# Check database connection
mysql -u absenn -p absensi_karyawan_db -e "SELECT 1;"
```

#### High Memory Usage
```bash
# Monitor memory
htop
free -h

# Check for memory leaks
ps aux --sort=-%mem | head -20

# Restart if necessary
sudo systemctl restart absenn
```

#### Database Connection Issues
```bash
# Check MySQL status
sudo systemctl status mysql

# Check connections
mysql -u root -p -e "SHOW PROCESSLIST;"

# Check configuration
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

---

## 📞 **Support & Contact**

### Production Support
- **Emergency**: +62-XXX-XXX-XXXX
- **Email**: support@ABSENN.com
- **Slack**: #absenn-support

### DevOps Team
- **Lead**: Fahri Hilmi
- **Email**: fahri.hilm@ABSENN.com
- **GitHub**: @Fahri-Hilm

---

**Last Updated**: October 5, 2025  
**Version**: 2.0.1  
**Environment**: Production Ready