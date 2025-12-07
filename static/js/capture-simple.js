/**
 * Face Capture Module (Simplified - No face-api.js)
 * InsightFace handles all face detection/recognition in backend
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
    try {
        captureState.stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user', width: 640, height: 480 }
        });
        
        const video = document.getElementById('videoElement');
        video.srcObject = captureState.stream;
        video.play();
        
        document.getElementById('cameraSection').style.display = 'block';
        showAlert('Camera ready!', 'success');
    } catch (error) {
        showAlert('Camera access denied', 'danger');
    }
}

function stopCamera() {
    if (captureState.stream) {
        captureState.stream.getTracks().forEach(track => track.stop());
    }
}

// Capture
function capturePhoto() {
    const video = document.getElementById('videoElement');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    captureState.photos.push(canvas.toDataURL('image/jpeg', 0.9));
    updatePreviewGrid();
    updateProgress();
    
    // Flash effect
    const flash = document.getElementById('captureFlash');
    flash.style.display = 'block';
    setTimeout(() => flash.style.display = 'none', 200);
}

function deletePhoto(index) {
    captureState.photos.splice(index, 1);
    updatePreviewGrid();
    updateProgress();
}

function resetCapture() {
    if (!confirm('Delete all photos?')) return;
    captureState.photos = [];
    updatePreviewGrid();
    updateProgress();
}

// Auto Capture
function startAutoCapture() {
    if (captureState.isCapturing) return;
    
    captureState.isCapturing = true;
    document.getElementById('captureBtn').disabled = true;
    document.getElementById('autoBtn').disabled = true;
    
    const interval = setInterval(() => {
        if (captureState.photos.length >= CONFIG.TARGET_PHOTOS) {
            stopAutoCapture();
            return;
        }
        capturePhoto();
    }, CONFIG.AUTO_CAPTURE_INTERVAL);
    
    captureState.autoCaptureInterval = interval;
    showAlert('Auto capture started', 'info');
}

function stopAutoCapture() {
    if (captureState.autoCaptureInterval) {
        clearInterval(captureState.autoCaptureInterval);
    }
    captureState.isCapturing = false;
    document.getElementById('captureBtn').disabled = false;
    document.getElementById('autoBtn').disabled = false;
}

// Save
async function savePhotos() {
    if (captureState.photos.length < CONFIG.MIN_PHOTOS) {
        showAlert(`Minimum ${CONFIG.MIN_PHOTOS} photos required`, 'warning');
        return;
    }
    
    const saveBtn = document.getElementById('saveBtn');
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Saving...';
    
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
            showAlert('✅ Saved successfully!', 'success');
            setTimeout(() => window.location.href = '/admin/employees', 2000);
        } else {
            throw new Error(result.message);
        }
    } catch (error) {
        showAlert('Failed: ' + error.message, 'danger');
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="bi bi-save"></i> Save';
    }
}

// Init
document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    captureState.employeeId = params.get('id');
    captureState.employeeName = params.get('name') || 'Unknown';
    captureState.employeeDept = params.get('dept') || 'Unknown';
    
    document.getElementById('employeeNameDisplay').textContent = captureState.employeeName;
    document.getElementById('employeeDeptDisplay').textContent = captureState.employeeDept;
    
    await initCamera();
    updateProgress();
});

window.addEventListener('beforeunload', stopCamera);
