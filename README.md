# 🏔️ K2 RAT - Advanced Persistent Threat Simulation
### PITP Cybersecurity Project 2026

---

## 👥 Team Members
- **Syed Muhammad Junaid Sarwar**
- **Syed Shafay Ahmed Zaidi**
- **Muhammad Shahood**
- **Muhammad Masroor**

---

## 📋 Project Overview
K2 RAT is a complete **Command & Control (C2) infrastructure** demonstrating the full Cyber Kill Chain:
- ✅ Multi-stage attack simulation
- ✅ Custom C2 server with real-time command execution
- ✅ Windows persistence (Registry + Startup Folder)
- ✅ Ransomware simulation (XOR encryption)
- ✅ System crash methods (BSOD, memory exhaustion, disk fill)
- ✅ UAC bypass (admin on first run only)

---

## 📁 Files Included
| File | Description |
|------|-------------|
| `client.py` | Windows payload (compile with PyInstaller) |
| `c2_server.py` | Command & Control server (run on Kali) |
| `exploit_server.py` | Fake download page for social engineering |
| `requirements.txt` | Python dependencies |

---

## 🛠️ Requirements

### Windows Host (for compiling payload)
```bash
# Install Python 3.8+ from python.org
# Then install dependencies:
pip install pyinstaller pynput pywin32
```

### Kali Linux (for C2 & Exploit servers)
```bash
# Python 3 is pre-installed
# No additional packages needed
```

---

## 🚀 Setup Instructions

### Step 1: Windows Host - Compile Payload (CMD)
```cmd
# Navigate to your project folder (adjust path as needed)
cd C:\Users\YourUsername\NED_Project
pip install pyinstaller
pyinstaller --onefile --noconsole --uac-admin client.py
cd dist
ren client.exe payload.exe
python -m http.server 8000
```
**Keep this terminal open - HTTP server is running!**

---

### Step 2: Kali VM - Create Project Folder & Download Payload
```bash
# Create project folder
mkdir ~/K2_RAT
cd ~/K2_RAT

# Windows Host IP is usually 192.168.56.1
# Download the compiled payload
wget http://192.168.56.1:8000/payload.exe -O client.exe
```

---

### Step 3: Kali VM - Terminal 1 (C2 Server)
```bash
cd ~/K2_RAT
nano c2_server.py
# COPY AND PASTE THE C2 SERVER CODE
# Ctrl + O -> Enter -> Ctrl + X (to save)

# Run C2 server
python3 c2_server.py
```

---

### Step 4: Kali VM - Terminal 2 (Exploit Server)
```bash
cd ~/K2_RAT
nano exploit_server.py
# COPY AND PASTE THE EXPLOIT SERVER CODE
# Ctrl + O -> Enter -> Ctrl + X (to save)

# Run Exploit server
python3 exploit_server.py
```

---

### Step 5: Windows VM - Victim
```
1. Find Kali's IP address:
   ip a | grep 192.168   (in Kali terminal)

2. Open browser in Windows VM:
   http://<KALI_IP>:8080/   (e.g., http://192.168.56.102:8080/)

3. Download "k2_rat_educational.exe"

4. Run the file (click "Yes" on UAC prompt)

5. C2 server will show connection: 
   "✅ New target: WIN_19216856103 - 192.168.56.103"
```

---

## 💻 Available Commands

| Command | Description |
|---------|-------------|
| `sysinfo` | Display system information |
| `install` | Install persistence (Registry + Startup) |
| `ransomware` | Encrypt folders with 'secret' in name |
| `ransomware <path>` | Encrypt specific folder |
| `decrypt` | Decrypt last encrypted folder |
| `decrypt <path>` | Decrypt specific folder |
| `kill forkbomb` | Crash with infinite processes |
| `kill memory` | Crash with memory exhaustion |
| `kill disk` | Crash by filling disk |
| `kill bsod` | Cause Blue Screen of Death |
| `whoami` | Show current user |
| `cd <path>` | Change directory |
| `dir` / `ipconfig` / any Windows command | Execute system commands |

---

## 🔧 Features Demonstrated

| Vulnerability | MITRE ATT&CK | Description |
|---------------|--------------|-------------|
| **UAC Bypass** | T1548.002 | Admin elevation on first run only |
| **Persistence** | T1547.001 | Registry Run keys + Startup folder |
| **Ransomware** | T1486 | XOR encryption of 'secret' folders |
| **System Crash** | T1499 | Fork bomb, memory/disk exhaustion |
| **Privilege Escalation** | T1068 | User addition via `net user` |
| **Defense Evasion** | T1564.001 | Hidden files, process masquerading |

---

## ⚠️ Important Notes
- **Windows Defender** must be disabled in victim VM
- Use only in **isolated lab environment**
- **Educational purposes only**
- Take VM snapshot before testing kill commands
- Windows Host IP is usually `192.168.56.1` (verify with `ipconfig`)
- Kali IP will vary - use `ip a` to find yours

---

## 📦 Requirements.txt
```txt
pyinstaller
pynput
pywin32
```

---

## 📝 License
This project is for **educational purposes only**. Unauthorized use against real systems is prohibited.

---

## 🙏 Acknowledgements
- PITP NED University Cybersecurity Course
- Submitted to Miss Zainab Kamal

---

## 🔗 GitHub Repository
```
https://github.com/junaid-sarwar/PITP-PROJECT-K2_RAT
```
