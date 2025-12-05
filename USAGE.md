# 📖 Usage Guide

> Panduan penggunaan Smart Absen Face Recognition System

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [User Roles](#-user-roles)
3. [Flow Absensi (Karyawan)](#-flow-absensi-karyawan)
4. [Admin Panel](#-admin-panel)
5. [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

Smart Absen memiliki 2 mode utama:
1. **Mode Absensi** - Untuk karyawan melakukan absen masuk/pulang
2. **Mode Admin** - Untuk mengelola karyawan dan melihat laporan

---

## 👥 User Roles

| Role | Akses | Deskripsi |
|------|-------|-----------|
| **Karyawan** | `/auth`, `/web_attendance` | Melakukan absensi |
| **Admin** | `/admin/*` | Full access |
| **Supervisor** | `/admin/*` | View & manage reports |

### Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| supervisor | super123 | Supervisor |

---

## 🕐 Flow Absensi (Karyawan)

### Diagram Alur

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ALUR ABSENSI LENGKAP                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌───────┐ │
│  │  START  │───►│ QR Page │───►│  Scan   │───►│ Absensi │───►│ DONE  │ │
│  └─────────┘    │ (Laptop)│    │  (HP)   │    │ (Laptop)│    └───────┘ │
│                 └─────────┘    └─────────┘    └─────────┘              │
│                                                                         │
│  Step 1         Step 2         Step 3         Step 4-6       Step 7    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Step 1: Buka Halaman QR (Laptop)

**URL:** `http://localhost:5001/auth` atau `https://[tunnel-url]/auth`

**Tampilan:**
```
┌──────────────────────────────────────────────────────┐
│                  Smart Absen                         │
│                                                      │
│  ┌────────────────┐    ┌────────────────────────┐   │
│  │                │    │                        │   │
│  │    [QR CODE]   │    │  Petunjuk:             │   │
│  │                │    │  1. Scan QR dengan HP  │   │
│  │                │    │  2. Tunggu redirect    │   │
│  └────────────────┘    │  3. Absen dengan wajah │   │
│                        │                        │   │
│  Code: ABC123          │  Atau masukkan kode    │   │
│                        │  secara manual:        │   │
│                        │  [___________] [OK]    │   │
│                        └────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Yang Harus Dilakukan:**
1. ✅ Biarkan halaman ini terbuka di laptop
2. ✅ QR Code akan auto-refresh setiap 5 menit
3. ✅ Catat kode di bawah QR (backup jika scan gagal)

---

### Step 2: Scan QR Code (HP)

**Cara Scan:**
1. Buka aplikasi kamera HP
2. Arahkan ke QR Code di layar laptop
3. Tap link yang muncul

**Alternatif (Manual Input):**
1. Di laptop, lihat kode di bawah QR (misal: `ABC123`)
2. Masukkan kode di form "Masukkan kode manual"
3. Klik "OK"

---

### Step 3: Verifikasi di HP

**Tampilan di HP setelah scan:**
```
┌─────────────────────────────────┐
│                                 │
│         ✅ KUNCI TERBUKA        │
│                                 │
│   Silakan lanjutkan absensi     │
│   di laptop Anda                │
│                                 │
│   ─────────────────────────     │
│                                 │
│   Halaman ini akan otomatis     │
│   tertutup dalam 5 detik        │
│                                 │
└─────────────────────────────────┘
```

**Yang Terjadi:**
- ✅ HP menampilkan konfirmasi "Kunci Terbuka"
- ✅ Laptop otomatis redirect ke halaman absensi
- ✅ HP bisa ditutup setelah ini

---

### Step 4: Pilih Mode Absensi (Laptop)

**Tampilan Halaman Absensi:**
```
┌──────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐                 │
│  │ ABSEN MASUK  │  │ ABSEN PULANG │   ← Tab Mode    │
│  └──────────────┘  └──────────────┘                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────┐  ┌────────────────────────┐ │
│  │                    │  │                        │ │
│  │    [CAMERA FEED]   │  │  Status: Mendeteksi   │ │
│  │                    │  │                        │ │
│  │   ┌──────────┐     │  │  Nama: -              │ │
│  │   │  Wajah   │     │  │  Waktu: 08:00:00      │ │
│  │   └──────────┘     │  │                        │ │
│  │                    │  │  [ABSEN SEKARANG]     │ │
│  └────────────────────┘  └────────────────────────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Pilih Tab:**
- 🟢 **ABSEN MASUK** - Untuk absensi pagi/masuk kerja
- 🔵 **ABSEN PULANG** - Untuk absensi sore/pulang kerja

---

### Step 5: Face Scan

**Persiapan:**
1. ✅ Pastikan pencahayaan cukup
2. ✅ Lepas kacamata hitam/masker
3. ✅ Hadapkan wajah ke kamera
4. ✅ Jaga jarak 30-60 cm dari kamera

**Indikator Deteksi:**
| Indikator | Artinya |
|-----------|---------|
| Kotak HIJAU | Wajah terdeteksi, siap absen |
| Kotak MERAH | Wajah terdeteksi tapi tidak dikenali |
| Tidak ada kotak | Wajah tidak terdeteksi |

---

### Step 6: Submit Absensi

**Klik tombol "ABSEN SEKARANG"**

**Proses:**
1. Sistem capture wajah
2. Face recognition memverifikasi identitas
3. Data absensi disimpan ke database

---

### Step 7: Konfirmasi Sukses

**Popup Sukses:**
```
┌─────────────────────────────────────┐
│                                     │
│            ✅ BERHASIL!             │
│                                     │
│   Nama: John Doe                    │
│   Waktu: 08:00:15                   │
│   Mode: Absen Masuk                 │
│                                     │
│   Redirect dalam 5 detik...         │
│                                     │
└─────────────────────────────────────┘
```

**Setelah 5 detik:**
- Otomatis redirect ke halaman QR (`/auth`)
- Siap untuk karyawan berikutnya

---

## 🔧 Admin Panel

### Login Admin

**URL:** `http://localhost:5001/admin/login`

```
┌──────────────────────────────────────┐
│           ADMIN LOGIN                │
│                                      │
│   Username: [____________]           │
│   Password: [____________]           │
│                                      │
│          [LOGIN]                     │
│                                      │
└──────────────────────────────────────┘
```

---

### Dashboard Admin

**URL:** `http://localhost:5001/admin/dashboard`

```
┌──────────────────────────────────────────────────────────────────┐
│  SMART ABSEN - ADMIN DASHBOARD                    [Logout]       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  KARYAWAN    │  │   HADIR      │  │   TERLAMBAT  │           │
│  │     25       │  │     20       │  │      3       │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MENU                                                      │ │
│  │                                                            │ │
│  │  [👥 Kelola Karyawan]    [📊 Laporan Absensi]             │ │
│  │  [⚙️ Pengaturan]         [📷 Training Model]              │ │
│  │                                                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

### Menu Admin

#### 1. Kelola Karyawan (`/admin/employees`)

**Fungsi:**
- ➕ Tambah karyawan baru
- ✏️ Edit data karyawan
- 🗑️ Hapus karyawan
- 👁️ Lihat detail karyawan

**Tabel Karyawan:**
```
┌─────┬──────────┬─────────────┬───────────┬────────────┬─────────┐
│ No  │ NIK      │ Nama        │ Jabatan   │ Departemen │ Aksi    │
├─────┼──────────┼─────────────┼───────────┼────────────┼─────────┤
│ 1   │ EMP001   │ John Doe    │ Staff     │ IT         │ [✏️][🗑️]│
│ 2   │ EMP002   │ Jane Smith  │ Manager   │ HR         │ [✏️][🗑️]│
│ 3   │ EMP003   │ Bob Wilson  │ Staff     │ Finance    │ [✏️][🗑️]│
└─────┴──────────┴─────────────┴───────────┴────────────┴─────────┘

[+ Tambah Karyawan Baru]
```

---

#### 2. Laporan Absensi (`/admin/attendance`)

**Filter:**
- 📅 Tanggal: [Dari] - [Sampai]
- 👤 Karyawan: [Semua / Pilih]
- 📊 Status: [Semua / Hadir / Terlambat / Tidak Hadir]

**Tabel Laporan:**
```
┌──────────┬─────────────┬───────────┬───────────┬──────────┐
│ Tanggal  │ Nama        │ Jam Masuk │ Jam Pulang│ Status   │
├──────────┼─────────────┼───────────┼───────────┼──────────┤
│ 05/12/25 │ John Doe    │ 07:55:00  │ 17:05:00  │ ✅ Hadir  │
│ 05/12/25 │ Jane Smith  │ 08:15:00  │ 17:00:00  │ ⚠️ Telat  │
│ 05/12/25 │ Bob Wilson  │ -         │ -         │ ❌ Absen  │
└──────────┴─────────────┴───────────┴───────────┴──────────┘

[📥 Export PDF]  [📥 Export Excel]
```

---

#### 3. Training Model (🚧 Coming Soon)

**Fungsi yang akan datang:**
- 📸 Capture foto wajah langsung dari dashboard
- 📤 Upload foto manual
- 🔄 Re-train model
- 📊 Status training

---

## 🔧 Troubleshooting

### QR Code Tidak Ter-scan

**Solusi:**
1. Pastikan QR code terlihat jelas (tidak blur)
2. Coba zoom in pada QR code
3. Gunakan input manual (ketik kode)

### Wajah Tidak Terdeteksi

**Solusi:**
1. Tingkatkan pencahayaan ruangan
2. Jaga jarak 30-60 cm dari kamera
3. Hadapkan wajah langsung ke kamera
4. Lepas kacamata/masker

### Wajah Terdeteksi Tapi Tidak Dikenali

**Solusi:**
1. Pastikan sudah ada data training
2. Minta admin untuk menambah foto training
3. Pastikan pencahayaan serupa dengan foto training

### Laptop Tidak Auto-Redirect

**Solusi:**
1. Refresh halaman QR di laptop
2. Pastikan HP dan laptop di jaringan yang sama (mode lokal)
3. Gunakan Cloudflare Tunnel untuk lintas jaringan
4. Cek console browser untuk error

### Kamera Tidak Muncul

**Solusi:**
1. Allow camera permission di browser
2. Pastikan tidak ada aplikasi lain yang menggunakan kamera
3. Gunakan HTTPS (Cloudflare Tunnel) jika dari HP
4. Coba browser lain (Chrome recommended)

---

## 📞 Bantuan

Jika mengalami masalah:
1. Cek dokumentasi troubleshooting di atas
2. Hubungi admin sistem
3. Buat issue di GitHub repository

---

<p align="center">
  <b>Smart Absen - Kelompok 4</b>
</p>
