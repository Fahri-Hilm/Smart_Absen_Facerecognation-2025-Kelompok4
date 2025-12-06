# 🚀 Quick Start - Documentation

## Setup (5 menit)

### 1. Install Dependencies
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install Swagger UI
pip install flask-swagger-ui pyyaml

# Or use requirements file
pip install -r requirements_swagger.txt
```

### 2. Run Setup Script
```bash
chmod +x setup_docs.sh
./setup_docs.sh
```

### 3. Start Application
```bash
python app.py
```

### 4. Access Documentation
- **Swagger UI:** http://localhost:5001/api/docs
- **Architecture:** Open `docs/ARCHITECTURE.md`
- **Diagrams:** Open `docs/architecture_diagram.drawio` in Draw.io

---

## 📖 What You Get

### 1. **Swagger UI** - Interactive API Documentation
- Test all API endpoints
- See request/response examples
- Auto-generated from OpenAPI spec

**URL:** http://localhost:5001/api/docs

**Features:**
- ✅ Try endpoints directly from browser
- ✅ See all parameters & responses
- ✅ Authentication testing
- ✅ Export to Postman/Insomnia

### 2. **Architecture Diagrams** - Visual System Design
- System architecture
- Component diagram
- Sequence diagrams (QR flow, Face recognition)
- Database ERD
- Data flow diagrams

**Files:**
- `docs/ARCHITECTURE.md` - Mermaid diagrams (view on GitHub)
- `docs/architecture_diagram.drawio` - Editable in Draw.io

### 3. **Docstring Guide** - Coding Standards
- Google-style docstring templates
- Examples for functions, classes, routes
- Best practices
- Auto-documentation tools

**File:** `docs/DOCSTRING_GUIDE.md`

---

## 🎯 Common Tasks

### Test API Endpoint
1. Go to http://localhost:5001/api/docs
2. Find endpoint (e.g., `/api/employees`)
3. Click "Try it out"
4. Fill parameters
5. Click "Execute"
6. See response

### Edit Architecture Diagram
1. Open https://app.diagrams.net/
2. File → Open → `docs/architecture_diagram.drawio`
3. Edit
4. File → Save

### Add Docstring to Function
```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description.
    
    Args:
        param1 (str): Description
        param2 (int): Description
    
    Returns:
        dict: Description
    
    Example:
        >>> result = my_function("test", 123)
    """
    pass
```

### Update API Documentation
1. Edit `docs/openapi.yaml`
2. Copy to `static/openapi.yaml`
3. Restart app
4. Refresh http://localhost:5001/api/docs

---

## 📊 Documentation Checklist

When adding new feature:

- [ ] Add endpoint to `openapi.yaml`
- [ ] Add docstring to function
- [ ] Update architecture diagram if needed
- [ ] Update sequence diagram if flow changed
- [ ] Test in Swagger UI
- [ ] Update `CHANGELOG.md`

---

## 🔧 Troubleshooting

### Swagger UI not showing
```bash
# Check if installed
pip list | grep flask-swagger-ui

# Reinstall
pip install --upgrade flask-swagger-ui

# Check file exists
ls static/openapi.yaml
```

### Diagrams not rendering on GitHub
- Mermaid diagrams auto-render on GitHub
- If not, view locally with VS Code + Mermaid extension
- Or paste to https://mermaid.live/

### Draw.io file won't open
- Use online version: https://app.diagrams.net/
- Or download desktop: https://www.diagrams.net/

---

## 📚 Next Steps

1. **Read Architecture:** `docs/ARCHITECTURE.md`
2. **Explore API:** http://localhost:5001/api/docs
3. **Add Docstrings:** Follow `docs/DOCSTRING_GUIDE.md`
4. **Generate Docs:** Use Sphinx or pdoc3

---

## 💡 Pro Tips

### 1. Auto-reload Swagger UI
Edit `openapi.yaml` → Save → Refresh browser (no restart needed)

### 2. Export API to Postman
Swagger UI → Download → Import to Postman

### 3. Generate Client Code
Swagger UI → Generate Client → Choose language

### 4. View Mermaid in VS Code
Install extension: "Markdown Preview Mermaid Support"

### 5. Keep Docs Updated
Set reminder: Update docs every sprint/release

---

**Need Help?** Check `docs/README.md` for full documentation index.
