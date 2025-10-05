import requests

# Pilih karyawan yang ingin dihapus
print("Karyawan yang tersedia:")
print("1. Faju (Staff)")
print("2. fj (Karyawan)")

choice = input("\nPilih nomor karyawan yang ingin dihapus (1 atau 2): ")

if choice == "1":
    name = "Faju"
    bagian = "Staff"
elif choice == "2":
    name = "fj"
    bagian = "Karyawan"
else:
    print("Pilihan tidak valid!")
    exit()

# Konfirmasi
confirm = input(f"\nYakin ingin menghapus karyawan {name} ({bagian})? (y/n): ")
if confirm.lower() != 'y':
    print("Dibatalkan.")
    exit()

# Kirim request delete
url = "http://127.0.0.1:5001/delete_employee"
data = {
    'name': name,
    'bagian': bagian
}

try:
    print(f"\nMenghapus karyawan {name} ({bagian})...")
    response = requests.post(url, data=data)
    result = response.json()
    
    if result['status'] == 'success':
        print(f"✅ {result['message']}")
        print("Karyawan berhasil dihapus dari sistem!")
    else:
        print(f"❌ Error: {result['message']}")
        
except Exception as e:
    print(f"❌ Error: {e}")