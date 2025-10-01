#!/bin/bash
echo "⚡ INSTALLING K PREMIUM - UNIVERSAL COMPATIBILITY"

# Detect operating system
OS=$(uname -s)
echo "Detected OS: $OS"

# Install Python dependencies
pip3 install matplotlib aiohttp fake-useragent psutil

# Platform-specific dependencies
if [ "$OS" = "Linux" ]; then
    sudo apt update
    sudo apt install -y python3-tk python3-pip
    echo "✅ Linux dependencies installed"
elif [ "$OS" = "Darwin" ]; then
    # macOS - check if tkinter is available
    python3 -c "import tkinter" 2>/dev/null || echo "⚠️  Tkinter may need manual installation on macOS"
    echo "✅ macOS setup complete"
else
    echo "⚠️  Windows detected - ensure Python with Tkinter is installed"
fi

# Universal optimizations
echo "* soft nofile 50000" | sudo tee -a /etc/security/limits.conf 2>/dev/null || true
echo "* hard nofile 50000" | sudo tee -a /etc/security/limits.conf 2>/dev/null || true

echo "✅ K PREMIUM INSTALLED - UNIVERSAL COMPATIBILITY"
echo "🚀 RUN: python3 k_ddos.py"
