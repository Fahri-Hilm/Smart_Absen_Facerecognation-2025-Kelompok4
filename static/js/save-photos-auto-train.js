/**
 * JavaScript untuk save foto dengan auto-training
 * Digunakan di halaman capture wajah
 */

class PhotoSaveManager {
    constructor() {
        this.photos = [];
        this.employeeId = null;
        this.isProcessing = false;
    }

    // Set employee ID
    setEmployeeId(id) {
        this.employeeId = id;
        console.log('Employee ID set:', id);
    }

    // Add photo to collection
    addPhoto(base64Data) {
        if (this.photos.length >= 50) {
            console.warn('Maximum 50 photos reached');
            return false;
        }
        
        this.photos.push(base64Data);
        console.log(`Photo added. Total: ${this.photos.length}`);
        return true;
    }

    // Clear all photos
    clearPhotos() {
        this.photos = [];
        console.log('Photos cleared');
    }

    // Get photo count
    getPhotoCount() {
        return this.photos.length;
    }

    // Save photos and auto-train
    async savePhotosAndTrain() {
        if (this.isProcessing) {
            console.warn('Already processing...');
            return { success: false, message: 'Sedang memproses...' };
        }

        if (!this.employeeId) {
            return { success: false, message: 'Employee ID tidak ada' };
        }

        if (this.photos.length < 5) {
            return { success: false, message: `Minimal 5 foto diperlukan (saat ini: ${this.photos.length})` };
        }

        this.isProcessing = true;

        try {
            console.log(`Saving ${this.photos.length} photos for employee ${this.employeeId}...`);

            const response = await fetch('/api/save_training_photos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    employee_id: this.employeeId,
                    photos: this.photos
                })
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                console.log('✅ Save and training successful:', result.message);
                this.clearPhotos(); // Clear photos after successful save
                return { success: true, message: result.message };
            } else {
                console.error('❌ Save failed:', result.error || result.message);
                return { success: false, message: result.error || result.message || 'Gagal menyimpan foto' };
            }

        } catch (error) {
            console.error('❌ Network error:', error);
            return { success: false, message: `Error koneksi: ${error.message}` };
        } finally {
            this.isProcessing = false;
        }
    }

    // Alternative simple save method
    async savePhotosSimple() {
        if (!this.employeeId || this.photos.length < 5) {
            return { success: false, message: 'Data tidak lengkap' };
        }

        try {
            const formData = new FormData();
            formData.append('employee_id', this.employeeId);
            formData.append('photos', JSON.stringify(this.photos));

            const response = await fetch('/api/save_photos_simple', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.success) {
                this.clearPhotos();
                return { success: true, message: result.message };
            } else {
                return { success: false, message: result.message };
            }

        } catch (error) {
            return { success: false, message: `Error: ${error.message}` };
        }
    }
}

// Global instance
window.photoSaveManager = new PhotoSaveManager();

// Helper functions for UI
function showSaveStatus(message, isSuccess = true) {
    const statusDiv = document.getElementById('save-status') || createStatusDiv();
    statusDiv.className = `alert ${isSuccess ? 'alert-success' : 'alert-danger'}`;
    statusDiv.textContent = message;
    statusDiv.style.display = 'block';
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 5000);
}

function createStatusDiv() {
    const div = document.createElement('div');
    div.id = 'save-status';
    div.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
    document.body.appendChild(div);
    return div;
}

function updatePhotoCounter() {
    const counter = document.getElementById('photo-counter');
    if (counter) {
        counter.textContent = `${window.photoSaveManager.getPhotoCount()} foto`;
    }
}

// Example usage in capture page:
/*
// Set employee ID when page loads
window.photoSaveManager.setEmployeeId(employeeId);

// Add photo when captured
function onPhotoCaptured(canvas) {
    const base64 = canvas.toDataURL('image/jpeg', 0.8);
    if (window.photoSaveManager.addPhoto(base64)) {
        updatePhotoCounter();
    }
}

// Save all photos and train
async function saveAllPhotos() {
    const result = await window.photoSaveManager.savePhotosAndTrain();
    showSaveStatus(result.message, result.success);
    
    if (result.success) {
        // Redirect to success page or employee list
        setTimeout(() => {
            window.location.href = '/admin/employees';
        }, 2000);
    }
}
*/
