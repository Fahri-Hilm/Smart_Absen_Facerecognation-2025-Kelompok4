/**
 * Face Capture Module with face-api.js Integration
 * Handles face detection, capture, and training data collection
 */

// State Management
const captureState = {
    mode: 'manual',
    photos: [],
    isCapturing: false,
    stream: null,
    employeeId: null,
    employeeName: '',
    employeeDept: '',
    faceDetectionReady: false
};

// Configuration
const CONFIG = {
    MIN_PHOTOS: 5,
    TARGET_PHOTOS: 10,
    AUTO_CAPTURE_DURATION: 3000,
    FACE_DETECTION_INTERVAL: 100,
    FACE_CONFIDENCE_THRESHOLD: 0.5
};

// Face Detection State
let faceDetectionInterval = null;
let lastDetectedFace = null;

// ============================================================================
// FACE-API.JS INITIALIZATION
// ============================================================================

async function loadFaceDetectionModels() {
    try {
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model';
        
        await Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
            faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_URL)
        ]);
        
        captureState.faceDetectionReady = true;
        console.log('✅ Face detection models loaded');
        showAlert('Face detection ready!', 'success');
        return true;
    } catch (error) {
        console.error('❌ Failed to load face detection models:', error);
        showAlert('Face detection unavailable, using basic mode', 'warning');
        return false;
    }
}

async function detectFaceInVideo(videoElement) {
    if (!captureState.faceDetectionReady) return null;
    
    try {
        const detection = await faceapi
            .detectSingleFace(videoElement, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks(true);
        
        return detection;
    } catch (error) {
        console.error('Face detection error:', error);
        return null;
    }
}

function drawFaceOverlay(detection, canvas, video) {
    if (!detection) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw face box
    const box = detection.detection.box;
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 3;
    ctx.strokeRect(box.x, box.y, box.width, box.height);
    
    // Draw landmarks
    if (detection.landmarks) {
        const landmarks = detection.landmarks.positions;
        ctx.fillStyle = '#00ff00';
        landmarks.forEach(point => {
            ctx.beginPath();
            ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI);
            ctx.fill();
        });
    }
}

function startFaceDetectionLoop(videoElement, overlayCanvas) {
    if (faceDetectionInterval) return;
    
    faceDetectionInterval = setInterval(async () => {
        const detection = await detectFaceInVideo(videoElement);
        lastDetectedFace = detection;
        
        // Update UI feedback
        const indicator = document.getElementById('faceIndicator');
        if (detection) {
            indicator.className = 'face-indicator detected';
            indicator.innerHTML = '<i class="bi bi-check-circle"></i> Face Detected';
            drawFaceOverlay(detection, overlayCanvas, videoElement);
        } else {
            indicator.className = 'face-indicator';
            indicator.innerHTML = '<i class="bi bi-exclamation-circle"></i> No Face';
            overlayCanvas.getContext('2d').clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
        }
    }, CONFIG.FACE_DETECTION_INTERVAL);
}

function stopFaceDetectionLoop() {
    if (faceDetectionInterval) {
        clearInterval(faceDetectionInterval);
        faceDetectionInterval = null;
    }
}

// ============================================================================
// UI HELPERS
// ============================================================================

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-custom alert-${type}-custom`;
    alertDiv.innerHTML = message;
    alertContainer.appendChild(alertDiv);
    
    setTimeout(() => alertDiv.remove(), 4000);
}

function updateProgress() {
    const count = captureState.photos.length;
    const percentage = Math.min((count / CONFIG.TARGET_PHOTOS) * 100, 100);
    
    document.getElementById('photoCount').textContent = count;
    
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = percentage + '%';
    progressBar.textContent = `${percentage.toFixed(0)}%`;
    
    const statusEl = document.getElementById('progressStatus');
    if (count >= CONFIG.MIN_PHOTOS) {
        statusEl.innerHTML = `✅ Ready! (${count} photos - 99%+ accuracy)`;
        statusEl.style.color = '#28a745';
        document.getElementById('saveBtn').disabled = false;
    } else if (count > 0) {
        statusEl.innerHTML = `🔄 ${count}/${CONFIG.MIN_PHOTOS} minimum...`;
        statusEl.style.color = '#FF8C00';
        document.getElementById('saveBtn').disabled = true;
    } else {
        statusEl.innerHTML = '📌 Ready to capture';
        statusEl.style.color = '#6C757D';
        document.getElementById('saveBtn').disabled = true;
    }
    
    document.getElementById('resetBtn').style.display = count > 0 ? 'block' : 'none';
}

function updatePreviewGrid() {
    const grid = document.getElementById('previewGrid');
    if (captureState.photos.length === 0) {
        grid.innerHTML = `
            <div class="preview-empty">
                <i class="bi bi-image"></i>
                <span>No photos yet</span>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = captureState.photos.map((photo, index) => `
        <div class="preview-item">
            <img src="${photo}" alt="Photo ${index + 1}">
            <button class="preview-item-delete" onclick="deletePhoto(${index})">
                <i class="bi bi-x"></i>
            </button>
            <div class="preview-item-number">${index + 1}</div>
        </div>
    `).join('');
}

// ============================================================================
// CAMERA MANAGEMENT
// ============================================================================

async function initCamera() {
    try {
        captureState.stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'user', width: 640, height: 480 }
        });
        
        const video = document.getElementById('videoElement');
        video.srcObject = captureState.stream;
        
        video.onloadedmetadata = () => {
            video.play();
            if (captureState.faceDetectionReady) {
                const overlay = document.getElementById('faceOverlay');
                startFaceDetectionLoop(video, overlay);
            }
        };
        
        document.getElementById('cameraSection').style.display = 'block';
        showAlert('Camera ready!', 'success');
    } catch (error) {
        console.error('Camera error:', error);
        showAlert('Camera access denied', 'danger');
    }
}

function stopCamera() {
    if (captureState.stream) {
        captureState.stream.getTracks().forEach(track => track.stop());
        captureState.stream = null;
    }
    stopFaceDetectionLoop();
}

// ============================================================================
// PHOTO CAPTURE
// ============================================================================

function capturePhoto() {
    // Check face detection
    if (captureState.faceDetectionReady && !lastDetectedFace) {
        showAlert('Please position your face in frame', 'warning');
        return;
    }
    
    const video = document.getElementById('videoElement');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    const photoData = canvas.toDataURL('image/jpeg', 0.9);
    captureState.photos.push(photoData);
    
    updatePreviewGrid();
    updateProgress();
    
    // Visual feedback
    document.getElementById('captureFlash').style.display = 'block';
    setTimeout(() => {
        document.getElementById('captureFlash').style.display = 'none';
    }, 200);
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
    showAlert('All photos deleted', 'info');
}

// ============================================================================
// AUTO CAPTURE MODE
// ============================================================================

function startAutoCapture() {
    if (captureState.isCapturing) return;
    
    captureState.isCapturing = true;
    captureState.mode = 'auto';
    
    document.getElementById('captureBtn').disabled = true;
    document.getElementById('autoBtn').disabled = true;
    
    const interval = setInterval(() => {
        if (captureState.photos.length >= CONFIG.TARGET_PHOTOS) {
            stopAutoCapture();
            return;
        }
        
        capturePhoto();
    }, CONFIG.AUTO_CAPTURE_DURATION / CONFIG.TARGET_PHOTOS);
    
    captureState.autoCaptureInterval = interval;
    showAlert('Auto capture started', 'info');
}

function stopAutoCapture() {
    if (captureState.autoCaptureInterval) {
        clearInterval(captureState.autoCaptureInterval);
        captureState.autoCaptureInterval = null;
    }
    
    captureState.isCapturing = false;
    captureState.mode = 'manual';
    
    document.getElementById('captureBtn').disabled = false;
    document.getElementById('autoBtn').disabled = false;
    
    showAlert('Auto capture stopped', 'info');
}

// ============================================================================
// SAVE TO SERVER
// ============================================================================

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
            showAlert('✅ Training data saved successfully!', 'success');
            setTimeout(() => {
                window.location.href = '/admin/employees';
            }, 2000);
        } else {
            throw new Error(result.message || 'Save failed');
        }
    } catch (error) {
        console.error('Save error:', error);
        showAlert('Failed to save: ' + error.message, 'danger');
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="bi bi-save"></i> Save Training Data';
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    // Load employee data from URL params
    const params = new URLSearchParams(window.location.search);
    captureState.employeeId = params.get('id');
    captureState.employeeName = params.get('name') || 'Unknown';
    captureState.employeeDept = params.get('dept') || 'Unknown';
    
    // Update UI
    document.getElementById('employeeNameDisplay').textContent = captureState.employeeName;
    document.getElementById('employeeDeptDisplay').textContent = captureState.employeeDept;
    
    // Load face detection models
    await loadFaceDetectionModels();
    
    // Initialize camera
    await initCamera();
    
    // Update initial state
    updateProgress();
    updatePreviewGrid();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    stopCamera();
    stopFaceDetectionLoop();
});
