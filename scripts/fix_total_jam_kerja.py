#!/usr/bin/env python3
"""
Script untuk memperbaiki total jam kerja yang null di database
"""

from database import get_db_manager
from models import Attendance
from datetime import timedelta

def fix_total_jam_kerja():
    """Perbaiki data total_jam_kerja yang null atau salah"""
    print("🔧 Memperbaiki data total jam kerja...")
    
    db = get_db_manager()
    
    # Ambil semua data attendance yang total_jam_kerja-nya null atau memiliki jam masuk dan pulang
    query = """
    SELECT id, jam_masuk, jam_pulang, total_jam_kerja 
    FROM attendance 
    WHERE (total_jam_kerja IS NULL OR total_jam_kerja = '') 
    AND jam_masuk IS NOT NULL 
    AND jam_pulang IS NOT NULL
    """
    
    records = db.execute_query(query)
    if not records:
        print("✅ Tidak ada data yang perlu diperbaiki")
        return
    
    print(f"📊 Ditemukan {len(records)} record yang perlu diperbaiki")
    
    fixed_count = 0
    for record in records:
        try:
            # Hitung total jam kerja
            total_jam = Attendance.calculate_work_hours(record['jam_masuk'], record['jam_pulang'])
            
            if total_jam:
                # Update database
                update_query = "UPDATE attendance SET total_jam_kerja = %s WHERE id = %s"
                result = db.execute_query(update_query, (total_jam, record['id']))
                
                if result:
                    print(f"✅ Fixed ID {record['id']}: {record['jam_masuk']} - {record['jam_pulang']} = {total_jam}")
                    fixed_count += 1
                else:
                    print(f"❌ Failed to update ID {record['id']}")
            else:
                print(f"⚠️  Could not calculate for ID {record['id']}")
                
        except Exception as e:
            print(f"❌ Error processing ID {record['id']}: {e}")
    
    print(f"\n🎯 Selesai! {fixed_count} dari {len(records)} record berhasil diperbaiki")
    
    # Tampilkan data terbaru
    print("\n📋 Data attendance terbaru:")
    recent_data = db.execute_query("SELECT * FROM attendance ORDER BY tanggal DESC LIMIT 5")
    if recent_data:
        for row in recent_data:
            print(f"ID: {row['id']}, Tanggal: {row['tanggal']}")
            print(f"  Masuk: {row['jam_masuk']}, Pulang: {row['jam_pulang']}")
            print(f"  Total: {row['total_jam_kerja']}")
            print("---")

if __name__ == "__main__":
    fix_total_jam_kerja()