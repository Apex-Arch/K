#!/bin/bash
echo "⚡ INSTALLING K - PREMIUM ASSAULT SYSTEM..."

# Install Python dependencies
pip3 install matplotlib aiohttp fake-useragent psutil

# Install system dependencies
sudo apt update
sudo apt install -y python3-tk python3-pip

# Increase system limits for premium performance
echo "* soft nofile 100000" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 100000" | sudo tee -a /etc/security/limits.conf

# Optimize network stack
echo "net.core.somaxconn = 100000" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 100000" | sudo tee -a /etc/sysctl.conf

sudo sysctl -p

echo "✅ K PREMIUM SYSTEM INSTALLED"
echo "🚀 RUN: python3 k_ddos.py"
