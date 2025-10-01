#!/bin/bash
echo "⚡ INSTALLING K DDoS TOOL..."

# Install Python dependencies
pip3 install matplotlib aiohttp fake-useragent psutil

# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y python3-tk python3-pip

# Increase system limits
echo "* soft nofile 100000" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 100000" | sudo tee -a /etc/security/limits.conf

echo "✅ Storm Breaker Installation Complete!"
echo "🚀 Run: python3 K.py"