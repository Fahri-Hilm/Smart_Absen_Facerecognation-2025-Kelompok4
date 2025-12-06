"""
QR Sync Manager - Handles cross-device synchronization for QR code authentication
"""

import threading
import time
from datetime import datetime, timedelta

class QRSyncManager:
    """
    Manages QR code sessions and cross-device synchronization.
    When a mobile device scans a QR code, the laptop browser should
    automatically detect the verification and redirect.
    """
    
    def __init__(self):
        self.sessions = {}  # {session_id: {verified: bool, timestamp: datetime, ...}}
        self.lock = threading.Lock()
        self.cleanup_interval = 300  # 5 minutes
        
    def create_session(self, session_id, code=None):
        """Create a new QR session"""
        with self.lock:
            self.sessions[session_id] = {
                'verified': False,
                'timestamp': datetime.now(),
                'code': code or session_id[:6].upper(),
                'device_info': None
            }
        return self.sessions[session_id]['code']
    
    def verify_session(self, session_id=None, code=None):
        """Mark a session as verified (called when mobile scans QR)"""
        with self.lock:
            # Find session by code if session_id not provided
            if code and not session_id:
                for sid, data in self.sessions.items():
                    if data.get('code') == code.upper():
                        session_id = sid
                        break
            
            if session_id and session_id in self.sessions:
                self.sessions[session_id]['verified'] = True
                self.sessions[session_id]['verified_at'] = datetime.now()
                return True
        return False
    
    def check_session(self, session_id):
        """Check if a session has been verified"""
        with self.lock:
            if session_id in self.sessions:
                return self.sessions[session_id].get('verified', False)
        return False
    
    def get_session(self, session_id):
        """Get session data"""
        with self.lock:
            return self.sessions.get(session_id, None)
    
    def get_session_by_code(self, code):
        """Find session by verification code"""
        with self.lock:
            for session_id, data in self.sessions.items():
                if data.get('code') == code.upper():
                    return session_id, data
        return None, None
    
    def remove_session(self, session_id):
        """Remove a session"""
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
    
    def cleanup_old_sessions(self):
        """Remove sessions older than cleanup_interval"""
        with self.lock:
            now = datetime.now()
            expired = []
            for session_id, data in self.sessions.items():
                if now - data['timestamp'] > timedelta(seconds=self.cleanup_interval):
                    expired.append(session_id)
            for session_id in expired:
                del self.sessions[session_id]
        return len(expired)
    
    def get_latest_auth(self, unit_code=None):
        """Get the latest authenticated session for a unit code"""
        with self.lock:
            latest = None
            latest_time = None
            for session_id, data in self.sessions.items():
                if data.get('verified', False):
                    # If unit_code specified, filter by it
                    if unit_code and data.get('code') != unit_code:
                        continue
                    verified_at = data.get('verified_at', data.get('timestamp'))
                    if latest_time is None or verified_at > latest_time:
                        latest = data
                        latest_time = verified_at
            return latest


# Global instance
qr_sync_manager = QRSyncManager()


def start_cleanup_thread():
    """Start background thread to cleanup old sessions"""
    def cleanup_loop():
        while True:
            time.sleep(60)  # Check every minute
            cleaned = qr_sync_manager.cleanup_old_sessions()
            if cleaned > 0:
                print(f"[QR Sync] Cleaned up {cleaned} expired sessions")
    
    thread = threading.Thread(target=cleanup_loop, daemon=True)
    thread.start()
    return thread
