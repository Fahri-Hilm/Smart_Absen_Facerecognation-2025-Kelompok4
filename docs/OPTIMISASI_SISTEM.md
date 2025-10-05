# ⚡ ABSENN System Optimization Guide

**ABSENN** (Advanced Biometric System for Employee Network Management) - Panduan optimisasi sistem untuk performa maksimal dan scalability enterprise.

## 1. **Database Optimization**

### Current Implementation:
- Optimized queries dengan proper indexing
- Connection pooling dengan PyMySQL
- Efficient face recognition data storage

### Performance Improvements:

#### A. Database Indexing
```sql
-- Optimasi database dengan indexes
ALTER TABLE employees ADD INDEX idx_name (name);
ALTER TABLE employees ADD INDEX idx_bagian (bagian);
ALTER TABLE attendance ADD INDEX idx_employee_date (employee_id, tanggal);
ALTER TABLE attendance ADD INDEX idx_tanggal (tanggal);
ALTER TABLE activity_logs ADD INDEX idx_employee_timestamp (employee_id, timestamp);

-- Composite indexes untuk queries yang sering digunakan
ALTER TABLE attendance ADD INDEX idx_employee_date_composite (employee_id, tanggal, jam_masuk, jam_pulang);
```

#### B. Connection Pooling Implementation
```python
# database.py - Improved connection management
import pymysql.cursors
from pymysql.pool import Pool
from contextlib import contextmanager
import threading

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.lock = threading.Lock()
        
    def initialize_connection_pool(self, config):
        """Initialize connection pool for better performance"""
        self.pool = Pool(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            autocommit=True,
            max_connections=20,  # Max connections in pool
            blocking=True,       # Block when pool is full
            cursorclass=pymysql.cursors.DictCursor
        )
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = self.pool.get_connection()
            yield connection
        finally:
            if connection:
                connection.close()  # Return to pool
```

#### C. Query Optimization
```python
# models.py - Optimized queries
class Attendance:
    @staticmethod
    def get_daily_attendance_optimized(date):
        """Optimized query with proper indexing"""
        query = """
        SELECT 
            e.name, e.bagian, 
            a.jam_masuk, a.jam_pulang,
            CASE 
                WHEN a.jam_masuk IS NOT NULL AND a.jam_pulang IS NOT NULL 
                THEN 'Lengkap'
                WHEN a.jam_masuk IS NOT NULL 
                THEN 'Masuk'
                ELSE 'Belum Absen'
            END as status
        FROM employees e
        LEFT JOIN attendance a ON e.id = a.employee_id AND a.tanggal = %s
        ORDER BY e.bagian, e.name
        """
        # Use prepared statements for better performance
        return db_manager.execute_query(query, (date,))
        
    @staticmethod
    def get_attendance_summary_cached(employee_id, month, year):
        """Cached attendance summary"""
        cache_key = f"attendance_{employee_id}_{month}_{year}"
        
        # Check cache first
        if cache_key in attendance_cache:
            return attendance_cache[cache_key]
            
        query = """
        SELECT 
            COUNT(*) as total_days,
            COUNT(CASE WHEN jam_masuk IS NOT NULL THEN 1 END) as present_days,
            AVG(CASE WHEN jam_masuk <= '08:00:00' THEN 1 ELSE 0 END) * 100 as punctuality
        FROM attendance 
        WHERE employee_id = %s 
        AND MONTH(tanggal) = %s 
        AND YEAR(tanggal) = %s
        """
        
        result = db_manager.execute_query(query, (employee_id, month, year))
        attendance_cache[cache_key] = result
        return result
```

## 2. **CACHING STRATEGY**

### Implementation:
```python
# cache.py - Redis-like caching system
import time
from typing import Any, Optional

class SimpleCache:
    def __init__(self, default_ttl=300):  # 5 minutes default
        self.cache = {}
        self.timestamps = {}
        self.default_ttl = default_ttl
        
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            if time.time() - self.timestamps[key] < self.default_ttl:
                return self.cache[key]
            else:
                # Expired, remove from cache
                del self.cache[key]
                del self.timestamps[key]
        return None
        
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        self.cache[key] = value
        self.timestamps[key] = time.time()
        
    def invalidate(self, pattern: str = None):
        """Invalidate cache entries"""
        if pattern:
            keys_to_remove = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self.cache[key]
                del self.timestamps[key]

# Usage in routes
@app.route('/get_attendance_data')
@qr_verification_required
def get_attendance_data():
    cache_key = f"attendance_data_{date.today()}"
    
    # Try cache first
    cached_data = simple_cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data)
    
    # If not cached, compute and cache
    names, bagian, tanggal, times, l = extract_attendance()
    data = {
        'names': names,
        'bagian': bagian, 
        'tanggal': tanggal,
        'times': times,
        'count': l
    }
    
    simple_cache.set(cache_key, data, ttl=60)  # Cache for 1 minute
    return jsonify(data)
```

## 3. **CAMERA RESOURCE OPTIMIZATION**

### Current Issues:
- Camera resource leaks
- Blocking camera operations
- No camera availability check

### Improvements:
```python
# camera_manager.py - Dedicated camera management
import cv2
import threading
import time
from queue import Queue, Empty

class CameraManager:
    def __init__(self):
        self.camera_lock = threading.Lock()
        self.active_cameras = {}
        self.camera_queue = Queue()
        
    def get_available_cameras(self):
        """Check available cameras efficiently"""
        available = []
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    available.append(i)
            cap.release()
        return available
        
    def acquire_camera(self, camera_id: int, timeout: int = 5):
        """Acquire camera with timeout"""
        with self.camera_lock:
            if camera_id in self.active_cameras:
                return None  # Camera busy
                
            cap = cv2.VideoCapture(camera_id)
            if cap.isOpened():
                self.active_cameras[camera_id] = cap
                return cap
            return None
            
    def release_camera(self, camera_id: int):
        """Safely release camera"""
        with self.camera_lock:
            if camera_id in self.active_cameras:
                cap = self.active_cameras[camera_id]
                cap.release()
                del self.active_cameras[camera_id]
                cv2.destroyAllWindows()
                time.sleep(0.5)  # Allow system cleanup

# Global camera manager instance
camera_manager = CameraManager()

# Updated attendance function
def run_attendance_with_camera_optimized(mode, camera_id):
    """Optimized camera function with proper resource management"""
    cap = camera_manager.acquire_camera(camera_id)
    if not cap:
        return {
            'status': 'error',
            'message': 'Kamera sedang digunakan atau tidak tersedia'
        }
    
    try:
        # Camera operations here
        # ... existing code ...
        
    finally:
        camera_manager.release_camera(camera_id)
```

## 4. **ASYNC OPERATIONS**

### Implementation:
```python
# async_utils.py - Background tasks
import threading
from concurrent.futures import ThreadPoolExecutor
import time

class BackgroundTasks:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def cleanup_expired_sessions(self):
        """Clean expired QR sessions in background"""
        def cleanup():
            current_time = time.time()
            expired_sessions = []
            
            for session_id, session_data in app.permanent_session_lifetime.items():
                if current_time - session_data['created'] > 600:  # 10 minutes
                    expired_sessions.append(session_id)
                    
            for session_id in expired_sessions:
                # Clean up expired sessions
                pass
                
        self.executor.submit(cleanup)
        
    def log_attendance_async(self, employee_id, mode, timestamp):
        """Log attendance in background"""
        def log_task():
            try:
                ActivityLog.add_log(employee_id, f"attendance_{mode}", 
                                  f"Absensi {mode} berhasil pada {timestamp}")
            except Exception as e:
                logger.error(f"Failed to log attendance: {e}")
                
        self.executor.submit(log_task)

# Usage in routes
background_tasks = BackgroundTasks()

@app.route('/mark_attendance', methods=['POST'])
@qr_verification_required 
def mark_attendance():
    # ... existing code ...
    
    # Log attendance asynchronously
    background_tasks.log_attendance_async(employee_id, mode, datetime.now())
    
    return jsonify(result)
```

## 5. **FRONTEND OPTIMIZATION**

### A. Asset Optimization:
```html
<!-- Optimized CSS/JS loading -->
<head>
    <!-- Preload critical resources -->
    <link rel="preload" href="/static/css/main.css" as="style">
    <link rel="preload" href="/static/js/attendance.js" as="script">
    
    <!-- Critical CSS inline -->
    <style>
        /* Critical above-the-fold CSS here */
        body { margin: 0; font-family: 'Poppins', sans-serif; }
        .loading-spinner { /* spinner styles */ }
    </style>
    
    <!-- Non-critical CSS deferred -->
    <link rel="stylesheet" href="/static/css/non-critical.css" media="print" onload="this.media='all'">
</head>
```

### B. JavaScript Optimization:
```javascript
// attendance.js - Optimized JavaScript
class AttendanceManager {
    constructor() {
        this.cache = new Map();
        this.requestQueue = [];
        this.isProcessing = false;
    }
    
    async markAttendance(mode) {
        if (this.isProcessing) {
            this.showMessage('Mohon tunggu, sedang memproses...', 'warning');
            return;
        }
        
        this.isProcessing = true;
        this.showLoadingState(mode);
        
        try {
            const formData = new FormData();
            formData.append('mode', mode);
            formData.append('camera_id', this.getSelectedCamera());
            
            const response = await fetch('/mark_attendance', {
                method: 'POST',
                body: formData,
                signal: AbortSignal.timeout(30000) // 30 second timeout
            });
            
            const result = await response.json();
            this.handleAttendanceResult(mode, result);
            
        } catch (error) {
            this.handleError(mode, error);
        } finally {
            this.isProcessing = false;
            this.hideLoadingState(mode);
        }
    }
    
    // Debounced attendance data refresh
    refreshAttendanceData = this.debounce(() => {
        fetch('/get_attendance_data')
            .then(response => response.json())
            .then(data => this.updateAttendanceDisplay(data))
            .catch(error => console.error('Failed to refresh data:', error));
    }, 1000);
    
    debounce(func, wait) {
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
}

// Initialize with service worker for offline capability
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js')
        .then(registration => console.log('SW registered'))
        .catch(error => console.log('SW registration failed'));
}
```

## 6. **MONITORING & ANALYTICS**

### Implementation:
```python
# monitoring.py - System monitoring
import psutil
import time
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.metrics = {
            'requests_count': 0,
            'camera_operations': 0,
            'failed_operations': 0,
            'response_times': []
        }
        
    def log_request(self, endpoint, response_time):
        """Log request metrics"""
        self.metrics['requests_count'] += 1
        self.metrics['response_times'].append(response_time)
        
        # Keep only last 100 response times
        if len(self.metrics['response_times']) > 100:
            self.metrics['response_times'] = self.metrics['response_times'][-100:]
            
    def get_system_stats(self):
        """Get current system performance"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'avg_response_time': sum(self.metrics['response_times']) / len(self.metrics['response_times']) if self.metrics['response_times'] else 0,
            'total_requests': self.metrics['requests_count']
        }

# Usage in Flask app
monitor = SystemMonitor()

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request  
def after_request(response):
    if hasattr(g, 'start_time'):
        response_time = time.time() - g.start_time
        monitor.log_request(request.endpoint, response_time)
    return response
```

## 7. **SECURITY ENHANCEMENTS**

```python
# security.py - Enhanced security measures
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.failed_attempts = {}
        
    def rate_limit_check(self, ip_address, max_attempts=5, window_minutes=15):
        """Rate limiting for attendance attempts"""
        now = datetime.now()
        if ip_address in self.failed_attempts:
            attempts = self.failed_attempts[ip_address]
            # Clean old attempts
            attempts = [attempt for attempt in attempts 
                       if now - attempt < timedelta(minutes=window_minutes)]
            
            if len(attempts) >= max_attempts:
                return False
                
        return True
        
    def log_failed_attempt(self, ip_address):
        """Log failed attendance attempt"""
        if ip_address not in self.failed_attempts:
            self.failed_attempts[ip_address] = []
        self.failed_attempts[ip_address].append(datetime.now())
        
    def generate_secure_qr_token(self, unit_code):
        """Generate JWT token for QR codes"""
        payload = {
            'unit_code': unit_code,
            'exp': datetime.utcnow() + timedelta(minutes=10),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
```

Apakah Anda ingin saya implementasikan salah satu optimisasi ini untuk meningkatkan performa sistem?