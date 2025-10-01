#!/usr/bin/env python3
import psutil
import time
import datetime

def monitor_system():
    """Monitor system during sustained operation"""
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"[{datetime.datetime.now()}] CPU: {cpu}% | "
              f"Memory: {memory.percent}% | Disk: {disk.percent}%")
        
        time.sleep(300)  # Log every 5 minutes

if __name__ == "__main__":
    monitor_system()