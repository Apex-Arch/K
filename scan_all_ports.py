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

print(f"🔍 SCANNING ALL PORTS ON {TARGET_IP}...")
open_ports = []

# Scan first 10000 ports
with ThreadPoolExecutor(max_workers=500) as executor:
    results = executor.map(scan_port, range(1, 10001))
    open_ports = [port for port in results if port]

print(f"🎯 OPEN PORTS FOUND: {len(open_ports)}")
print(open_ports)
