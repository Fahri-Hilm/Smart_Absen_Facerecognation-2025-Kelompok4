#!/bin/bash

# Setup Documentation for Smart Absen
# Run this script to install and setup all documentation tools

echo "📚 Setting up Smart Absen Documentation..."
echo ""

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not active!"
    echo "Please activate it first:"
    echo "  source .venv/bin/activate"
    exit 1
fi

# Install Swagger dependencies
echo "📦 Installing Swagger UI dependencies..."
pip install -r requirements_swagger.txt

# Copy OpenAPI spec to static folder
echo "📄 Copying OpenAPI specification..."
cp docs/openapi.yaml static/openapi.yaml

# Create docs directory if not exists
mkdir -p docs

echo ""
echo "✅ Documentation setup complete!"
echo ""
echo "📖 Available documentation:"
echo "  - Swagger UI: http://localhost:5001/api/docs"
echo "  - Architecture: docs/ARCHITECTURE.md"
echo "  - Docstring Guide: docs/DOCSTRING_GUIDE.md"
echo "  - Draw.io Diagram: docs/architecture_diagram.drawio"
echo ""
echo "🚀 Start the app with: python app.py"
echo "   Then visit: http://localhost:5001/api/docs"
