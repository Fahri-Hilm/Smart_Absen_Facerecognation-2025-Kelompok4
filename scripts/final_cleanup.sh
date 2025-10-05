#!/bin/bash

echo "🧹 FINAL CLEANUP - MAKING PROJECT SUPER CLEAN"
echo "=============================================="

# Remove all __pycache__ folders
echo "🗑️  Removing Python cache files..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null

# Remove log files
echo "🗑️  Removing log files..."
find . -name "*.log" -delete 2>/dev/null

# Remove temporary files
echo "🗑️  Removing temporary files..."
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.temp" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null

# Remove DS_Store (macOS)
echo "🗑️  Removing system files..."
find . -name ".DS_Store" -delete 2>/dev/null

# Remove empty directories (except .git)
echo "🗑️  Removing empty directories..."
find . -type d -empty ! -path "./.git*" -delete 2>/dev/null

# Check for large files that shouldn't be committed
echo "📊 Checking for large files..."
find . -type f -size +10M ! -path "./.git/*" ! -path "./.venv/*" -exec ls -lh {} \; | head -5

echo ""
echo "✅ PROJECT CLEANUP COMPLETED!"
echo "🎯 Ready for professional GitHub push!"
echo ""

# Show final structure
echo "📁 FINAL PROJECT STRUCTURE:"
echo "============================"
ls -la | grep -E '^d|^-.*\.(py|md|txt|yml|yaml|json)$' | head -20