#!/usr/bin/env python3
import requests
import time

TARGET_IP = "116.202.161.203"
TARGET_DOMAIN = "sp123.edu.pl"

def test_website():
    try:
        # Test via domain (through CDN)
        start = time.time()
        r1 = requests.get(f"https://{TARGET_DOMAIN}", timeout=5)
        domain_time = time.time() - start
        
        # Test via direct IP (bypass CDN)
        start = time.time()
        headers = {'Host': TARGET_DOMAIN}
        r2 = requests.get(f"http://{TARGET_IP}/", headers=headers, timeout=5)
        ip_time = time.time() - start
        
        print(f"🌐 VIA DOMAIN: {domain_time:.2f}s - Status: {r1.status_code}")
        print(f"🎯 VIA DIRECT IP: {ip_time:.2f}s - Status: {r2.status_code}")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")

test_website()
