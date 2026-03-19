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

### Step 1: Windows Host - Compile Payload
```cmd
cd C:\Users\junai\NED_Project
pip install pyinstaller
pyinstaller --onefile --noconsole --uac-admin client.py
cd dist
ren client.exe payload.exe
python -m http.server 8000
```

### Step 2: Kali VM - C2 Server (1 TERMINAL)
```bash
mkdir NED_Project
cd ~/NED_Project
nano c2_server.py
--COPY AND PASTE THE C2 SERVER CODE ---
Ctrl + O -> Enter -> Ctrl + X (TO SAVE)
python3 c2_server.py
```

### Step 3: Kali VM - Exploit Server (2nd TERMINAL)
```bash
cd ~/NED_Project
nano exploit_server.py
--COPY AND PASTE THE EXPLOIT SERVER CODE ---
Ctrl + O -> Enter -> Ctrl + X (TO SAVE)
python3 exploit_server.py
```

### Step 4: Windows VM - Victim
```
1. Open browser: http://192.168.56.102:8080/
2. Download "k2_rat_educational.exe"
3. Run the file (click "Yes" on UAC prompt)
4. C2 server will show connection
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

<!-- ---

## 📸 Screenshots
*Add your screenshots here:*
- C2 server with connected target
- Ransomware encryption
- BSOD / crash demonstration
- Wireshark traffic capture

--- -->

## ⚠️ Important Notes
- **Windows Defender** must be disabled in victim VM
- Use only in **isolated lab environment**
- Educational purposes only
- Take VM snapshot before testing kill commands

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
