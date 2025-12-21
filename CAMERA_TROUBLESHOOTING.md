# 📷 Camera Troubleshooting Guide

## Masalah: Tombol "Ambil Foto" tidak bisa diklik dan kamera tidak terbuka

### ✅ Solusi yang Sudah Diterapkan:

1. **Fixed JavaScript Issues:**
   - Memperbaiki ID element video dari `videoElement` ke `trainingWebcam`
   - Menambahkan event listeners untuk semua tombol
   - Memperbaiki parameter URL dari `id` ke `employee_id`
   - Menambahkan mode switching dan file upload handler

2. **Added Debug Page:**
   - Akses: http://localhost:5001/camera-debug
   - Test kamera secara langsung tanpa form

### 🔧 Langkah Troubleshooting:

#### 1. Test Kamera Basic
```bash
# Buka browser dan akses:
http://localhost:5001/camera-debug
```

#### 2. Periksa Permission Browser
- **Chrome/Edge:** Klik ikon kamera di address bar → Allow
- **Firefox:** Klik ikon kamera di address bar → Allow
- **Safari:** Safari → Preferences → Websites → Camera → Allow

#### 3. Periksa Kamera Hardware
```bash
# Linux - cek device kamera
ls /dev/video*

# Jika tidak ada output, kamera tidak terdeteksi
# Install v4l-utils untuk troubleshooting
sudo apt install v4l-utils
v4l2-ctl --list-devices
```

#### 4. Test di Browser Lain
- Chrome: `google-chrome --use-fake-ui-for-media-stream`
- Firefox: about:config → media.navigator.permission.disabled = true

#### 5. Periksa HTTPS Requirement
Modern browsers require HTTPS for camera access. Solutions:
- Use localhost (works with HTTP)
- Use Cloudflare Tunnel for HTTPS
- Use ngrok for HTTPS tunnel

### 🚀 Cara Menggunakan Setelah Fix:

1. **Buka Form Tambah Karyawan:**
   ```
   http://localhost:5001/admin/add_employee_form
   ```

2. **Isi Data Karyawan** dan klik "Simpan & Lanjut ke Capture Wajah"

3. **Di Halaman Capture Wajah:**
   - Kamera akan otomatis menyala
   - Pilih mode: Manual, Auto, atau Upload
   - Ambil minimal 5 foto dari sudut berbeda
   - Klik "Selesai & Simpan"

### 🔍 Debug Steps:

#### Check Console Errors:
```javascript
// Buka Developer Tools (F12) dan cek Console
// Error umum:
// - "Permission denied" → Allow camera permission
// - "NotFoundError" → No camera detected
// - "NotAllowedError" → User denied permission
```

#### Manual Camera Test:
```javascript
// Test di Console browser:
navigator.mediaDevices.getUserMedia({video: true})
  .then(stream => console.log('Camera OK:', stream))
  .catch(err => console.error('Camera Error:', err));
```

### 📱 Mobile Browser Issues:

#### Android Chrome:
- Settings → Site Settings → Camera → Allow
- Clear browser cache and cookies

#### iOS Safari:
- Settings → Safari → Camera → Ask/Allow
- Restart Safari after permission change

### 🔧 Advanced Troubleshooting:

#### 1. Check Camera Process:
```bash
# Check if camera is used by other process
sudo lsof /dev/video0
```

#### 2. Restart Camera Service:
```bash
# Ubuntu/Debian
sudo systemctl restart uvcvideo
# or
sudo modprobe -r uvcvideo && sudo modprobe uvcvideo
```

#### 3. Check Browser Flags:
Chrome: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
Add: `http://localhost:5001`

### 📋 Error Messages & Solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| "Camera access denied" | Permission not granted | Allow camera in browser |
| "NotFoundError" | No camera detected | Check hardware connection |
| "NotAllowedError" | User denied permission | Reset site permissions |
| "NotReadableError" | Camera in use by other app | Close other camera apps |
| "OverconstrainedError" | Unsupported camera settings | Try different resolution |

### ✅ Verification Checklist:

- [ ] Camera hardware connected and working
- [ ] Browser permissions allowed
- [ ] JavaScript console shows no errors
- [ ] http://localhost:5001/camera-debug works
- [ ] Video element shows camera feed
- [ ] Buttons are clickable and responsive
- [ ] Photos can be captured and saved

### 🆘 Still Not Working?

1. **Try Different Browser:** Chrome, Firefox, Edge
2. **Check System Camera:** Use system camera app first
3. **Restart Browser:** Close all tabs and restart
4. **Clear Browser Data:** Cache, cookies, site data
5. **Use External Camera:** If laptop camera fails
6. **Check Antivirus:** May block camera access

### 📞 Contact Support:
If issues persist, provide:
- Browser name and version
- Operating system
- Console error messages
- Screenshot of camera-debug page
