"""
QR Sync Manager - Handles cross-device synchronization for QR code authentication
"""

import threading
import time
import json
import os
from datetime import datetime, timedelta

# File untuk menyimpan device-employee associations (persistent)
DEVICE_DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'device_registry.json')

class DeviceRegistry:
    """
    Menyimpan asosiasi antara device ID dengan employee.
    Data disimpan ke file JSON agar persistent.
    """
    
    def __init__(self):
        self.devices = {}  # {device_id: {employee_id, employee_name, nik, last_seen, ...}}
        self.lock = threading.Lock()
        self._load_from_file()
    
    def _load_from_file(self):
        """Load device data from JSON file"""
        try:
            if os.path.exists(DEVICE_DATA_FILE):
                with open(DEVICE_DATA_FILE, 'r') as f:
                    self.devices = json.load(f)
                print(f"[DeviceRegistry] Loaded {len(self.devices)} registered devices")
        except Exception as e:
            print(f"[DeviceRegistry] Error loading device data: {e}")
            self.devices = {}
    
    def _save_to_file(self):
        """Save device data to JSON file"""
        try:
            os.makedirs(os.path.dirname(DEVICE_DATA_FILE), exist_ok=True)
            with open(DEVICE_DATA_FILE, 'w') as f:
                json.dump(self.devices, f, indent=2, default=str)
        except Exception as e:
            print(f"[DeviceRegistry] Error saving device data: {e}")
    
    def register_device(self, device_id, employee_id, employee_name, nik=None):
        """Register a device with an employee"""
        with self.lock:
            self.devices[device_id] = {
                'employee_id': employee_id,
                'employee_name': employee_name,
                'nik': nik,
                'registered_at': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            }
            self._save_to_file()
            print(f"[DeviceRegistry] Device {device_id[:8]}... registered to {employee_name}")
            return True
    
    def get_employee_by_device(self, device_id):
        """Get employee info by device ID"""
        with self.lock:
            if device_id in self.devices:
                # Update last seen
                self.devices[device_id]['last_seen'] = datetime.now().isoformat()
                self._save_to_file()
                return self.devices[device_id]
            return None
    
    def unregister_device(self, device_id):
        """Remove device registration"""
        with self.lock:
            if device_id in self.devices:
                del self.devices[device_id]
                self._save_to_file()
                return True
            return False
    
    def get_devices_by_employee(self, employee_id):
        """Get all devices registered to an employee"""
        with self.lock:
            return [
                {'device_id': did, **data}
                for did, data in self.devices.items()
                if data.get('employee_id') == employee_id
            ]


# Global device registry instance
device_registry = DeviceRegistry()


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
                    if unit_code and data.get('code') != unit_code.upper():
                        continue
                    verified_at = data.get('verified_at', data.get('timestamp'))
                    if latest_time is None or verified_at > latest_time:
                        latest = data.copy()
                        latest['unit_code'] = data.get('code')  # Add unit_code field for compatibility
                        latest_time = verified_at
            return latest
    
    def verify_qr_auth(self, code, device_info=None, employee_info=None, device_id=None):
        """Verify QR auth by code (called when mobile scans QR)"""
        with self.lock:
            code_upper = code.upper()
            # Find existing session by code
            found = False
            for session_id, data in self.sessions.items():
                if data.get('code') == code_upper:
                    self.sessions[session_id]['verified'] = True
                    self.sessions[session_id]['verified_at'] = datetime.now()
                    self.sessions[session_id]['device_info'] = device_info
                    self.sessions[session_id]['employee_info'] = employee_info
                    self.sessions[session_id]['device_id'] = device_id
                    found = True
                    break
            
            # If no session found, create one
            if not found:
                session_id = f"mobile_{code_upper}_{datetime.now().timestamp()}"
                self.sessions[session_id] = {
                    'verified': True,
                    'timestamp': datetime.now(),
                    'verified_at': datetime.now(),
                    'code': code_upper,
                    'device_info': device_info,
                    'employee_info': employee_info,
                    'device_id': device_id
                }
            return True

    def is_authenticated(self, unit_code):
        """Check if a unit code has been authenticated"""
        with self.lock:
            for session_id, data in self.sessions.items():
                if data.get('code') == unit_code.upper() and data.get('verified', False):
                    return True
        return False


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
