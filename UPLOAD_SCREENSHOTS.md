# 📸 Upload Screenshots ke Imgur

## 🎯 Screenshot yang Dibutuhkan

1. **Dashboard Utama** - Halaman utama dengan statistik
2. **Face Recognition** - Proses deteksi wajah
3. **QR Code Sync** - Halaman QR sync
4. **Admin Panel** - Panel admin/manajemen

---

## 📋 Langkah Upload

### 1. Ambil Screenshot
- Jalankan aplikasi: `python app.py` atau `docker run ...`
- Buka browser: http://localhost:5001
- Screenshot setiap halaman (Windows: Win+Shift+S, Mac: Cmd+Shift+4)

### 2. Upload ke Imgur

**Untuk setiap screenshot:**

1. Buka: https://imgur.com/upload
2. Drag & drop file screenshot
3. Tunggu upload selesai
4. Klik kanan pada gambar → **"Copy image address"** atau **"Get share links"**
5. Copy **Direct Link** (format: `https://i.imgur.com/xxxxx.png`)

### 3. Update README.md

Ganti placeholder dengan link Imgur:

**Before:**
```markdown
![Dashboard](https://i.imgur.com/PLACEHOLDER1.png)
```

**After:**
```markdown
![Dashboard](https://i.imgur.com/AbCd123.png)
```

---

## 🔗 Format Link Imgur

**Direct Link (yang dipakai):**
```
https://i.imgur.com/AbCd123.png
```

**Bukan ini:**
```
https://imgur.com/AbCd123  ❌ (halaman Imgur, bukan direct image)
```

---

## 📝 Mapping Screenshot ke README

| Screenshot | Placeholder | Section |
|------------|-------------|---------|
| Dashboard utama | PLACEHOLDER1 | Dashboard Utama |
| Face recognition | PLACEHOLDER2 | Face Recognition |
| QR sync | PLACEHOLDER3 | QR Code Sync |
| Admin panel | PLACEHOLDER4 | Admin Panel |

---

## ✅ Checklist

- [ ] Screenshot 1: Dashboard utama
- [ ] Screenshot 2: Face recognition
- [ ] Screenshot 3: QR sync
- [ ] Screenshot 4: Admin panel
- [ ] Upload ke Imgur (4 files)
- [ ] Copy 4 direct links
- [ ] Update README.md
- [ ] Commit & push

---

## 🚀 Quick Commands

```bash
# Setelah update README.md
cd /home/fj/Desktop/PROJECT/Campus/SOFTWARE\ PROJECT/Absenn
git add README.md
git commit -m "Add screenshots to README"
git push origin main
```

---

## 💡 Tips

1. **Resolusi:** 1920x1080 atau 1280x720 (HD)
2. **Format:** PNG (lebih tajam) atau JPG (lebih kecil)
3. **Crop:** Fokus ke konten utama, buang bagian tidak penting
4. **Blur:** Blur data sensitif (nama, foto wajah real) jika perlu
5. **Lighting:** Pastikan UI terlihat jelas

---

## 🎨 Contoh Screenshot Bagus

**Dashboard:**
- Tampilkan statistik lengkap
- Ada data attendance
- Terlihat professional

**Face Recognition:**
- Capture saat proses deteksi
- Tampilkan bounding box wajah
- Terlihat accuracy indicator

**QR Sync:**
- Tampilkan QR code
- Terlihat instruksi penggunaan

**Admin Panel:**
- Tampilkan tabel data
- Terlihat menu navigasi

---

**Ready to upload!** 📸
