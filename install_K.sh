#!/bin/bash
# K Premium DDoS Tool - Dependency Installer
# Cross-platform dependency installation script

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   K Premium DDoS Tool                         ║"
echo "║              Dependency Installation Script                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${CYAN}[K INSTALLER]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Darwin)
            OS="macOS"
            ;;
        Linux)
            if [ -f /etc/debian_version ]; then
                OS="debian"
            elif [ -f /etc/redhat-release ]; then
                OS="redhat"
            elif [ -f /etc/arch-release ]; then
                OS="arch"
            else
                OS="linux"
            fi
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            OS="windows"
            ;;
        *)
            OS="unknown"
            ;;
    esac
    print_status "Detected operating system: $OS"
}

# Check if Python 3 is installed
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
        print_success "Python $PYTHON_VERSION found"
        return 0
    else
        print_error "Python 3 is not installed"
        return 1
    fi
}

# Check if pip is installed
check_pip() {
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        return 0
    elif python3 -m pip --version &> /dev/null; then
        print_success "python3 -m pip available"
        return 0
    else
        print_error "pip3 is not installed"
        return 1
    fi
}

# Install system dependencies for different OS
install_system_deps() {
    print_status "Installing system dependencies..."
    
    case $OS in
        debian|ubuntu)
            sudo apt update
            sudo apt install -y python3-tk python3-dev build-essential libssl-dev libffi-dev
            ;;
        redhat|centos|fedora)
            sudo dnf install -y python3-tkinter python3-devel gcc openssl-devel
            ;;
        arch)
            sudo pacman -S --noconfirm tk python python-pip gcc
            ;;
        macOS)
            if ! command -v brew &> /dev/null; then
                print_warning "Homebrew not found. Please install Homebrew first:"
                echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                return 1
            fi
            brew install python-tk
            ;;
        windows)
            print_warning "On Windows, ensure you have Tkinter installed with your Python distribution"
            ;;
        *)
            print_warning "Unknown OS - please install Tkinter manually"
            ;;
    esac
}

# Install Python packages
install_python_packages() {
    print_status "Installing Python packages..."
    
    # Base packages
    PIP_PACKAGES="matplotlib aiohttp fake-useragent psutil numpy"
    
    # Try different pip commands
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif python3 -m pip &> /dev/null; then
        PIP_CMD="python3 -m pip"
    else
        print_error "No pip command found"
        return 1
    fi
    
    # Install packages
    for package in $PIP_PACKAGES; do
        print_status "Installing $package..."
        $PIP_CMD install --upgrade $package
    done
    
    # Special handling for tkinter (usually comes with Python)
    print_status "Verifying tkinter installation..."
    if python3 -c "import tkinter" &> /dev/null; then
        print_success "tkinter is available"
    else
        print_error "tkinter is not available"
        print_warning "Please install tkinter using your system package manager"
        case $OS in
            debian|ubuntu)
                echo "Run: sudo apt install python3-tk"
                ;;
            redhat|centos|fedora)
                echo "Run: sudo dnf install python3-tkinter"
                ;;
            macOS)
                echo "Run: brew install python-tk"
                ;;
            *)
                echo "Please install tkinter for your system"
                ;;
        esac
    fi
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    python3 - << 'EOF'
try:
    import tkinter
    import matplotlib
    import aiohttp
    from fake_useragent import UserAgent
    import psutil
    import numpy as np
    print("✓ All dependencies installed successfully!")
    print("✓ K Premium DDoS Tool is ready to use!")
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    exit(1)
EOF
    
    if [ $? -eq 0 ]; then
        print_success "Verification completed successfully!"
        return 0
    else
        print_error "Verification failed"
        return 1
    fi
}

# Create virtual environment (optional)
create_venv() {
    read -p "Do you want to create a Python virtual environment? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Creating virtual environment..."
        python3 -m venv k_ddos_env
        print_success "Virtual environment created: k_ddos_env"
        print_warning "Activate with: source k_ddos_env/bin/activate (Linux/macOS) or k_ddos_env\\Scripts\\activate (Windows)"
    fi
}

# Main installation function
main() {
    echo ""
    print_status "Starting K Premium DDoS Tool dependency installation..."
    echo ""
    
    # Detect OS
    detect_os
    
    # Check Python
    if ! check_python; then
        print_error "Please install Python 3.7 or higher first"
        exit 1
    fi
    
    # Check pip
    if ! check_pip; then
        print_error "Please install pip3 first"
        exit 1
    fi
    
    # Install system dependencies
    install_system_deps
    
    # Install Python packages
    install_python_packages
    
    # Verify installation
    if verify_installation; then
        echo ""
        print_success "🎉 K Premium DDoS Tool dependencies installed successfully!"
        echo ""
        print_status "You can now run the tool with:"
        echo "  sudo python3 K.py"
        echo ""
        
        # Offer to create virtual environment
        create_venv
        
        echo ""
        print_warning "⚠️  LEGAL DISCLAIMER: Use this tool only on systems you own or have explicit permission to test."
        print_warning "   Unauthorized use is illegal and unethical."
        echo ""
    else
        print_error "Installation failed. Please check the errors above."
        exit 1
    fi
}

# Run main function
main "$@"
