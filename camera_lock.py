"""
Camera Lock Manager - Handles camera access synchronization across devices
Prevents multiple devices from accessing camera simultaneously
"""

import threading
import time
from datetime import datetime, timedelta

class CameraLockManager:
    """
    Manages camera access locks to prevent conflicts when multiple
    devices try to access the camera simultaneously.
    """
    
    def __init__(self, camera_id='default', session_id='default'):
        self.locks = {}  # {camera_id: {locked_by: session_id, locked_at: datetime}}
        self.lock = threading.Lock()
        self.lock_timeout = 60  # Lock expires after 60 seconds
        self._context_camera_id = camera_id
        self._context_session_id = session_id
    
    def __enter__(self):
        """Context manager entry - acquire lock"""
        self.acquire_lock(self._context_camera_id, self._context_session_id)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - release lock"""
        self.release_lock(self._context_camera_id, self._context_session_id)
        return False
        
    def acquire_lock(self, camera_id, session_id):
        """Try to acquire a lock on a camera"""
        with self.lock:
            now = datetime.now()
            
            # Check if camera is already locked
            if camera_id in self.locks:
                lock_info = self.locks[camera_id]
                locked_at = lock_info.get('locked_at', now)
                
                # Check if lock has expired
                if now - locked_at > timedelta(seconds=self.lock_timeout):
                    # Lock expired, remove it
                    del self.locks[camera_id]
                elif lock_info.get('locked_by') != session_id:
                    # Camera is locked by another session
                    return False
            
            # Acquire the lock
            self.locks[camera_id] = {
                'locked_by': session_id,
                'locked_at': now
            }
            return True
    
    def release_lock(self, camera_id, session_id=None):
        """Release a lock on a camera"""
        with self.lock:
            if camera_id in self.locks:
                # If session_id provided, only release if it matches
                if session_id and self.locks[camera_id].get('locked_by') != session_id:
                    return False
                del self.locks[camera_id]
                return True
            return False
    
    def check_lock(self, camera_id):
        """Check if a camera is locked"""
        with self.lock:
            if camera_id in self.locks:
                now = datetime.now()
                lock_info = self.locks[camera_id]
                locked_at = lock_info.get('locked_at', now)
                
                # Check if lock has expired
                if now - locked_at > timedelta(seconds=self.lock_timeout):
                    del self.locks[camera_id]
                    return None
                return lock_info
            return None
    
    def get_lock_info(self, camera_id):
        """Get detailed lock information"""
        return self.check_lock(camera_id)
    
    def refresh_lock(self, camera_id, session_id):
        """Refresh/extend a lock"""
        with self.lock:
            if camera_id in self.locks:
                if self.locks[camera_id].get('locked_by') == session_id:
                    self.locks[camera_id]['locked_at'] = datetime.now()
                    return True
            return False
    
    def cleanup_expired_locks(self):
        """Remove all expired locks"""
        with self.lock:
            now = datetime.now()
            expired = []
            for camera_id, lock_info in self.locks.items():
                locked_at = lock_info.get('locked_at', now)
                if now - locked_at > timedelta(seconds=self.lock_timeout):
                    expired.append(camera_id)
            for camera_id in expired:
                del self.locks[camera_id]
            return len(expired)
    
    def is_camera_available(self, camera_id):
        """Check if camera is available (not locked or lock expired)"""
        return self.check_lock(camera_id) is None


# Alias for backward compatibility
CameraLock = CameraLockManager

# Global instance
camera_lock_manager = CameraLockManager()

# Helper functions for backward compatibility
def is_camera_busy(camera_id='default'):
    """Check if camera is busy/locked"""
    return camera_lock_manager.check_lock(camera_id) is not None

def acquire_camera(camera_id='default', session_id='default'):
    """Acquire camera lock"""
    return camera_lock_manager.acquire_lock(camera_id, session_id)

def release_camera(camera_id='default', session_id=None):
    """Release camera lock"""
    return camera_lock_manager.release_lock(camera_id, session_id)


def start_cleanup_thread():
    """Start background thread to cleanup expired locks"""
    def cleanup_loop():
        while True:
            time.sleep(30)  # Check every 30 seconds
            cleaned = camera_lock_manager.cleanup_expired_locks()
            if cleaned > 0:
                print(f"[Camera Lock] Cleaned up {cleaned} expired locks")
    
    thread = threading.Thread(target=cleanup_loop, daemon=True)
    thread.start()
    return thread
