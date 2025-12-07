# 📚 API Documentation - ABSENN

## 🌐 **Base URLs**

### Local Access
```
http://localhost:5001
```

### Internet Access (Ngrok)
```
https://[random-string].ngrok-free.dev
```

---

## 🔐 **Authentication**

### Headers Required
```http
Content-Type: application/json
X-Requested-With: XMLHttpRequest
```

### Session Management
- Sessions expire after 1 hour of inactivity
- Automatic session renewal on activity
- Secure session storage with HttpOnly cookies

---

## 📋 **Core Endpoints**

### 🏠 **Home & Dashboard**

#### `GET /`
**Description**: Main dashboard page with QR code and system status

**Response**: HTML page with:
- Dynamic QR code (auto-refresh every 10 minutes)
- Real-time attendance counter
- System status indicators
- PWA manifest integration

**Example Response**:
```html
<!-- Fully rendered HTML page with embedded JavaScript -->
<div id="qr-container">
  <img src="data:image/png;base64,..." alt="QR Code">
  <p>QR Code valid until: 2025-10-05 19:45:32</p>
</div>
```

---

### 🔐 **Authentication Endpoints**

#### `POST /auth`
**Description**: QR code authentication endpoint

**Request Body**:
```json
{
  "token": "string (QR token from scan)",
  "timestamp": "ISO 8601 timestamp",
  "device_info": {
    "user_agent": "string",
    "ip_address": "string",
    "device_type": "mobile|desktop"
  }
}
```

**Success Response** (200):
```json
{
  "success": true,
  "message": "QR code valid. Proceed to face recognition.",
  "redirect_url": "/face_recognition",
  "session_token": "jwt_token_here",
  "expires_at": "2025-10-05T20:00:00Z"
}
```

**Error Responses**:

**400 - Invalid Request**:
```json
{
  "success": false,
  "error": "INVALID_TOKEN",
  "message": "QR token is invalid or malformed",
  "code": 4001
}
```

**401 - Token Expired**:
```json
{
  "success": false,
  "error": "TOKEN_EXPIRED", 
  "message": "QR code has expired. Please scan a new code.",
  "code": 4011,
  "expires_at": "2025-10-05T19:45:32Z"
}
```

**429 - Rate Limit**:
```json
{
  "success": false,
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Too many authentication attempts. Try again in 60 seconds.",
  "retry_after": 60
}
```

---

### 👤 **Face Recognition**

#### `GET /face_recognition`
**Description**: Face recognition page (requires valid session)

**Headers Required**:
```http
Authorization: Bearer {session_token}
```

**Response**: HTML page with camera interface

#### `POST /capture_image`
**Description**: Process captured face image for recognition

**Request**:
- Content-Type: `multipart/form-data`
- Body: Image file (JPEG/PNG, max 5MB)

**Request Example**:
```javascript
const formData = new FormData();
formData.append('image', imageBlob, 'capture.jpg');
formData.append('attendance_type', 'masuk'); // or 'pulang'

fetch('/capture_image', {
  method: 'POST',
  body: formData,
  headers: {
    'Authorization': 'Bearer ' + sessionToken
  }
});
```

**Success Response** (200):
```json
{
  "success": true,
  "employee": {
    "id": 123,
    "name": "John Doe",
    "position": "Software Engineer",
    "department": "IT"
  },
  "attendance": {
    "id": 456,
    "type": "masuk",
    "timestamp": "2025-10-05T08:30:00Z",
    "location": "Main Office",
    "confidence": 0.992
  },
  "message": "Attendance recorded successfully"
}
```

**Error Responses**:

**404 - Face Not Found**:
```json
{
  "success": false,
  "error": "FACE_NOT_RECOGNIZED",
  "message": "Face not recognized. Please contact HR for registration.",
  "code": 4041,
  "confidence": 0.342
}
```

**400 - Image Issues**:
```json
{
  "success": false,
  "error": "IMAGE_QUALITY_LOW",
  "message": "Image quality too low. Please ensure good lighting and face visibility.",
  "code": 4002,
  "suggestions": [
    "Improve lighting",
    "Move closer to camera", 
    "Remove glasses/mask if possible"
  ]
}
```

---

### 📊 **Data & Monitoring**

#### `GET /api/status`
**Description**: Real-time system status and statistics

**Response** (200):
```json
{
  "system": {
    "status": "healthy",
    "version": "2.0.1",
    "uptime": "72h 15m",
    "last_restart": "2025-10-02T14:30:00Z"
  },
  "database": {
    "status": "connected",
    "connections": {
      "active": 3,
      "max": 20
    },
    "response_time": "15ms"
  },
  "attendance": {
    "today": {
      "total": 45,
      "masuk": 23,
      "pulang": 22
    },
    "last_activity": "2025-10-05T15:30:00Z"
  },
  "face_recognition": {
    "model_loaded": true,
    "accuracy": 0.992,
    "total_faces": 156
  },
  "network": {
    "local_url": "http://localhost:5001",
    "ngrok_url": "https://abc123.ngrok-free.dev",
    "ngrok_status": "connected"
  }
}
```

#### `GET /api/attendance/today`
**Description**: Today's attendance summary

**Query Parameters**:
- `limit` (optional): Number of records (default: 50)
- `offset` (optional): Pagination offset (default: 0)
- `type` (optional): Filter by 'masuk' or 'pulang'

**Response** (200):
```json
{
  "success": true,
  "data": {
    "summary": {
      "total": 45,
      "masuk": 23,
      "pulang": 22,
      "present_employees": 1
    },
    "records": [
      {
        "id": 456,
        "employee_id": 123,
        "employee_name": "John Doe",
        "type": "masuk",
        "timestamp": "2025-10-05T08:30:00Z",
        "confidence": 0.992,
        "location": "Main Office"
      }
    ],
    "pagination": {
      "limit": 50,
      "offset": 0,
      "total": 45,
      "has_next": false
    }
  }
}
```

---

### 🔄 **Utility Endpoints**

#### `GET /health`
**Description**: Health check endpoint for monitoring

**Response** (200):
```json
{
  "status": "healthy",
  "timestamp": "2025-10-05T15:45:00Z",
  "checks": {
    "database": "ok",
    "face_model": "ok", 
    "ngrok": "ok"
  }
}
```

#### `GET /qr_refresh`
**Description**: Get new QR code data

**Response** (200):
```json
{
  "success": true,
  "qr_data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expires_at": "2025-10-05T20:00:00Z",
    "qr_image": "data:image/png;base64,iVBORw0KGgo..."
  }
}
```

---

## 🚨 **Error Handling**

### Standard Error Format
```json
{
  "success": false,
  "error": "ERROR_CODE",
  "message": "Human readable error message",
  "code": 4001,
  "timestamp": "2025-10-05T15:45:00Z",
  "request_id": "req_abc123",
  "details": {
    "field": "specific error details"
  }
}
```

### Common Error Codes

| Code | Error | Description |
|------|-------|-------------|
| 4001 | INVALID_TOKEN | QR token invalid or malformed |
| 4011 | TOKEN_EXPIRED | QR code has expired |
| 4041 | FACE_NOT_RECOGNIZED | Face not found in database |
| 4002 | IMAGE_QUALITY_LOW | Image quality insufficient |
| 4291 | RATE_LIMIT_EXCEEDED | Too many requests |
| 5001 | DATABASE_ERROR | Database connection issue |
| 5002 | MODEL_ERROR | Face recognition model error |
| 5003 | NGROK_ERROR | Ngrok tunnel error |

---

## 📱 **PWA Service Worker API**

### Cache Management
```javascript
// Cache attendance data offline
self.addEventListener('fetch', event => {
  if (event.request.url.includes('/api/attendance')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
  }
});
```

### Background Sync
```javascript
// Queue attendance when offline
self.addEventListener('sync', event => {
  if (event.tag === 'attendance-sync') {
    event.waitUntil(syncAttendance());
  }
});
```

---

## 🔒 **Security Considerations**

### Rate Limiting
- `/auth`: 5 requests per minute per IP
- `/capture_image`: 3 requests per minute per session
- Global: 100 requests per minute per IP

### Data Protection
- All sensitive data encrypted at rest
- Session tokens use JWT with 1-hour expiry
- Face recognition data stored as hashed features
- Audit logging for all attendance actions

### CORS Policy
```http
Access-Control-Allow-Origin: https://[ngrok-domain].ngrok-free.dev
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## 🧪 **Testing Examples**

### Test QR Authentication
```bash
curl -X POST http://localhost:5001/auth \
  -H "Content-Type: application/json" \
  -d '{"token": "test_token_123", "timestamp": "2025-10-05T15:45:00Z"}'
```

### Test System Status
```bash
curl -X GET http://localhost:5001/api/status \
  -H "Accept: application/json"
```

### Test Health Check
```bash
curl -X GET http://localhost:5001/health
```

---

## 📖 **SDK Examples**

### JavaScript/TypeScript
```typescript
class AbsennAPI {
  constructor(private baseUrl: string) {}
  
  async authenticate(token: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseUrl}/auth`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, timestamp: new Date().toISOString() })
    });
    return response.json();
  }
  
  async getStatus(): Promise<StatusResponse> {
    const response = await fetch(`${this.baseUrl}/api/status`);
    return response.json();
  }
}
```

### Python
```python
import requests
from datetime import datetime

class AbsennAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def authenticate(self, token: str) -> dict:
        response = requests.post(f"{self.base_url}/auth", json={
            "token": token,
            "timestamp": datetime.now().isoformat()
        })
        return response.json()
    
    def get_status(self) -> dict:
        response = requests.get(f"{self.base_url}/api/status")
        return response.json()
```

---

## 🔗 **Related Documentation**

- [📋 Ngrok Setup Guide](NGROK_SETUP.md)
- [🚀 Deployment Guide](DEPLOYMENT_GUIDE.md)
- [🗄️ Database Schema](DATABASE_SCHEMA.md)
- [🎨 UI/UX Guide](UI_UX_GUIDE.md)
- [🔧 Troubleshooting](../README.md#troubleshooting)

---

**Last Updated**: October 5, 2025  
**API Version**: 2.0.1  
**Documentation Version**: 1.0.0