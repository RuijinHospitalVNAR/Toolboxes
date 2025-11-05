#!/bin/bash
# -*- coding: utf-8 -*-
# Quick Start Script for VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles

echo "=========================================="
echo "VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles"
echo "Quick Start Guide"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if required files exist
if [ ! -f "src/vlpim/vlpim.py" ]; then
    echo "❌ Main pipeline script not found. Please run this from the project directory."
    exit 1
fi

echo "✅ Pipeline script found"

# Create example input if it doesn't exist
if [ ! -f "input/example.fasta" ]; then
    echo "📁 Creating example input files..."
    mkdir -p input
    cat > input/example.fasta << EOF
>example_protein
MKLLVLGCTAGCTTTCCGGA
EOF
    echo "✅ Example FASTA file created"
fi

# Show available commands
echo ""
echo "🚀 Quick Start Commands:"
echo ""
echo "1. Install dependencies:"
echo "   make install"
echo ""
echo "2. Run setup:"
echo "   make setup"
echo ""
echo "3. Test installation:"
echo "   make test"
echo ""
echo "4. Run with example data:"
echo "   make run-example"
echo ""
echo "5. Show help:"
echo "   python3 immunogenicity_optimization_pipeline.py --help"
echo ""
echo "📖 For detailed instructions, see:"
echo "   - README.md (usage guide)"
echo "   - INSTALL.md (installation guide)"
echo ""
echo "🔧 For troubleshooting:"
echo "   - Check INSTALL.md for common issues"
echo "   - Run with --log-level DEBUG for verbose output"
echo ""
