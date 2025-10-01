#!/bin/bash
echo "🔧 OPTIMIZING SYSTEM FOR 48-HOUR SUSTAINED OPERATION"

# Increase system limits
echo "* soft nofile 100000" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 100000" | sudo tee -a /etc/security/limits.conf
echo "* soft nproc 100000" | sudo tee -a /etc/security/limits.conf
echo "* hard nproc 100000" | sudo tee -a /etc/security/limits.conf

# Network optimization
echo "net.core.somaxconn = 100000" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 100000" | sudo tee -a /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 100000" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_rmem = 4096 87380 16777216" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_wmem = 4096 87380 16777216" | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p
ulimit -n 100000

echo "✅ SYSTEM OPTIMIZED FOR SUSTAINED OPERATION"