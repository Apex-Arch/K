#!/usr/bin/env python3
import psutil
import time

def monitor_system():
    print("📊 LIVE SYSTEM PERFORMANCE MONITOR")
    
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()
        
        print(f"🔥 CPU: {cpu}% | 💾 Memory: {memory.percent}% | 📨 Packets: {network.packets_sent}")
        time.sleep(2)

if __name__ == "__main__":
    monitor_system()
