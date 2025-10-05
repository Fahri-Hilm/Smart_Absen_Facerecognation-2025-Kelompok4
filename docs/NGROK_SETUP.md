# 🔐 NGROK SETUP GUIDE

## Langkah-langkah Setup Ngrok Authtoken:

### 1. Buka Dashboard Ngrok
Pergi ke: https://dashboard.ngrok.com/get-started/your-authtoken

### 2. Copy Authtoken
Setelah login dengan GitHub, Anda akan melihat authtoken di dashboard.
Copy token yang terlihat seperti: `2abc123def456ghi789jkl...`

### 3. Install Authtoken
Jalankan command berikut dengan authtoken Anda:

```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

Contoh:
```bash
ngrok config add-authtoken 2abc123def456ghi789jkl012mno345pqr678stu
```

### 4. Verify Setup
Setelah authtoken diset, test dengan:
```bash
ngrok config check
```

### 5. Test Ngrok
Test tunnel manual:
```bash
ngrok http 5001
```

### 6. Jalankan ABSENN
Setelah authtoken berhasil diset:
```bash
./start_ngrok.sh
# atau
./start_both.sh
```

## Troubleshooting

Jika masih error:
1. Pastikan account ngrok sudah verified (cek email)
2. Pastikan authtoken copied dengan benar (tidak ada spasi)
3. Restart terminal setelah setup authtoken

## Quick Commands

```bash
# Check ngrok status
ngrok config check

# View ngrok config
cat ~/.ngrok2/ngrok.yml

# Test manual tunnel
ngrok http 5001

# Start ABSENN with ngrok
./start_ngrok.sh
```