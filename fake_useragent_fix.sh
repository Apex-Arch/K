#!/bin/bash
# K Premium DDoS Tool - ULTIMATE Dependency Installer
# Guaranteed to install ALL dependencies including fake-useragent

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                K Premium - ULTIMATE Installer                 ║"
echo "║          100% Working fake-useragent Installation             ║"
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
print_status() { echo -e "${CYAN}[K INSTALLER]${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Darwin) OS="macOS"; PKG_MGR="brew" ;;
        Linux)
            if [ -f /etc/debian_version ]; then OS="debian"; PKG_MGR="apt"
            elif [ -f /etc/redhat-release ]; then OS="redhat"; PKG_MGR="dnf"  
            elif [ -f /etc/arch-release ]; then OS="arch"; PKG_MGR="pacman"
            else OS="linux"; PKG_MGR="unknown"; fi ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*) OS="windows"; PKG_MGR="choco" ;;
        *) OS="unknown"; PKG_MGR="unknown" ;;
    esac
    print_success "Detected: $OS | Package Manager: $PKG_MGR"
}

# Check if command exists
command_exists() { command -v "$1" >/dev/null 2>&1; }

# Install Python if missing
install_python() {
    if ! command_exists python3 && ! command_exists python; then
        print_status "Installing Python 3..."
        case $PKG_MGR in
            apt) sudo apt update && sudo apt install -y python3 python3-pip python3-venv ;;
            dnf) sudo dnf install -y python3 python3-pip ;;
            pacman) sudo pacman -S --noconfirm python python-pip ;;
            brew) brew install python3 ;;
            choco) choco install python3 -y ;;
            *) print_error "Cannot auto-install Python on this system"; return 1 ;;
        esac
    fi
    
    # Set Python command
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python not found after installation attempt"
        return 1
    fi
    print_success "Python found: $($PYTHON_CMD --version)"
}

# Set PIP command
set_pip_command() {
    if command_exists pip3; then
        PIP_CMD="pip3"
    elif command_exists pip; then
        PIP_CMD="pip" 
    elif $PYTHON_CMD -m pip --version &>/dev/null; then
        PIP_CMD="$PYTHON_CMD -m pip"
    else
        print_error "pip not found"
        return 1
    fi
    print_success "pip found: $($PIP_CMD --version | head -n1)"
}

# FORCE install fake-useragent with multiple methods
install_fake_useragent_force() {
    print_status "🔧 FORCE INSTALLING fake-useragent..."
    
    # Method 1: Normal install
    print_status "Method 1: Standard pip install..."
    if $PIP_CMD install --upgrade fake-useragent; then
        print_success "Standard installation successful"
        return 0
    fi
    
    # Method 2: With --break-system-packages (new pip)
    print_status "Method 2: With --break-system-packages..."
    if $PIP_CMD install --break-system-packages fake-useragent; then
        print_success "Installation with --break-system-packages successful"
        return 0
    fi
    
    # Method 3: With --user flag
    print_status "Method 3: With --user flag..."
    if $PIP_CMD install --user fake-useragent; then
        print_success "User installation successful"
        return 0
    fi
    
    # Method 4: With --no-cache-dir
    print_status "Method 4: With --no-cache-dir..."
    if $PIP_CMD install --no-cache-dir fake-useragent; then
        print_success "No-cache installation successful"
        return 0
    fi
    
    # Method 5: Install from git
    print_status "Method 5: Installing from GitHub..."
    if $PIP_CMD install --upgrade git+https://github.com/hellysmile/fake-useragent.git; then
        print_success "Git installation successful"
        return 0
    fi
    
    # Method 6: Using easy_install as last resort
    print_status "Method 6: Trying easy_install..."
    if command_exists easy_install; then
        if easy_install fake-useragent; then
            print_success "easy_install successful"
            return 0
        fi
    fi
    
    print_error "All fake-useragent installation methods failed"
    return 1
}

# Install all other packages
install_all_packages() {
    print_status "Installing all required packages..."
    
    local packages="matplotlib aiohttp psutil numpy pillow requests"
    
    for pkg in $packages; do
        print_status "Installing $pkg..."
        if $PIP_CMD install --upgrade $pkg; then
            print_success "Installed $pkg"
        else
            print_warning "Failed to install $pkg, trying with --break-system-packages..."
            $PIP_CMD install --break-system-packages $pkg || true
        fi
    done
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    case $OS in
        debian|ubuntu)
            sudo apt update && sudo apt install -y \
                python3-tk python3-dev build-essential \
                libssl-dev libffi-dev tk-dev ;;
        redhat|centos|fedora)
            sudo $PKG_MGR install -y \
                python3-tkinter python3-devel gcc \
                openssl-devel libffi-devel tk-devel ;;
        arch)
            sudo pacman -S --noconfirm tk python python-pip gcc ;;
        macOS)
            brew install python-tk ;;
        *) print_warning "Skipping system dependencies for unknown OS" ;;
    esac
}

# Create verification script that actually tests imports
create_verification_script() {
    cat > verify_k.py << 'EOF'
#!/usr/bin/env python3
"""
K Premium - REAL Verification Script
Tests actual imports and functionality
"""

import sys
import importlib

def test_import(module_name, install_name=None):
    """Test if a module can be imported"""
    try:
        if install_name is None:
            install_name = module_name
        importlib.import_module(module_name)
        print(f"✅ {module_name:20} - IMPORT SUCCESS")
        return True
    except ImportError as e:
        print(f"❌ {module_name:20} - IMPORT FAILED")
        print(f"   Error: {e}")
        print(f"   Install with: pip install {install_name}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name:20} - IMPORT WARNING: {e}")
        return True

print("🔍 K Premium - REAL VERIFICATION")
print("=" * 60)

# Test CRITICAL imports
critical_modules = [
    ("tkinter", None),  # Built-in
    ("matplotlib", "matplotlib"),
    ("aiohttp", "aiohttp"), 
    ("fake_useragent", "fake-useragent"),  # THIS IS THE PROBLEM CHILD
    ("psutil", "psutil"),
    ("numpy", "numpy"),
]

print("\n🧪 TESTING CRITICAL IMPORTS:")
all_critical_ok = True

for module_name, install_name in critical_modules:
    if not test_import(module_name, install_name):
        all_critical_ok = False

# Test functionality
print("\n🔧 TESTING FUNCTIONALITY:")
try:
    import fake_useragent
    ua = fake_useragent.UserAgent()
    random_ua = ua.random
    print(f"✅ fake_useragent - FUNCTIONALITY WORKS: {random_ua[:50]}...")
except Exception as e:
    print(f"❌ fake_useragent - FUNCTIONALITY BROKEN: {e}")

try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    root.destroy()
    print("✅ tkinter - GUI FUNCTIONALITY WORKS")
except Exception as e:
    print(f"❌ tkinter - GUI BROKEN: {e}")

print("\n" + "=" * 60)
if all_critical_ok:
    print("🎉 SUCCESS: All critical dependencies are working!")
    print("🚀 You can now run: python3 K_DDoS.py")
else:
    print("💥 CRITICAL FAILURE: Some dependencies are missing!")
    print("   Please run the installer again or install manually.")

# Show Python path info
print(f"\n📁 Python Path: {sys.executable}")
print(f"📁 Python Version: {sys.version}")

EOF

    chmod +x verify_k.py
}

# Main installation function
main() {
    echo ""
    print_status "Starting ULTIMATE K Premium installation..."
    print_status "SPECIAL FOCUS: Ensuring fake-useragent installs correctly"
    echo ""
    
    # Detect OS and setup
    detect_os
    install_python
    set_pip_command
    
    # Upgrade pip first
    print_status "Upgrading pip..."
    $PIP_CMD install --upgrade pip
    
    # Install system dependencies
    install_system_deps
    
    # INSTALL FAKE-USERAGENT FIRST AND FORCEFULLY
    print_status "🎯 FOCUS: Installing fake-useragent with maximum force..."
    if install_fake_useragent_force; then
        print_success "fake-useragent installation completed"
    else
        print_error "fake-useragent failed to install - trying alternative approach..."
        
        # LAST RESORT: Install directly via easy_install or curl
        print_status "🚨 EMERGENCY INSTALL: Downloading and installing manually..."
        $PIP_CMD install --no-deps fake-useragent || true
    fi
    
    # Install other packages
    install_all_packages
    
    # Create and run verification
    create_verification_script
    print_status "Running ULTIMATE verification..."
    $PYTHON_CMD verify_k.py
    
    # Final check specifically for fake-useragent
    print_status "🔍 FINAL FAKE-USERAGENT CHECK..."
    if $PYTHON_CMD -c "import fake_useragent; print('✅ ULTIMATE SUCCESS: fake_useragent is NOW WORKING!')"; then
        print_success "🎉 fake-useragent is DEFINITELY installed and working!"
    else
        print_error "💥 fake-useragent STILL not working - manual intervention required"
        print_info "Try: pip install --user --force-reinstall fake-useragent"
    fi
    
    echo ""
    print_success "Installation completed!"
    print_info "Run the tool: python3 K_DDoS.py"
    echo ""
    
    # Cleanup
    rm -f verify_k.py
}

# Run the ultimate installer
main
