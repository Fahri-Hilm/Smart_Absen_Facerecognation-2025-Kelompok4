# Kafebasabasi Attendance System - UML Documentation

## Overview
This directory contains comprehensive UML diagrams for the Kafebasabasi Face Recognition Attendance System. These diagrams provide a complete visual documentation of the system's architecture, behavior, and deployment.

## Available Diagrams

### 1. Class Diagram (`class_diagram.puml`)
**Purpose**: Shows the static structure of the system including classes, attributes, methods, and relationships.

**Key Components**:
- Database layer with `DatabaseManager` and model classes
- Face recognition components (`FaceRecognitionEngine`)
- Web application structure (`AttendanceController`, `AdminController`)
- QR authentication system (`QRManager`)

**Use Cases**:
- Understanding system architecture
- Code maintenance and refactoring
- New developer onboarding

### 2. Sequence Diagram (`sequence_diagram.puml`)
**Purpose**: Illustrates the interaction flow during face recognition attendance process.

**Key Flows**:
- QR authentication workflow
- Face recognition attendance marking
- Database update process
- Camera subprocess isolation

**Use Cases**:
- Understanding system behavior
- Debugging interaction issues
- Process optimization

### 3. Activity Diagram (`activity_diagram.puml`)
**Purpose**: Shows the complete workflow of user interactions and system processes.

**Key Activities**:
- User authentication flow
- Attendance marking process (masuk/pulang)
- Admin functions workflow
- Error handling paths

**Use Cases**:
- User experience analysis
- Process documentation
- Training materials

### 4. System Architecture Diagram (`system_architecture.puml`)
**Purpose**: High-level view of system components and their relationships.

**Key Layers**:
- Web Layer (Flask, API endpoints)
- Business Logic Layer (controllers, managers)
- Data Layer (models, database)
- External Systems (MySQL, Camera, File System)

**Use Cases**:
- System overview for stakeholders
- Infrastructure planning
- Technology stack documentation

### 5. Database ERD (`database_erd.puml`)
**Purpose**: Entity Relationship Diagram showing database structure and relationships.

**Key Entities**:
- `employees` - Employee master data
- `attendance` - Daily attendance records
- `activity_log` - System activity audit trail
- `admin_users` - Administrative access
- `qr_sessions` - QR authentication sessions

**Use Cases**:
- Database design and maintenance
- Data migration planning
- Query optimization

### 6. Deployment Diagram (`deployment_diagram.puml`)
**Purpose**: Shows the physical deployment of system components.

**Key Environments**:
- Development (Devilbox containers)
- Production (Linux server deployment)
- Network infrastructure
- Client devices

**Use Cases**:
- Deployment planning
- Infrastructure setup
- Security configuration

## How to View the Diagrams

### Option 1: PlantUML Online Server
1. Go to [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
2. Copy the content from any `.puml` file
3. Paste it into the online editor
4. View the generated diagram

### Option 2: VS Code Extension
1. Install "PlantUML" extension in VS Code
2. Open any `.puml` file
3. Press `Alt+D` or use Command Palette: "PlantUML: Preview Current Diagram"

### Option 3: Local PlantUML Installation
```bash
# Install Java (required for PlantUML)
sudo apt update
sudo apt install default-jre

# Download PlantUML
wget http://sourceforge.net/projects/plantuml/files/plantuml.jar/download -O plantuml.jar

# Generate PNG from PUML file
java -jar plantuml.jar class_diagram.puml
```

### Option 4: Docker PlantUML
```bash
# Generate all diagrams using Docker
docker run --rm -v $(pwd):/work plantuml/plantuml:latest -tpng /work/*.puml
```

## Diagram Relationships

```
System Architecture
       │
       ├── Class Diagram (static structure)
       ├── Sequence Diagram (interaction flow)
       ├── Activity Diagram (process flow)
       ├── Database ERD (data structure)
       └── Deployment Diagram (physical architecture)
```

## Maintenance Guidelines

### When to Update Diagrams
- Adding new features or components
- Modifying database schema
- Changing system architecture
- Deployment environment changes
- Major refactoring

### Diagram Versioning
- Keep diagrams in sync with code changes
- Use git for version control
- Document major changes in commit messages
- Review diagrams during code reviews

### Naming Conventions
- Use descriptive file names with `_diagram.puml` suffix
- Follow consistent naming in diagram elements
- Use clear, readable labels and descriptions
- Maintain consistent styling across diagrams

## Integration with Development Workflow

### Code Reviews
Include relevant diagrams in pull requests when:
- Architecture changes are proposed
- New components are added
- Database schema modifications
- API endpoint changes

### Documentation Updates
Update diagrams when:
- README files are modified
- API documentation changes
- Deployment guides are updated
- User manuals are revised

### Testing
Validate diagrams by:
- Ensuring they compile without errors
- Checking diagram readability
- Verifying accuracy against actual code
- Getting feedback from team members

## Export Formats

PlantUML supports multiple output formats:
- **PNG**: Best for documentation and presentations
- **SVG**: Scalable vector graphics for web
- **PDF**: Professional documentation
- **ASCII**: Text-based for terminal viewing

Example export commands:
```bash
# PNG format
java -jar plantuml.jar -tpng *.puml

# SVG format
java -jar plantuml.jar -tsvg *.puml

# PDF format
java -jar plantuml.jar -tpdf *.puml
```

## Best Practices

### Diagram Design
1. **Keep it Simple**: Avoid overcrowding diagrams
2. **Use Colors Wisely**: Consistent color coding for component types
3. **Clear Labels**: Descriptive names for all elements
4. **Proper Grouping**: Logical organization of components
5. **Consistent Style**: Use same theme across all diagrams

### Documentation
1. **Add Notes**: Explain complex relationships or processes
2. **Include Legends**: Define symbols and colors used
3. **Version Information**: Include creation and update dates
4. **Context**: Explain when and why to use each diagram

### Collaboration
1. **Team Reviews**: Get feedback on diagram accuracy
2. **Stakeholder Input**: Include non-technical stakeholders in reviews
3. **Regular Updates**: Schedule periodic diagram maintenance
4. **Training**: Ensure team knows how to read and update diagrams

## Troubleshooting

### Common Issues
1. **Syntax Errors**: Check PlantUML syntax carefully
2. **Missing Dependencies**: Ensure Java is installed for local generation
3. **Large Diagrams**: Break complex diagrams into smaller, focused ones
4. **Rendering Issues**: Try different output formats if one fails

### Performance Tips
1. Use `!theme` directive for consistent styling
2. Minimize the number of elements in single diagram
3. Use `!include` for shared components
4. Consider splitting large diagrams into multiple files

## Related Documentation
- [API Documentation](API_DOCUMENTATION.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Database Documentation](README_DATABASE.md)
- [System Implementation](IMPLEMENTASI_LENGKAP.md)