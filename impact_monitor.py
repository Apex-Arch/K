#!/usr/bin/env python3
import requests
import time
import datetime

TARGET = "https://sp123.edu.pl"

def monitor_impact():
    print("📊 MONITORING ATTACK IMPACT IN REAL-TIME...")
    
    while True:
        try:
            start = time.time()
            r = requests.get(TARGET, timeout=10, verify=False)
            response_time = time.time() - start
            status = r.status_code
            
            if response_time > 5:
                impact = "🔥 HEAVY IMPACT"
            elif response_time > 2:
                impact = "🔴 MODERATE IMPACT"
            else:
                impact = "🟢 MINIMAL IMPACT"
                
            print(f"[{datetime.datetime.now()}] {impact} - Response: {response_time:.2f}s - Status: {status}")
            
        except Exception as e:
            print(f"[{datetime.datetime.now()}] 💀 TARGET OFFLINE - {e}")
        
        time.sleep(10)

monitor_impact()
