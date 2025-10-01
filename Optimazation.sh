#!/bin/bash
echo "💀 OPTIMIZING SYSTEM FOR ABSOLUTE DESTRUCTION"

# Maximum system limits
echo "* soft nofile 1000000" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 1000000" | sudo tee -a /etc/security/limits.conf
echo "* soft nproc 1000000" | sudo tee -a /etc/security/limits.conf
echo "* hard nproc 1000000" | sudo tee -a /etc/security/limits.conf

# Nuclear network settings
echo "net.core.somaxconn = 1000000" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_max_syn_backlog = 1000000" | sudo tee -a /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 1000000" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.ip_local_port_range = 1024 65535" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_tw_reuse = 1" | sudo tee -a /etc/sysctl.conf

# Disable all protections
echo "net.ipv4.tcp_syncookies = 0" | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p
ulimit -n 1000000

echo "✅ SYSTEM OPTIMIZED FOR ABSOLUTE DESTRUCTION"
