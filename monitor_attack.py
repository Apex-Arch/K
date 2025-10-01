#!/usr/bin/env python3
import requests
import time

TARGET_IP = "116.202.161.203"
TARGET_DOMAIN = "sp123.edu.pl"

def monitor_target():
    print("📊 MONITORING TARGET AVAILABILITY...")
    
    while True:
        try:
            # Test HTTP
            start = time.time()
            r = requests.get(f"http://{TARGET_IP}/", headers={'Host': TARGET_DOMAIN}, timeout=5)
            http_time = time.time() - start
            http_status = r.status_code
        except:
            http_time = "TIMEOUT"
            http_status = "FAILED"
        
        try:
            # Test HTTPS
            start = time.time()
            r = requests.get(f"https://{TARGET_DOMAIN}", timeout=5)
            https_time = time.time() - start
            https_status = r.status_code
        except:
            https_time = "TIMEOUT"
            https_status = "FAILED"
        
        print(f"🌐 HTTP: {http_status} ({http_time}) | HTTPS: {https_status} ({https_time})")
        time.sleep(10)

monitor_target()
