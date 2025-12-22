# Multi-stage build untuk optimasi ukuran image
FROM python:3.10-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Install InsightFace dengan dependencies
RUN pip install --no-cache-dir --user \
    insightface==0.7.3 \
    onnxruntime==1.16.3 \
    mxnet==1.9.1

# Final stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libgl1 \
    libgtk-3-0 \
    libopenblas0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages dari builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Create directories
RUN mkdir -p logs Attendance face_data assets/insightface_model

# Download InsightFace model jika belum ada
RUN python -c "
import os
import insightface
from insightface.app import FaceAnalysis

# Download dan setup model
if not os.path.exists('assets/insightface_model'):
    os.makedirs('assets/insightface_model', exist_ok=True)
    
# Initialize model (akan auto-download)
try:
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    print('InsightFace model berhasil didownload dan disetup')
except Exception as e:
    print(f'Error setup InsightFace: {e}')
"

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5001/health', timeout=5)" || exit 1

# Run application
CMD ["python", "app.py"]
