#!/usr/bin/env python3
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

TARGET_IP = "116.202.161.203"

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((TARGET_IP, port))
        sock.close()
        if result == 0:
            print(f"✅ PORT {port} - OPEN")
            return port
    except:
        pass
    return None

# Scan common web ports
common_ports = [80, 443, 8080, 8443, 3000, 5000, 8000, 8081, 8888, 9090, 22, 21, 25, 53, 110, 143, 993, 995, 3306, 5432, 27017, 6379]

print(f"🔍 SCANNING {TARGET_IP} FOR OPEN PORTS...")
with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(scan_port, common_ports)

open_ports = [port for port in results if port]
print(f"🎯 OPEN PORTS FOUND: {open_ports}")
