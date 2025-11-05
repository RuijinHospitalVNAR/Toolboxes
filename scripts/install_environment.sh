#!/bin/bash
# -*- coding: utf-8 -*-
# VLPIM: A Comprehensive Tool for Immunogenicity Modulation of Virus-like Particles - Setup Script
# This script sets up the environment and installs dependencies

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_status "Found Python $PYTHON_VERSION"
        
        # Check if version is >= 3.8
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
            print_success "Python version is compatible (>= 3.8)"
        else
            print_error "Python version must be >= 3.8. Found: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        print_success "Python dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Function to check for external tools
check_external_tools() {
    print_status "Checking for external tools..."
    
    local missing_tools=()
    
    # Check for ProteinMPNN
    if ! command_exists protein_mpnn; then
        missing_tools+=("ProteinMPNN")
    fi
    
    # Check for NetMHCIIpan
    if ! command_exists netMHCIIpan; then
        missing_tools+=("NetMHCIIpan")
    fi
    
    # Check for AlphaFold3
    if ! command_exists alphafold3; then
        missing_tools+=("AlphaFold3")
    fi
    
    # Check for Rosetta interface_analyzer
    if ! command_exists interface_analyzer; then
        missing_tools+=("Rosetta interface_analyzer")
    fi
    
    if [ ${#missing_tools[@]} -eq 0 ]; then
        print_success "All external tools are available"
    else
        print_warning "The following external tools are missing:"
        for tool in "${missing_tools[@]}"; do
            echo "  - $tool"
        done
        echo ""
        print_warning "Please install these tools manually. See INSTALL.md for detailed instructions."
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p results
    mkdir -p input
    mkdir -p logs
    mkdir -p tools/external
    
    print_success "Directories created successfully"
}

# Function to set up environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Immunogenicity Optimization Pipeline Environment Variables

# External tool paths (update these to match your installation)
export PROTEIN_MPNN_PATH=""
export NETMHCIIPAN_PATH=""
export ALPHAFOLD3_PATH=""
export ROSETTA_PATH=""

# API keys (if needed)
export IEDB_API_KEY=""

# Default parameters
export DEFAULT_OUTPUT_DIR="results"
export DEFAULT_LOG_LEVEL="INFO"
EOF
        print_success "Created .env file with default environment variables"
        print_warning "Please update .env file with your actual tool paths"
    else
        print_status ".env file already exists"
    fi
}

# Function to run tests
run_tests() {
    print_status "Running basic tests..."
    
    if python3 -c "import pandas, numpy, requests" 2>/dev/null; then
        print_success "Basic Python imports successful"
    else
        print_error "Basic Python imports failed"
        exit 1
    fi
    
    # Test pipeline import
    if python3 -c "from immunogenicity_optimization_pipeline import ImmunogenicityOptimizer" 2>/dev/null; then
        print_success "Pipeline import successful"
    else
        print_error "Pipeline import failed"
        exit 1
    fi
}

# Function to display installation summary
display_summary() {
    echo ""
    echo "=========================================="
    print_success "Installation completed successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Update .env file with your external tool paths"
    echo "2. Install missing external tools (see INSTALL.md)"
    echo "3. Test the pipeline with: python3 immunogenicity_optimization_pipeline.py --help"
    echo ""
    echo "For detailed usage instructions, see README.md"
    echo "For troubleshooting, see INSTALL.md"
    echo ""
}

# Main installation function
main() {
    echo "=========================================="
    echo "Immunogenicity Optimization Pipeline Setup"
    echo "=========================================="
    echo ""
    
    # Check Python
    check_python
    
    # Install Python dependencies
    install_python_deps
    
    # Create directories
    create_directories
    
    # Setup environment
    setup_environment
    
    # Check external tools
    check_external_tools
    
    # Run tests
    run_tests
    
    # Display summary
    display_summary
}

# Run main function
main "$@"
