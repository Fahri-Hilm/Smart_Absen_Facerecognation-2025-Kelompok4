# 🤝 Contributing Guide

> Panduan kontribusi untuk Smart Absen Face Recognition System

---

## 📋 Table of Contents

1. [Getting Started](#-getting-started)
2. [Development Setup](#-development-setup)
3. [Project Structure](#-project-structure)
4. [Coding Standards](#-coding-standards)
5. [Git Workflow](#-git-workflow)
6. [Pull Request Process](#-pull-request-process)
7. [Testing](#-testing)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Git
- VS Code (recommended)

### Quick Setup

```bash
# 1. Fork repository di GitHub

# 2. Clone fork Anda
git clone https://github.com/YOUR_USERNAME/Smart_Absen_Facerecognation-2025-Kelompok4.git
cd Smart_Absen_Facerecognation-2025-Kelompok4

# 3. Add upstream remote
git remote add upstream https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4.git

# 4. Setup environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Setup database & config
# (Lihat INSTALLATION.md)

# 6. Run application
python app.py
```

---

## 💻 Development Setup

### VS Code Extensions (Recommended)

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "mtxr.sqltools",
    "ritwickdey.LiveServer"
  ]
}
```

### Environment Variables

Buat file `.env` (jangan commit!):

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=absensi_karyawan_db
SECRET_KEY=your-dev-secret-key
DEBUG=True
```

---

## 📁 Project Structure

```
Smart_Absen/
│
├── app.py                 # ⭐ Main application entry point
│   ├── Routes             # URL endpoints
│   ├── Face Recognition   # FR logic
│   └── QR Sync            # Cross-device sync
│
├── config.py              # Configuration
├── database.py            # DB connection handler
├── models.py              # Data models
│
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base template
│   ├── qr_auth.html       # QR authentication
│   ├── web_attendance.html# Attendance page
│   └── admin/             # Admin templates
│
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript
│   └── images/            # Images
│
└── docs/                  # Documentation
```

### Key Files

| File | Purpose | Owner |
|------|---------|-------|
| `app.py` | Main Flask app, semua routes | Backend |
| `templates/*.html` | UI templates | Frontend |
| `static/css/*.css` | Styling | Frontend |
| `database.py` | DB operations | Backend |

---

## 📝 Coding Standards

### Python Style Guide

Ikuti **PEP 8** dengan tambahan:

```python
# ✅ Good
def get_employee_by_id(employee_id: int) -> dict:
    """
    Mengambil data karyawan berdasarkan ID.
    
    Args:
        employee_id: ID karyawan
        
    Returns:
        Dictionary berisi data karyawan
    """
    pass

# ❌ Bad
def getEmp(id):
    pass
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `employee_name` |
| Functions | snake_case | `get_employee()` |
| Classes | PascalCase | `EmployeeManager` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Files | snake_case | `employee_manager.py` |

### HTML/CSS Standards

```html
<!-- ✅ Good: Semantic HTML -->
<section class="attendance-form">
    <header class="form-header">
        <h2>Absensi Karyawan</h2>
    </header>
    <main class="form-content">
        <!-- content -->
    </main>
</section>

<!-- ❌ Bad: Div soup -->
<div class="div1">
    <div class="div2">
        <div class="div3">
        </div>
    </div>
</div>
```

### JavaScript Standards

```javascript
// ✅ Good: ES6+, descriptive names
const fetchEmployeeData = async (employeeId) => {
    try {
        const response = await fetch(`/api/employee/${employeeId}`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch employee:', error);
        throw error;
    }
};

// ❌ Bad: Old syntax, unclear names
function getData(id, callback) {
    var xhr = new XMLHttpRequest();
    // ...
}
```

---

## 🔀 Git Workflow

### Branch Naming

```
<type>/<description>

Types:
- feature/  → Fitur baru
- bugfix/   → Perbaikan bug
- hotfix/   → Perbaikan urgent
- docs/     → Dokumentasi
- refactor/ → Refactoring code
```

**Examples:**
```
feature/dashboard-training
bugfix/camera-not-detected
docs/update-readme
refactor/optimize-face-recognition
```

### Commit Messages

Format: `<type>: <description>`

```bash
# Types
feat:     # Fitur baru
fix:      # Bug fix
docs:     # Dokumentasi
style:    # Formatting (tidak mengubah logic)
refactor: # Refactoring
test:     # Testing
chore:    # Maintenance

# Examples
git commit -m "feat: add face training dashboard"
git commit -m "fix: camera not detected on firefox"
git commit -m "docs: update installation guide"
```

### Workflow Steps

```bash
# 1. Sync dengan upstream
git checkout main
git fetch upstream
git merge upstream/main

# 2. Buat branch baru
git checkout -b feature/your-feature

# 3. Code & commit
git add .
git commit -m "feat: your feature description"

# 4. Push ke fork Anda
git push origin feature/your-feature

# 5. Buat Pull Request di GitHub
```

---

## 🔄 Pull Request Process

### Before Creating PR

- [ ] Code berjalan tanpa error
- [ ] Tidak ada conflict dengan main
- [ ] Sudah test manual
- [ ] Code sesuai style guide
- [ ] Dokumentasi di-update (jika perlu)

### PR Template

```markdown
## Description
Jelaskan perubahan yang dilakukan.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Langkah-langkah untuk test:
1. ...
2. ...

## Screenshots (if applicable)
Tambahkan screenshot jika ada perubahan UI.

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

1. **Automated Checks** - Linting, build
2. **Code Review** - Minimal 1 approval
3. **Testing** - Manual testing
4. **Merge** - Squash merge ke main

---

## 🧪 Testing

### Manual Testing Checklist

```markdown
## Core Features
- [ ] QR code generation works
- [ ] QR scan redirects correctly
- [ ] Face detection works
- [ ] Face recognition identifies correctly
- [ ] Attendance data saved to database
- [ ] Admin login works
- [ ] Admin can view employees
- [ ] Admin can view attendance

## Cross-browser
- [ ] Chrome
- [ ] Firefox
- [ ] Edge

## Responsive
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Mobile (375x667)
```

### Running Tests

```bash
# (Future implementation)
python -m pytest tests/
```

---

## 📞 Questions?

Jika ada pertanyaan:
1. Cek dokumentasi yang ada
2. Buat Issue di GitHub
3. Diskusi di group chat tim

---

<p align="center">
  <b>Happy Contributing! 🎉</b>
</p>
