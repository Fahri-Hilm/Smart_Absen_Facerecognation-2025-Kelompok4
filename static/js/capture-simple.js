/**
 * Face Capture Module (Simplified - No face-api.js)
 * InsightFace handles all face detection/recognition in backend
 * 
 * IMPORTANT: Camera access requires HTTPS or localhost due to browser security
 */

const captureState = {
    mode: 'manual',
    photos: [],
    isCapturing: false,
    stream: null,
    employeeId: null,
    employeeName: '',
    employeeDept: ''
};

const CONFIG = {
    MIN_PHOTOS: 5,
    TARGET_PHOTOS: 10,
    AUTO_CAPTURE_INTERVAL: 500
};

// Security Context Check
function checkSecurityContext() {
    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1' || hostname.endsWith('.local');
    const isHTTPS = window.location.protocol === 'https:';
    const isSecure = window.isSecureContext;
    
    console.log('[Security] Hostname:', hostname);
    console.log('[Security] isLocalhost:', isLocalhost);
    console.log('[Security] isHTTPS:', isHTTPS);
    console.log('[Security] isSecureContext:', isSecure);
    
    if (!isSecure && !isLocalhost) {
        showSecurityWarning();
        return false;
    }
    return true;
}

function showSecurityWarning() {
    const alertContainer = document.getElementById('alertContainer');
    const warningHtml = `
        <div class="alert alert-danger" style="border-left: 4px solid #dc3545;">
            <h5><i class="bi bi-shield-exclamation"></i> Akses Kamera Diblokir</h5>
            <p>Browser memblokir akses kamera karena koneksi tidak aman (HTTP).</p>
            <hr>
            <p class="mb-2"><strong>Solusi:</strong></p>
            <ul class="mb-2">
                <li><strong>Gunakan HTTPS:</strong> Akses via Cloudflare Tunnel atau SSL</li>
                <li><strong>Akses Lokal:</strong> <a href="http://localhost:5001${window.location.pathname}${window.location.search}" class="alert-link">http://localhost:5001${window.location.pathname}</a></li>
            </ul>
            <p class="mb-0 small text-muted">
                <i class="bi bi-info-circle"></i> Jalankan: <code>cloudflared tunnel --url http://localhost:5001</code>
            </p>
        </div>
    `;
    alertContainer.innerHTML = warningHtml;
    
    // Update UI to show camera blocked
    document.getElementById('faceStatusBadge').innerHTML = '<i class="bi bi-shield-x"></i> Kamera Diblokir (HTTP)';
    document.getElementById('faceStatusBadge').className = 'face-status-badge no-face';
    document.getElementById('faceGuide').className = 'face-guide no-face';
}

// UI Helpers
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `${message}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    alertContainer.appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 4000);
}

function updateProgress() {
    const count = captureState.photos.length;
    const percentage = Math.min((count / CONFIG.TARGET_PHOTOS) * 100, 100);
    
    document.getElementById('photoCount').textContent = count;
    document.getElementById('progressBar').style.width = percentage + '%';
    document.getElementById('progressBar').textContent = `${percentage.toFixed(0)}%`;
    
    const statusEl = document.getElementById('progressStatus');
    if (count >= CONFIG.MIN_PHOTOS) {
        statusEl.innerHTML = `✅ Ready! (${count} photos)`;
        statusEl.className = 'text-success';
        document.getElementById('saveBtn').disabled = false;
    } else {
        statusEl.innerHTML = `🔄 ${count}/${CONFIG.MIN_PHOTOS} minimum`;
        statusEl.className = 'text-warning';
        document.getElementById('saveBtn').disabled = true;
    }
    
    document.getElementById('resetBtn').style.display = count > 0 ? 'inline-block' : 'none';
}

function updatePreviewGrid() {
    const grid = document.getElementById('previewGrid');
    if (captureState.photos.length === 0) {
        grid.innerHTML = '<div class="text-center text-muted p-4"><i class="bi bi-image" style="font-size:3rem;"></i><p>No photos yet</p></div>';
        return;
    }
    
    grid.innerHTML = captureState.photos.map((photo, i) => `
        <div class="position-relative" style="aspect-ratio:1;">
            <img src="${photo}" class="w-100 h-100 rounded" style="object-fit:cover;">
            <button class="btn btn-sm btn-danger position-absolute top-0 end-0 m-1" onclick="deletePhoto(${i})">
                <i class="bi bi-x"></i>
            </button>
            <span class="badge bg-dark position-absolute bottom-0 start-0 m-1">${i + 1}</span>
        </div>
    `).join('');
}

// Camera
async function initCamera() {
    // Check security context first
    if (!checkSecurityContext()) {
        console.warn('[Camera] Security context check failed - camera access will be blocked');
        // Don't return here, let the browser show its own error too
    }
    
    // Check if mediaDevices is available
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showAlert('Browser tidak mendukung akses kamera atau koneksi tidak aman (HTTP).', 'danger');
        document.getElementById('faceStatusBadge').innerHTML = '<i class="bi bi-x-circle"></i> Kamera Tidak Tersedia';
        document.getElementById('faceStatusBadge').className = 'face-status-badge error';
        return;
    }
    
    try {
        console.log('[Camera] Requesting camera access...');
        
        captureState.stream = await navigator.mediaDevices.getUserMedia({
            video: { 
                facingMode: 'user', 
                width: { ideal: 640 }, 
                height: { ideal: 480 } 
            }
        });
        
        const video = document.getElementById('trainingWebcam');
        video.srcObject = captureState.stream;
        
        video.onloadedmetadata = () => {
            video.play();
            console.log('[Camera] Video playing:', video.videoWidth, 'x', video.videoHeight);
        };
        
        showAlert('✅ Kamera siap! Ambil foto dari berbagai sudut.', 'success');
        document.getElementById('faceStatusBadge').innerHTML = '<i class="bi bi-check-circle"></i> Kamera Siap';
        document.getElementById('faceStatusBadge').className = 'face-status-badge detected';
        document.getElementById('faceGuide').className = 'face-guide detected';
        
    } catch (error) {
        console.error('[Camera] Error:', error.name, error.message);
        
        let errorMsg = 'Gagal mengakses kamera. ';
        
        switch (error.name) {
            case 'NotAllowedError':
            case 'PermissionDeniedError':
                errorMsg += 'Izin kamera ditolak. Klik ikon kamera di address bar untuk mengizinkan.';
                break;
            case 'NotFoundError':
            case 'DevicesNotFoundError':
                errorMsg += 'Kamera tidak ditemukan.';
                break;
            case 'NotReadableError':
            case 'TrackStartError':
                errorMsg += 'Kamera sedang digunakan aplikasi lain.';
                break;
            case 'OverconstrainedError':
                errorMsg += 'Resolusi kamera tidak didukung.';
                break;
            case 'TypeError':
                errorMsg = 'Akses kamera diblokir karena koneksi tidak aman (HTTP). Gunakan HTTPS atau localhost.';
                break;
            default:
                errorMsg += error.message;
        }
        
        showAlert(errorMsg, 'danger');
        document.getElementById('faceStatusBadge').innerHTML = '<i class="bi bi-x-circle"></i> Kamera Error';
        document.getElementById('faceStatusBadge').className = 'face-status-badge no-face';
    }
}

function stopCamera() {
    if (captureState.stream) {
        captureState.stream.getTracks().forEach(track => track.stop());
    }
}

// Capture
function capturePhoto() {
    const video = document.getElementById('trainingWebcam');
    
    if (!video.srcObject || video.readyState < 2) {
        showAlert('Kamera belum siap. Tunggu sebentar...', 'warning');
        return;
    }
    
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    captureState.photos.push(canvas.toDataURL('image/jpeg', 0.9));
    updatePreviewGrid();
    updateProgress();
    
    // Flash effect
    const flash = document.getElementById('captureFlash');
    flash.classList.add('active');
    setTimeout(() => flash.classList.remove('active'), 200);
}

function deletePhoto(index) {
    captureState.photos.splice(index, 1);
    updatePreviewGrid();
    updateProgress();
}

function resetCapture() {
    if (!confirm('Hapus semua foto?')) return;
    captureState.photos = [];
    updatePreviewGrid();
    updateProgress();
}

// Auto Capture
function startAutoCapture() {
    if (captureState.isCapturing) return;
    
    const video = document.getElementById('trainingWebcam');
    if (!video.srcObject || video.readyState < 2) {
        showAlert('Kamera belum siap.', 'warning');
        return;
    }
    
    captureState.isCapturing = true;
    document.getElementById('startAutoBtn').disabled = true;
    document.getElementById('startAutoBtn').innerHTML = '<i class="bi bi-hourglass-split"></i> Capturing...';
    
    let count = 0;
    const maxPhotos = CONFIG.TARGET_PHOTOS - captureState.photos.length;
    
    const interval = setInterval(() => {
        if (count >= maxPhotos || captureState.photos.length >= CONFIG.TARGET_PHOTOS) {
            stopAutoCapture();
            return;
        }
        capturePhoto();
        count++;
    }, CONFIG.AUTO_CAPTURE_INTERVAL);
    
    captureState.autoCaptureInterval = interval;
    showAlert('🚀 Auto capture dimulai! Putar kepala perlahan...', 'info');
}

function stopAutoCapture() {
    if (captureState.autoCaptureInterval) {
        clearInterval(captureState.autoCaptureInterval);
    }
    captureState.isCapturing = false;
    document.getElementById('startAutoBtn').disabled = false;
    document.getElementById('startAutoBtn').innerHTML = '<i class="bi bi-play-fill"></i> Mulai Auto Capture (10 Foto)';
    showAlert('✅ Auto capture selesai!', 'success');
}

// Save
async function savePhotos() {
    if (captureState.photos.length < CONFIG.MIN_PHOTOS) {
        showAlert(`Minimum ${CONFIG.MIN_PHOTOS} foto diperlukan`, 'warning');
        return;
    }
    
    const saveBtn = document.getElementById('saveBtn');
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Menyimpan...';
    
    try {
        const response = await fetch('/api/save_face_training', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                employee_id: captureState.employeeId,
                employee_name: captureState.employeeName,
                employee_dept: captureState.employeeDept,
                photos: captureState.photos
            })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showAlert('✅ Data wajah berhasil disimpan!', 'success');
            setTimeout(() => window.location.href = '/admin/employees', 2000);
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        showAlert('Gagal menyimpan: ' + error.message, 'danger');
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="bi bi-check2-circle"></i> ✅ Selesai & Simpan (min 5 foto)';
    }
}

// Mode switching function
function switchMode(mode) {
    captureState.mode = mode;
    
    // Update mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(mode + 'ModeBtn').classList.add('active');
    
    // Show/hide controls
    document.getElementById('manualControls').style.display = mode === 'manual' ? 'block' : 'none';
    document.getElementById('autoControls').style.display = mode === 'auto' ? 'block' : 'none';
    document.getElementById('uploadControls').style.display = mode === 'upload' ? 'block' : 'none';
}

// File upload handler
function handleFileUpload(event) {
    const files = Array.from(event.target.files);
    const validFiles = files.filter(file => file.type.startsWith('image/'));
    
    if (validFiles.length === 0) {
        showAlert('Pilih file gambar yang valid', 'warning');
        return;
    }
    
    document.getElementById('selectedFilesCount').textContent = `${validFiles.length} foto dipilih`;
    document.getElementById('uploadPreviewInfo').style.display = 'block';
    
    // Process uploaded files
    validFiles.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
            captureState.photos.push(e.target.result);
            updatePreviewGrid();
            updateProgress();
        };
        reader.readAsDataURL(file);
    });
    
    showAlert(`📁 ${validFiles.length} foto berhasil dimuat`, 'success');
}

// Init
document.addEventListener('DOMContentLoaded', async () => {
    console.log('[Init] Face Capture Module starting...');
    console.log('[Init] Location:', window.location.href);
    console.log('[Init] Protocol:', window.location.protocol);
    console.log('[Init] isSecureContext:', window.isSecureContext);
    
    const params = new URLSearchParams(window.location.search);
    captureState.employeeId = params.get('employee_id');
    captureState.employeeName = params.get('name') || 'Unknown';
    captureState.employeeDept = params.get('dept') || 'Unknown';
    
    document.getElementById('employeeName').textContent = captureState.employeeName;
    document.getElementById('employeeDept').textContent = captureState.employeeDept;
    
    // Event Listeners
    document.getElementById('captureManualBtn').addEventListener('click', capturePhoto);
    document.getElementById('startAutoBtn').addEventListener('click', startAutoCapture);
    document.getElementById('selectPhotosBtn').addEventListener('click', () => {
        document.getElementById('photoUploadInput').click();
    });
    document.getElementById('saveBtn').addEventListener('click', savePhotos);
    document.getElementById('resetBtn').addEventListener('click', resetCapture);
    document.getElementById('backBtn').addEventListener('click', () => {
        window.location.href = '/admin/employees';
    });
    
    // Mode switching
    document.getElementById('manualModeBtn').addEventListener('click', () => switchMode('manual'));
    document.getElementById('autoModeBtn').addEventListener('click', () => switchMode('auto'));
    document.getElementById('uploadModeBtn').addEventListener('click', () => switchMode('upload'));
    
    // File upload handler
    document.getElementById('photoUploadInput').addEventListener('change', handleFileUpload);
    
    await initCamera();
    updateProgress();
});

window.addEventListener('beforeunload', stopCamera);
