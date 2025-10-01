#!/bin/bash
# K Premium DDoS Tool - Complete Dependency Installer
# Comprehensive cross-platform installation script

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                K Premium - Complete Installer                 ║"
echo "║           Installing ALL Dependencies & Components            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
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

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Darwin)
            OS="macOS"
            PKG_MGR="brew"
            ;;
        Linux)
            if [ -f /etc/debian_version ] || [ -f /etc/debian_release ]; then
                OS="debian"
                PKG_MGR="apt"
            elif [ -f /etc/redhat-release ] || [ -f /etc/centos-release ] || [ -f /etc/fedora-release ]; then
                OS="redhat"
                PKG_MGR="dnf"
            elif [ -f /etc/arch-release ]; then
                OS="arch"
                PKG_MGR="pacman"
            elif [ -f /etc/alpine-release ]; then
                OS="alpine"
                PKG_MGR="apk"
            else
                OS="linux"
                PKG_MGR="unknown"
            fi
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            OS="windows"
            PKG_MGR="choco"
            ;;
        *)
            OS="unknown"
            PKG_MGR="unknown"
            ;;
    esac
    print_success "Detected: $OS ($(uname -s)) | Package Manager: $PKG_MGR"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install package manager if missing
install_package_manager() {
    case $PKG_MGR in
        brew)
            if ! command_exists brew; then
                print_status "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
                eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
            fi
            ;;
        choco)
            if ! command_exists choco; then
                print_warning "Chocolatey not found. Please install manually from https://chocolatey.org/"
            fi
            ;;
    esac
}

# Check if Python 3 is installed
check_python() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
        return 0
    elif command_exists python; then
        PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
        if [ $(python -c "import sys; print(sys.version_info.major)") -eq 3 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
            return 0
        fi
    fi
    
    print_error "Python 3 is not installed"
    return 1
}

# Check if pip is installed
check_pip() {
    if command_exists pip3; then
        print_success "pip3 found"
        PIP_CMD="pip3"
        return 0
    elif command_exists pip; then
        if [ $(pip --version | grep -o 'python 3') ]; then
            print_success "pip (Python 3) found"
            PIP_CMD="pip"
            return 0
        fi
    elif $PYTHON_CMD -m pip --version &> /dev/null; then
        print_success "python -m pip available"
        PIP_CMD="$PYTHON_CMD -m pip"
        return 0
    else
        print_error "pip is not installed"
        return 1
    fi
}

# Install Python if missing
install_python() {
    print_status "Installing Python 3..."
    case $PKG_MGR in
        apt)
            sudo apt update && sudo apt install -y python3 python3-pip python3-venv
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip
            ;;
        pacman)
            sudo pacman -S --noconfirm python python-pip
            ;;
        brew)
            brew install python3
            ;;
        choco)
            choco install python3 -y
            ;;
        apk)
            sudo apk add python3 py3-pip
            ;;
        *)
            print_warning "Unknown package manager. Please install Python 3 manually."
            return 1
            ;;
    esac
    
    # Refresh command detection
    check_python
    check_pip
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies for $OS..."
    
    case $OS in
        debian|ubuntu)
            sudo apt update
            sudo apt install -y \
                python3-tk \
                python3-dev \
                build-essential \
                libssl-dev \
                libffi-dev \
                libxml2-dev \
                libxslt-dev \
                libjpeg-dev \
                zlib1g-dev \
                libfreetype6-dev \
                libpng-dev \
                libblas-dev \
                liblapack-dev \
                gfortran \
                pkg-config \
                tk-dev \
                tcl-dev
            ;;
        redhat|centos|fedora)
            sudo $PKG_MGR install -y \
                python3-tkinter \
                python3-devel \
                gcc \
                gcc-c++ \
                openssl-devel \
                libffi-devel \
                libxml2-devel \
                libxslt-devel \
                libjpeg-turbo-devel \
                freetype-devel \
                zlib-devel \
                libpng-devel \
                blas-devel \
                lapack-devel \
                gcc-gfortran \
                tk-devel \
                tcl-devel
            ;;
        arch)
            sudo pacman -S --noconfirm \
                tk \
                python \
                python-pip \
                gcc \
                pkgconf \
                freetype2 \
                libjpeg-turbo \
                zlib \
                libpng \
                blas \
                lapack \
                gfortran
            ;;
        macOS)
            brew install \
                python-tk \
                freetype \
                jpeg \
                libpng \
                openblas
            ;;
        windows)
            print_info "On Windows, ensure you have Tkinter installed with your Python distribution"
            ;;
        alpine)
            sudo apk add \
                python3 \
                py3-pip \
                tk \
                tcl \
                gcc \
                musl-dev \
                python3-dev \
                libffi-dev \
                openssl-dev \
                jpeg-dev \
                zlib-dev \
                freetype-dev \
                lapack-dev \
                gfortran
            ;;
        *)
            print_warning "Unknown OS - installing common development tools"
            if command_exists apt; then
                sudo apt install -y python3 python3-pip python3-tk build-essential
            elif command_exists dnf; then
                sudo dnf install -y python3 python3-pip python3-tkinter gcc
            elif command_exists pacman; then
                sudo pacman -S --noconfirm python python-pip tk gcc
            fi
            ;;
    esac
}

# Upgrade pip and setuptools
upgrade_pip() {
    print_status "Upgrading pip and setuptools..."
    $PIP_CMD install --upgrade pip setuptools wheel
}

# Install Python packages
install_python_packages() {
    print_status "Installing Python packages..."
    
    # Core packages from the script
    CORE_PACKAGES="matplotlib aiohttp fake-useragent psutil numpy"
    
    # Additional packages that might be needed
    EXTRA_PACKAGES="asyncio threading socket random time os sys json platform concurrent.futures tkinter scrolledtext"
    
    # Packages for matplotlib backends and performance
    MATPLOTLIB_EXTRAS="pillow cycler kiwisolver pyparsing python-dateutil"
    
    # Networking and performance
    NETWORKING_PACKAGES="requests urllib3 chardet certifi idna"
    
    # Combine all packages
    ALL_PACKAGES="$CORE_PACKAGES $MATPLOTLIB_EXTRAS $NETWORKING_PACKAGES"
    
    # Install packages one by one with error handling
    for package in $ALL_PACKAGES; do
        print_status "Installing $package..."
        if $PIP_CMD install --upgrade $package; then
            print_success "Successfully installed $package"
        else
            print_warning "Failed to install $package, trying with --break-system-packages (if on Linux)..."
            $PIP_CMD install --upgrade $package --break-system-packages || true
        fi
    done
    
    # Special handling for tkinter verification
    print_status "Verifying tkinter installation..."
    if $PYTHON_CMD -c "import tkinter; print('✓ tkinter available')" 2>/dev/null; then
        print_success "tkinter is available"
    else
        print_warning "tkinter is not available as a Python package"
        print_info "tkinter is usually included with Python system packages"
    fi
}

# Install specific backend for matplotlib if needed
install_matplotlib_backend() {
    print_status "Configuring matplotlib backend..."
    
    # Try to set the backend to Agg if Tk is problematic
    $PYTHON_CMD -c "
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for installation
import matplotlib.pyplot as plt
plt.figure()
plt.close()
print('✓ matplotlib configured successfully')
" 2>/dev/null || true
}

# Create test script to verify installation
create_test_script() {
    print_status "Creating verification script..."
    
    cat > verify_k_installation.py << 'EOF'
#!/usr/bin/env python3
"""
K Premium - Installation Verification Script
Tests all required dependencies
"""

import sys
import importlib

def check_module(module_name, package_name=None):
    """Check if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name, package=package_name)
        else:
            importlib.import_module(module_name)
        print(f"✓ {module_name:20} - OK")
        return True
    except ImportError as e:
        print(f"✗ {module_name:20} - MISSING: {e}")
        return False
    except Exception as e:
        print(f"⚠ {module_name:20} - WARNING: {e}")
        return True

print("🔍 K Premium - Verifying Installation")
print("=" * 50)

# Core modules (should always be available)
core_modules = [
    'asyncio', 'threading', 'socket', 'random', 'time', 'os', 'sys', 
    'json', 'platform', 'concurrent.futures'
]

# Required external packages
external_packages = [
    'tkinter',          # GUI
    'matplotlib',       # Charts
    'aiohttp',          # Async HTTP
    'fake_useragent',   # User agents
    'psutil',           # System info
    'numpy',            # Math operations
]

# Optional but recommended
optional_packages = [
    'PIL',              # Pillow for images
    'requests',         # HTTP requests
]

print("\n📦 Core Python Modules:")
all_ok = True
for module in core_modules:
    if not check_module(module):
        all_ok = False

print("\n📦 Required External Packages:")
for package in external_packages:
    if not check_module(package):
        all_ok = False

print("\n📦 Optional Packages:")
for package in optional_packages:
    check_module(package)

print("\n" + "=" * 50)
if all_ok:
    print("🎉 SUCCESS: All required dependencies are installed!")
    print("🚀 You can now run: python3 K_DDoS.py")
else:
    print("❌ Some dependencies are missing. Please check the output above.")

# Test specific functionality
print("\n🔧 Testing Specific Functionality:")
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the window
    print("✓ Tkinter GUI functionality - OK")
    root.destroy()
except Exception as e:
    print(f"✗ Tkinter GUI functionality - FAILED: {e}")

try:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(2, 2))
    plt.plot([1, 2, 3], [1, 2, 3])
    plt.close('all')
    print("✓ Matplotlib plotting - OK")
except Exception as e:
    print(f"✗ Matplotlib plotting - FAILED: {e}")

try:
    import aiohttp
    print("✓ Aiohttp async HTTP - OK")
except Exception as e:
    print(f"✗ Aiohttp async HTTP - FAILED: {e}")

print("\n✅ Verification complete!")
EOF

    chmod +x verify_k_installation.py
}

# Run verification
verify_installation() {
    print_status "Running comprehensive verification..."
    
    if $PYTHON_CMD verify_k_installation.py; then
        print_success "🎉 K Premium installation completed successfully!"
        return 0
    else
        print_warning "Installation completed with some warnings"
        return 1
    fi
}

# Create virtual environment (optional)
create_venv() {
    if [ "$1" = "--venv" ]; then
        print_status "Creating Python virtual environment..."
        $PYTHON_CMD -m venv k_ddos_env
        print_success "Virtual environment created: k_ddos_env"
        
        if [ "$OS" = "windows" ]; then
            print_info "Activate with: k_ddos_env\\Scripts\\activate"
        else
            print_info "Activate with: source k_ddos_env/bin/activate"
        fi
        
        # Update Python and PIP commands to use venv
        if [ "$OS" = "windows" ]; then
            PYTHON_CMD="k_ddos_env\\Scripts\\python"
            PIP_CMD="k_ddos_env\\Scripts\\pip"
        else
            PYTHON_CMD="./k_ddos_env/bin/python"
            PIP_CMD="./k_ddos_env/bin/pip"
        fi
        
        # Re-install packages in venv
        upgrade_pip
        install_python_packages
    fi
}

# Clean up
cleanup() {
    if [ -f "verify_k_installation.py" ]; then
        rm -f verify_k_installation.py
    fi
}

# Main installation function
main() {
    echo ""
    print_status "Starting COMPLETE K Premium installation..."
    echo ""
    
    # Initial checks
    detect_os
    install_package_manager
    
    # Python setup
    if ! check_python; then
        install_python
    else
        check_python
    fi
    
    if ! check_pip; then
        print_error "pip is required but not installed"
        exit 1
    fi
    
    # Installation process
    install_system_deps
    upgrade_pip
    install_python_packages
    install_matplotlib_backend
    create_test_script
    
    # Handle virtual environment if requested
    if [ "$1" = "--venv" ]; then
        create_venv "$1"
    fi
    
    # Final verification
    if verify_installation; then
        echo ""
        print_success "🎉 K Premium is ready for action!"
        echo ""
        print_info "Run the tool with:"
        echo "  python3 K_DDoS.py"
        echo ""
        print_info "Or test the installation again with:"
        echo "  python3 verify_k_installation.py"
        echo ""
    else
        print_warning "Some components may need manual installation"
    fi
    
    # Legal notice
    echo ""
    print_warning "⚖️  LEGAL DISCLAIMER:"
    print_warning "   This tool is for EDUCATIONAL and AUTHORIZED TESTING purposes ONLY."
    print_warning "   Use only on systems you own or have explicit written permission to test."
    print_warning "   Unauthorized use is ILLEGAL and UNETHICAL."
    echo ""
    
    cleanup
}

# Run main function with all arguments
main "$@"
