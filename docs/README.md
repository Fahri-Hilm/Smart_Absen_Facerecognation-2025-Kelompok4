# 📚 Documentation Hub

**Version:** 2.1.0 | **Last Updated:** 2025-12-07

Welcome to Smart Absen Face Recognition System documentation center.

---

## 🚀 Quick Links

| Document | Description | Audience |
|----------|-------------|----------|
| [README.md](../README.md) | Project overview & quick start | Everyone |
| [INSTALLATION.md](../INSTALLATION.md) | Installation guide (Docker & Manual) | Developers |
| [DOCKER_DEPLOYMENT.md](../DOCKER_DEPLOYMENT.md) | Complete Docker deployment guide | DevOps |
| [DOCKER_QUICKSTART.md](../DOCKER_QUICKSTART.md) | Docker quick reference | DevOps |
| [USAGE.md](../USAGE.md) | User guide & features | End Users |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guidelines | Contributors |

---

## 📖 Technical Documentation

### Architecture & Design
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture & design patterns
- [API.md](API.md) - REST API endpoints documentation
- [FRONTEND.md](FRONTEND.md) - Frontend development guide

### Diagrams
- [architecture_diagram.drawio](architecture_diagram.drawio) - System architecture (Draw.io)
- [system_architecture.puml](system_architecture.puml) - Architecture (PlantUML)
- [class_diagram.puml](class_diagram.puml) - Class diagram
- [sequence_diagram.puml](sequence_diagram.puml) - Sequence diagram
- [activity_diagram.puml](activity_diagram.puml) - Activity diagram
- [deployment_diagram.puml](deployment_diagram.puml) - Deployment diagram
- [database_erd.puml](database_erd.puml) - Database ERD

### Development
- [DOCSTRING_GUIDE.md](DOCSTRING_GUIDE.md) - Code documentation standards
- [openapi.yaml](openapi.yaml) - OpenAPI 3.0 specification

---

## 🐳 Docker Documentation

### Quick Start
```bash
# Pull & run
docker pull ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
docker run -d -p 5001:5001 --env-file .env \
  ghcr.io/fahri-hilm/smart_absen_facerecognation-2025-kelompok4:latest
```

### Full Guides
- **[DOCKER_DEPLOYMENT.md](../DOCKER_DEPLOYMENT.md)** - Complete deployment guide
  - Prerequisites & installation
  - Build & push to GHCR
  - Production deployment
  - Troubleshooting
  - Security notes
  
- **[DOCKER_QUICKSTART.md](../DOCKER_QUICKSTART.md)** - Quick reference
  - Common commands
  - Docker Compose usage
  - Debug commands
  - Update procedures

---

## 🔒 Security & Operations

- [SECURITY.md](../SECURITY.md) - Security best practices & implementation
- [STATUS.md](../STATUS.md) - System status & verification report
- [CHANGELOG.md](../CHANGELOG.md) - Version history & changes

---

## 📋 Documentation Index

### Root Level Documentation
1. **README.md** - Project overview, tech stack, quick start
2. **INSTALLATION.md** - Setup guide (Docker & manual)
3. **USAGE.md** - User guide & feature walkthrough
4. **CONTRIBUTING.md** - How to contribute
5. **CHANGELOG.md** - Version history
6. **SECURITY.md** - Security implementation
7. **STATUS.md** - System verification report
8. **DOCKER_DEPLOYMENT.md** - Docker deployment guide ✨ NEW
9. **DOCKER_QUICKSTART.md** - Docker quick reference ✨ NEW

### Technical Docs (docs/)
10. **ARCHITECTURE.md** - System architecture
11. **API.md** - API documentation
12. **FRONTEND.md** - Frontend guide
13. **DOCSTRING_GUIDE.md** - Code documentation standards
14. **openapi.yaml** - OpenAPI specification

### Diagrams (docs/)
15. **architecture_diagram.drawio** - Visual architecture
16. **system_architecture.puml** - PlantUML architecture
17. **class_diagram.puml** - Class relationships
18. **sequence_diagram.puml** - Interaction flows
19. **activity_diagram.puml** - Process flows
20. **deployment_diagram.puml** - Deployment topology
21. **database_erd.puml** - Database schema

---

## 🎯 Documentation by Role

### For End Users
1. [README.md](../README.md) - What is this project?
2. [USAGE.md](../USAGE.md) - How to use the system?

### For Developers
1. [INSTALLATION.md](../INSTALLATION.md) - How to install?
2. [ARCHITECTURE.md](ARCHITECTURE.md) - How is it built?
3. [API.md](API.md) - What are the endpoints?
4. [FRONTEND.md](FRONTEND.md) - How to modify UI?
5. [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute?

### For DevOps Engineers
1. [DOCKER_DEPLOYMENT.md](../DOCKER_DEPLOYMENT.md) - How to deploy with Docker?
2. [DOCKER_QUICKSTART.md](../DOCKER_QUICKSTART.md) - Quick Docker commands
3. [SECURITY.md](../SECURITY.md) - Security considerations
4. [STATUS.md](../STATUS.md) - System health & metrics

### For Project Managers
1. [README.md](../README.md) - Project overview
2. [CHANGELOG.md](../CHANGELOG.md) - What changed?
3. [STATUS.md](../STATUS.md) - Current status
4. [ARCHITECTURE.md](ARCHITECTURE.md) - Technical overview

---

## 🔄 Documentation Updates

### Version 2.1.0 (2025-12-07)
- ✅ Added Docker deployment documentation
- ✅ Added Docker quickstart guide
- ✅ Updated INSTALLATION.md with Docker section
- ✅ Updated CHANGELOG.md with v2.1 changes
- ✅ Updated STATUS.md with Docker metrics
- ✅ Updated README.md with Docker quick start

### Version 2.0.0 (2025-12-07)
- ✅ Consolidated 30+ files to 12 files (60% reduction)
- ✅ Merged frontend docs into single FRONTEND.md
- ✅ Renamed files for clarity
- ✅ Created comprehensive documentation index
- ✅ Added security documentation

---

## 📞 Need Help?

- **Issues:** [GitHub Issues](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Fahri-Hilm/Smart_Absen_Facerecognation-2025-Kelompok4/discussions)
- **Email:** Check repository for contact info

---

**Last Updated:** 2025-12-07  
**Maintained by:** Kelompok 4 - Software Project 2025
