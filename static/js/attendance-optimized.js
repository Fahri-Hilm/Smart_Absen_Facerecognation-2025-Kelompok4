/**
 * KAFEBASABASI - Optimized Attendance System
 * Enhanced JavaScript Framework v2.0
 */

class AttendanceSystem {
    constructor() {
        this.cache = new Map();
        this.requestQueue = [];
        this.isProcessing = false;
        this.retryAttempts = 3;
        this.requestTimeout = 30000; // 30 seconds
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.startLiveClock();
        this.setupAutoRefresh();
        this.loadAttendanceStatus();
        this.setupServiceWorker();
    }
    
    // ===========================
    // CORE ATTENDANCE FUNCTIONS
    // ===========================
    
    async markAttendance(mode) {
        if (this.isProcessing) {
            this.showNotification('Mohon tunggu, sedang memproses...', 'warning');
            return;
        }
        
        // Rate limiting check
        if (!this.checkRateLimit(mode)) {
            this.showNotification('Terlalu banyak percobaan. Tunggu sebentar.', 'error');
            return;
        }
        
        this.isProcessing = true;
        this.setLoadingState(mode, true);
        
        try {
            const formData = new FormData();
            formData.append('mode', mode);
            formData.append('camera_id', this.getSelectedCamera());
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.requestTimeout);
            
            const response = await fetch('/mark_attendance', {
                method: 'POST',
                body: formData,
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            this.handleAttendanceResult(mode, result);
            
        } catch (error) {
            this.handleAttendanceError(mode, error);
        } finally {
            this.isProcessing = false;
            this.setLoadingState(mode, false);
        }
    }
    
    handleAttendanceResult(mode, result) {
        if (result.status === 'success') {
            this.markAttendanceComplete(mode);
            this.showNotification(result.message, 'success');
            this.refreshAttendanceData();
            this.updateAttendanceStatus(mode, 'completed');
            
            // Hapus dari localStorage rate limit
            this.resetRateLimit(mode);
            
        } else if (result.status === 'warning') {
            this.showNotification(result.message, 'warning');
        } else {
            this.showNotification(result.message || 'Terjadi kesalahan', 'error');
        }
    }
    
    handleAttendanceError(mode, error) {
        console.error('Attendance error:', error);
        
        let message = 'Terjadi kesalahan sistem';
        if (error.name === 'AbortError') {
            message = 'Koneksi timeout. Silakan coba lagi.';
        } else if (error.message.includes('Failed to fetch')) {
            message = 'Tidak dapat terhubung ke server';
        }
        
        this.showNotification(message, 'error');
        this.incrementRateLimit(mode);
    }
    
    // ===========================
    // UI STATE MANAGEMENT
    // ===========================
    
    setLoadingState(mode, isLoading) {
        const button = document.querySelector(`.btn-${mode}`);
        if (!button) return;
        
        if (isLoading) {
            button.classList.add('loading');
            button.disabled = true;
            
            const content = button.querySelector('.btn-content h4');
            if (content) {
                content.textContent = 'Memproses...';
            }
        } else {
            button.classList.remove('loading');
            button.disabled = false;
            
            const content = button.querySelector('.btn-content h4');
            if (content) {
                content.textContent = mode === 'masuk' ? 'Absen Masuk' : 'Absen Pulang';
            }
        }
    }
    
    markAttendanceComplete(mode) {
        const button = document.querySelector(`.btn-${mode}`);
        const statusElement = document.querySelector(`#status${mode.charAt(0).toUpperCase() + mode.slice(1)}`);
        const timeElement = document.querySelector(`#jam${mode.charAt(0).toUpperCase() + mode.slice(1)}`);
        
        if (button) {
            button.classList.add('completed');
            button.disabled = true;
        }
        
        if (statusElement) {
            statusElement.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
        }
        
        if (timeElement) {
            timeElement.textContent = new Date().toLocaleTimeString('id-ID', {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        // Animate success
        this.animateSuccess(button);
    }
    
    animateSuccess(element) {
        if (!element) return;
        
        element.style.transform = 'scale(1.1)';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 200);
    }
    
    // ===========================
    // LIVE CLOCK SYSTEM
    // ===========================
    
    startLiveClock() {
        this.updateClock();
        setInterval(() => this.updateClock(), 1000);
    }
    
    updateClock() {
        const now = new Date();
        const timeElement = document.getElementById('liveTime');
        const dateElement = document.getElementById('liveDate');
        
        if (timeElement) {
            timeElement.textContent = now.toLocaleTimeString('id-ID', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        }
        
        if (dateElement) {
            dateElement.textContent = now.toLocaleDateString('id-ID', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
    }
    
    // ===========================
    // DATA MANAGEMENT
    // ===========================
    
    async refreshAttendanceData() {
        try {
            const cacheKey = 'attendance_data';
            const cached = this.cache.get(cacheKey);
            
            // Use cache if less than 30 seconds old
            if (cached && Date.now() - cached.timestamp < 30000) {
                this.updateAttendanceDisplay(cached.data);
                return;
            }
            
            const response = await fetch('/api/attendance_data');
            if (!response.ok) throw new Error('Failed to fetch data');
            
            const data = await response.json();
            
            // Cache the data
            this.cache.set(cacheKey, {
                data: data,
                timestamp: Date.now()
            });
            
            this.updateAttendanceDisplay(data);
            
        } catch (error) {
            console.error('Failed to refresh attendance data:', error);
        }
    }
    
    updateAttendanceDisplay(data) {
        const tableBody = document.querySelector('#attendanceTable tbody');
        if (!tableBody || !data.names) return;
        
        tableBody.innerHTML = '';
        
        for (let i = 0; i < data.names.length; i++) {
            const row = document.createElement('tr');
            row.className = 'fade-in';
            row.style.animationDelay = `${i * 0.1}s`;
            
            const status = this.getAttendanceStatus(data.times[i]);
            const statusClass = this.getStatusClass(status);
            
            row.innerHTML = `
                <td><strong>${data.names[i]}</strong></td>
                <td><span class="badge bg-secondary">${data.bagian[i]}</span></td>
                <td>${data.tanggal[i] || '-'}</td>
                <td>${data.times[i] || '-'}</td>
                <td><span class="badge ${statusClass}">${status}</span></td>
            `;
            
            tableBody.appendChild(row);
        }
    }
    
    getAttendanceStatus(timeStr) {
        if (!timeStr || timeStr === '-') return 'Belum Absen';
        if (timeStr.includes(' - ')) return 'Lengkap';
        return 'Masuk';
    }
    
    getStatusClass(status) {
        switch (status) {
            case 'Lengkap': return 'bg-success';
            case 'Masuk': return 'bg-warning';
            default: return 'bg-secondary';
        }
    }
    
    // ===========================
    // CAMERA MANAGEMENT
    // ===========================
    
    getSelectedCamera() {
        const select = document.getElementById('cameraSelect');
        return select ? select.value : '0';
    }
    
    async loadAvailableCameras() {
        try {
            const response = await fetch('/api/cameras');
            const cameras = await response.json();
            
            const select = document.getElementById('cameraSelect');
            if (select && cameras.length > 0) {
                select.innerHTML = cameras.map(camera => 
                    `<option value="${camera.id}">Kamera ${camera.id} (${camera.name})</option>`
                ).join('');
            }
        } catch (error) {
            console.error('Failed to load cameras:', error);
        }
    }
    
    // ===========================
    // RATE LIMITING
    // ===========================
    
    checkRateLimit(mode) {
        const key = `rate_limit_${mode}`;
        const attempts = JSON.parse(localStorage.getItem(key) || '[]');
        const now = Date.now();
        const fiveMinutesAgo = now - (5 * 60 * 1000);
        
        // Filter attempts from last 5 minutes
        const recentAttempts = attempts.filter(time => time > fiveMinutesAgo);
        
        // Allow max 3 attempts per 5 minutes
        return recentAttempts.length < 3;
    }
    
    incrementRateLimit(mode) {
        const key = `rate_limit_${mode}`;
        const attempts = JSON.parse(localStorage.getItem(key) || '[]');
        attempts.push(Date.now());
        localStorage.setItem(key, JSON.stringify(attempts));
    }
    
    resetRateLimit(mode) {
        const key = `rate_limit_${mode}`;
        localStorage.removeItem(key);
    }
    
    // ===========================
    // NOTIFICATIONS
    // ===========================
    
    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existing = document.querySelectorAll('.notification');
        existing.forEach(el => el.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'info'} alert-dismissible fade show`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            animation: slideInRight 0.3s ease-out;
        `;
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    // ===========================
    // AUTO REFRESH & MONITORING
    // ===========================
    
    setupAutoRefresh() {
        // Refresh data every 30 seconds
        setInterval(() => {
            if (!this.isProcessing) {
                this.refreshAttendanceData();
            }
        }, 30000);
        
        // Refresh on page visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && !this.isProcessing) {
                this.refreshAttendanceData();
            }
        });
    }
    
    // ===========================
    // EVENT LISTENERS
    // ===========================
    
    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'm') {
                e.preventDefault();
                this.markAttendance('masuk');
            } else if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                this.markAttendance('pulang');
            }
        });
        
        // Page load events
        window.addEventListener('load', () => {
            this.loadAvailableCameras();
            this.refreshAttendanceData();
        });
        
        // Connection status monitoring
        window.addEventListener('online', () => {
            this.showNotification('Koneksi internet tersambung kembali', 'success');
            this.refreshAttendanceData();
        });
        
        window.addEventListener('offline', () => {
            this.showNotification('Koneksi internet terputus', 'warning');
        });
    }
    
    // ===========================
    // SERVICE WORKER
    // ===========================
    
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/sw.js')
                .then(registration => {
                    console.log('Service Worker registered successfully');
                })
                .catch(error => {
                    console.log('Service Worker registration failed');
                });
        }
    }
    
    // ===========================
    // ATTENDANCE STATUS TRACKING
    // ===========================
    
    async loadAttendanceStatus() {
        try {
            const today = new Date().toISOString().split('T')[0];
            const cacheKey = `status_${today}`;
            
            let status = this.cache.get(cacheKey);
            if (!status) {
                // Load from server or localStorage
                status = JSON.parse(localStorage.getItem(cacheKey) || '{}');
            }
            
            if (status.masuk) {
                this.updateAttendanceStatus('masuk', 'completed');
            }
            if (status.pulang) {
                this.updateAttendanceStatus('pulang', 'completed');
            }
            
        } catch (error) {
            console.error('Failed to load attendance status:', error);
        }
    }
    
    updateAttendanceStatus(mode, status) {
        const today = new Date().toISOString().split('T')[0];
        const cacheKey = `status_${today}`;
        
        let currentStatus = JSON.parse(localStorage.getItem(cacheKey) || '{}');
        currentStatus[mode] = status === 'completed';
        
        localStorage.setItem(cacheKey, JSON.stringify(currentStatus));
        this.cache.set(cacheKey, currentStatus);
        
        if (status === 'completed') {
            this.markAttendanceComplete(mode);
        }
    }
}

// ===========================
// UTILITY FUNCTIONS
// ===========================

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format time helper
function formatTime(date) {
    return date.toLocaleTimeString('id-ID', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Initialize system when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.attendanceSystem = new AttendanceSystem();
});

// Global function for button clicks (backward compatibility)
function markAttendance(mode) {
    if (window.attendanceSystem) {
        window.attendanceSystem.markAttendance(mode);
    }
}