# 📚 Smart Absen - Documentation Hub

Selamat datang di pusat dokumentasi Smart Absen! Pilih dokumentasi yang Anda butuhkan:

---

## 🚀 Quick Links

| Dokumentasi | Deskripsi | Link |
|-------------|-----------|------|
| 📖 **API Documentation** | REST API endpoints dengan Swagger UI | [/api/docs](http://localhost:5001/api/docs) |
| 🏗️ **Architecture** | System architecture & diagrams | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 📝 **Docstring Guide** | Coding standards & docstring templates | [DOCSTRING_GUIDE.md](DOCSTRING_GUIDE.md) |
| 📋 **API Spec** | OpenAPI 3.0 specification | [openapi.yaml](openapi.yaml) |
| 🎨 **Diagrams** | Draw.io architecture diagrams | [architecture_diagram.drawio](architecture_diagram.drawio) |

---

## 📖 Documentation Structure

```
docs/
├── README.md                    # This file - Documentation hub
├── ARCHITECTURE.md              # System architecture & design
├── DOCSTRING_GUIDE.md           # Docstring standards & examples
├── openapi.yaml                 # OpenAPI 3.0 specification
├── architecture_diagram.drawio  # Draw.io diagram file
└── API_DOCUMENTATION.md         # Detailed API documentation
```

---

## 🎯 For Different Roles

### 👨‍💻 **Developers**

**Getting Started:**
1. Read [ARCHITECTURE.md](ARCHITECTURE.md) untuk understand system
2. Check [DOCSTRING_GUIDE.md](DOCSTRING_GUIDE.md) untuk coding standards
3. Use Swagger UI untuk test API: http://localhost:5001/api/docs

**Key Resources:**
- API endpoints: `/api/docs`
- Code examples: `DOCSTRING_GUIDE.md`
- Database schema: `ARCHITECTURE.md` (ERD section)

---

### 🎨 **UI/UX Designers**

**Resources:**
- User flow diagrams: `ARCHITECTURE.md` (Sequence Diagrams)
- Component structure: `ARCHITECTURE.md` (Component Diagram)
- Wireframes: `/templates` folder

---

### 🔧 **System Administrators**

**Resources:**
- Deployment architecture: `ARCHITECTURE.md`
- Health check endpoint: `/health`
- Performance considerations: `ARCHITECTURE.md`

---

### 📊 **Project Managers**

**Resources:**
- System overview: `ARCHITECTURE.md`
- Technology stack: `ARCHITECTURE.md`
- Scalability plan: `ARCHITECTURE.md`

---

## 🛠️ How to Use Swagger UI

### 1. Start the Application
```bash
# Install swagger dependencies
pip install -r requirements_swagger.txt

# Run the app
python app.py
```

### 2. Access Swagger UI
Open browser: http://localhost:5001/api/docs

### 3. Test Endpoints
- Click endpoint → "Try it out"
- Fill parameters
- Click "Execute"
- See response

---

## 📐 How to Edit Architecture Diagrams

### Option 1: Draw.io Desktop
1. Download Draw.io: https://www.diagrams.net/
2. Open `architecture_diagram.drawio`
3. Edit & save

### Option 2: Draw.io Online
1. Go to https://app.diagrams.net/
2. File → Open → Select `architecture_diagram.drawio`
3. Edit & download

### Option 3: Mermaid (Markdown)
Diagrams in `ARCHITECTURE.md` use Mermaid syntax.
- View on GitHub (auto-rendered)
- Edit in VS Code with Mermaid extension
- Preview: https://mermaid.live/

---

## 📝 How to Add Docstrings

### 1. Follow Google Style
```python
def function_name(param1, param2):
    """
    Brief description.
    
    Args:
        param1 (str): Description
        param2 (int): Description
    
    Returns:
        dict: Description
    """
    pass
```

### 2. Use Type Hints
```python
def function_name(param1: str, param2: int) -> dict:
    """Docstring here"""
    pass
```

### 3. Generate Documentation
```bash
# Using pdoc3
pip install pdoc3
pdoc --html --output-dir docs/api .

# Using Sphinx
pip install sphinx
sphinx-quickstart docs
sphinx-apidoc -o docs/source .
make html
```

See [DOCSTRING_GUIDE.md](DOCSTRING_GUIDE.md) for complete guide.

---

## 🔄 Updating Documentation

### When to Update

| Change | Update |
|--------|--------|
| New API endpoint | `openapi.yaml` + Swagger UI |
| New function | Add docstring |
| Architecture change | `ARCHITECTURE.md` + diagrams |
| New feature | All relevant docs |

### Update Checklist

- [ ] Update `openapi.yaml` if API changed
- [ ] Add/update docstrings in code
- [ ] Update `ARCHITECTURE.md` if design changed
- [ ] Update diagrams if flow changed
- [ ] Test Swagger UI
- [ ] Update `CHANGELOG.md`

---

## 📊 Documentation Coverage

Current status:

| Component | Coverage | Status |
|-----------|----------|--------|
| API Endpoints | 90% | ✅ Good |
| Functions | 60% | ⚠️ Needs improvement |
| Classes | 70% | ⚠️ Needs improvement |
| Architecture | 100% | ✅ Complete |

**Goal:** 90%+ coverage for all components

---

## 🎓 Learning Resources

### Flask & Python
- Flask Documentation: https://flask.palletsprojects.com/
- Python Type Hints: https://docs.python.org/3/library/typing.html

### API Documentation
- OpenAPI Specification: https://swagger.io/specification/
- Swagger UI: https://swagger.io/tools/swagger-ui/

### Diagrams
- Mermaid Syntax: https://mermaid.js.org/
- Draw.io Tutorial: https://www.diagrams.net/doc/

### Face Recognition
- InsightFace: https://github.com/deepinsight/insightface
- OpenCV: https://docs.opencv.org/

---

## 🐛 Found Issues?

If you find errors or missing information in documentation:

1. Create GitHub issue with label `documentation`
2. Or submit PR with fixes
3. Or contact: support@smartabsen.com

---

## 📞 Support

**Documentation Team:**
- Kelompok 4 - Software Project 2025
- Email: support@smartabsen.com
- GitHub: [Repository Link]

---

## 📜 License

Documentation is licensed under MIT License.

---

**Last Updated:** 2025-12-07  
**Version:** 2.0.0  
**Maintained by:** Kelompok 4
