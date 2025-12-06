# Docstring Guide - Smart Absen

## Standard Format

Gunakan **Google Style** docstrings untuk konsistensi.

## Templates

### 1. Module Docstring

```python
"""Module untuk [fungsi utama module].

Module ini menyediakan [deskripsi singkat]. Digunakan untuk [use case].

Example:
    from module_name import ClassName
    
    obj = ClassName()
    result = obj.method()

Attributes:
    CONSTANT_NAME (type): Deskripsi konstanta.
"""
```

### 2. Class Docstring

```python
class ClassName:
    """Deskripsi singkat class (satu baris).
    
    Deskripsi detail tentang fungsi class, use case, dan behavior.
    
    Attributes:
        attribute_name (type): Deskripsi attribute.
        another_attr (type): Deskripsi attribute lain.
    
    Example:
        >>> obj = ClassName(param1="value")
        >>> result = obj.method()
        >>> print(result)
        'expected output'
    """
```

### 3. Function/Method Docstring

```python
def function_name(param1, param2, optional_param=None):
    """Deskripsi singkat fungsi (satu baris).
    
    Deskripsi detail tentang apa yang dilakukan fungsi,
    edge cases, dan behavior khusus.
    
    Args:
        param1 (type): Deskripsi parameter pertama.
        param2 (type): Deskripsi parameter kedua.
        optional_param (type, optional): Deskripsi parameter opsional.
            Defaults to None.
    
    Returns:
        type: Deskripsi return value.
    
    Raises:
        ExceptionType: Kondisi kapan exception di-raise.
        AnotherException: Kondisi lain.
    
    Example:
        >>> result = function_name("value1", 123)
        >>> print(result)
        'expected output'
    
    Note:
        Catatan penting tentang fungsi ini.
    """
```

## Real Examples from Smart Absen

### Example 1: QR Sync Manager

```python
class QRSyncManager:
    """Manager untuk sinkronisasi QR code cross-device.
    
    Class ini mengelola lifecycle QR code untuk autentikasi,
    termasuk generate, verify, dan cleanup token yang expired.
    
    Attributes:
        db: Database connection object.
        validity_minutes (int): Durasi validitas QR dalam menit.
        active_tokens (dict): Cache token aktif untuk performa.
    
    Example:
        >>> manager = QRSyncManager(db_connection)
        >>> qr_data = manager.generate_qr_code()
        >>> print(qr_data['token'])
        'abc123...'
    """
    
    def generate_qr_code(self):
        """Generate QR code baru dengan token unik.
        
        Membuat token random 64 karakter, menyimpan ke database,
        dan generate QR code image dalam format base64.
        
        Returns:
            dict: Dictionary berisi:
                - token (str): Token unik 64 karakter
                - qr_image (str): Base64 encoded QR image
                - expires_at (datetime): Waktu expiry
        
        Raises:
            DatabaseError: Jika gagal menyimpan ke database.
        
        Example:
            >>> qr_data = manager.generate_qr_code()
            >>> token = qr_data['token']
            >>> img = qr_data['qr_image']
        """
        pass
    
    def verify_qr_code(self, token):
        """Verifikasi token QR code.
        
        Mengecek apakah token valid, belum expired, dan belum
        digunakan sebelumnya.
        
        Args:
            token (str): Token 64 karakter dari QR scan.
        
        Returns:
            bool: True jika valid, False jika tidak.
        
        Example:
            >>> is_valid = manager.verify_qr_code("abc123...")
            >>> if is_valid:
            ...     print("QR valid!")
        
        Note:
            Token hanya bisa digunakan sekali (one-time use).
        """
        pass
```

### Example 2: Face Recognition

```python
def recognize_face(image_array, model_path='assets/model_knn.pkl'):
    """Identifikasi wajah dari image array.
    
    Menggunakan pre-trained KNN model untuk mengenali wajah
    dari image yang sudah di-detect sebelumnya.
    
    Args:
        image_array (numpy.ndarray): Array image RGB (H, W, 3).
        model_path (str, optional): Path ke model KNN.
            Defaults to 'assets/model_knn.pkl'.
    
    Returns:
        tuple: (nama_karyawan, confidence_score)
            - nama_karyawan (str): Nama yang dikenali atau "Unknown"
            - confidence_score (float): Skor confidence 0.0-1.0
    
    Raises:
        FileNotFoundError: Jika model file tidak ditemukan.
        ValueError: Jika image_array format salah.
    
    Example:
        >>> import cv2
        >>> img = cv2.imread('face.jpg')
        >>> nama, score = recognize_face(img)
        >>> print(f"{nama}: {score:.2%}")
        'John Doe: 99.5%'
    
    Note:
        Minimum confidence threshold adalah 0.85 (85%).
    """
    pass
```

### Example 3: Database Handler

```python
class Database:
    """Handler untuk operasi database MySQL.
    
    Menyediakan methods untuk CRUD operations dengan
    connection pooling dan error handling.
    
    Attributes:
        config (dict): Database configuration.
        connection: MySQL connection object.
    """
    
    def insert_attendance(self, karyawan_id, jam_masuk, status='Hadir'):
        """Insert record absensi baru.
        
        Args:
            karyawan_id (int): ID karyawan dari tabel karyawan.
            jam_masuk (datetime): Waktu absen masuk.
            status (str, optional): Status kehadiran. 
                Defaults to 'Hadir'.
        
        Returns:
            int: ID record absensi yang baru dibuat.
        
        Raises:
            DatabaseError: Jika insert gagal.
            ValueError: Jika karyawan_id tidak valid.
        
        Example:
            >>> from datetime import datetime
            >>> db = Database(config)
            >>> record_id = db.insert_attendance(
            ...     karyawan_id=1,
            ...     jam_masuk=datetime.now()
            ... )
            >>> print(f"Record ID: {record_id}")
            'Record ID: 42'
        """
        pass
```

## Best Practices

### DO ✅

1. **Tulis docstring untuk semua public functions/classes**
   ```python
   def public_function():
       """Always document public APIs."""
       pass
   ```

2. **Gunakan type hints + docstring**
   ```python
   def add(a: int, b: int) -> int:
       """Add two integers.
       
       Args:
           a: First integer.
           b: Second integer.
       
       Returns:
           Sum of a and b.
       """
       return a + b
   ```

3. **Sertakan examples untuk fungsi kompleks**
   ```python
   def complex_function(data):
       """Process complex data.
       
       Example:
           >>> result = complex_function({'key': 'value'})
           >>> print(result)
           {'processed': True}
       """
       pass
   ```

4. **Dokumentasikan exceptions**
   ```python
   def risky_operation():
       """Perform risky operation.
       
       Raises:
           ValueError: If input invalid.
           IOError: If file not found.
       """
       pass
   ```

### DON'T ❌

1. **Jangan tulis docstring yang obvious**
   ```python
   # BAD
   def get_name(self):
       """Get name."""  # Too obvious
       return self.name
   
   # GOOD
   def get_name(self):
       """Return employee full name from database."""
       return self.name
   ```

2. **Jangan copy-paste tanpa update**
   ```python
   # BAD - Docstring tidak sesuai implementasi
   def calculate_total(items):
       """Calculate average of items."""  # WRONG!
       return sum(items)
   ```

3. **Jangan skip parameter descriptions**
   ```python
   # BAD
   def process(data, mode, verbose):
       """Process data."""  # Missing param docs
       pass
   
   # GOOD
   def process(data, mode, verbose):
       """Process data.
       
       Args:
           data: Input data to process.
           mode: Processing mode ('fast' or 'accurate').
           verbose: Enable verbose logging.
       """
       pass
   ```

## Docstring Checklist

Sebelum commit, pastikan:

- [ ] Semua public functions punya docstring
- [ ] Semua classes punya docstring
- [ ] Args dan Returns terdokumentasi
- [ ] Exceptions terdokumentasi
- [ ] Examples disertakan untuk fungsi kompleks
- [ ] Type hints konsisten dengan docstring
- [ ] Tidak ada typo atau grammar error

## Tools

### Generate Documentation

```bash
# Install pdoc
pip install pdoc3

# Generate HTML docs
pdoc --html --output-dir docs/html app.py database.py qr_sync.py

# View docs
open docs/html/index.html
```

### Validate Docstrings

```bash
# Install pydocstyle
pip install pydocstyle

# Check docstrings
pydocstyle app.py
```

---

**Last Updated:** 2025-12-07  
**Version:** 1.0
