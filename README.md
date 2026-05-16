# ALPHA JARVIS - AI Cybersecurity Assistant

```
-:-- ALPHA OFFLINE AI CYBER ASSISTANT -:--
     J A R V I S  v1.0.0
  THINK SMARTER. WORK FASTER. STAY SECURE
```

## Overview

ALPHA JARVIS is a modular, offline CLI-based cybersecurity toolkit for Kali Linux.
It provides 40 integrated tools with a hacker-themed terminal interface.

## Installation

```bash
# Quick install
chmod +x install.sh && ./install.sh

# Manual install
pip3 install rich psutil tqdm cryptography speedtest-cli
sudo apt install nmap curl whois dnsutils arp-scan
```

## Usage

```bash
python3 main.py
```

## Project Structure

```
ALPHA-JARVIS/
├── main.py              # Entry point
├── install.sh           # Auto-installer
├── requirements.txt     # Python dependencies
├── core/
│   ├── display.py       # UI rendering engine
│   ├── menu.py          # Menu router
│   └── logger.py        # Logging system
├── modules/
│   ├── network.py       # Network tools (scan, ping, DNS, VPN...)
│   ├── system.py        # System tools (info, maintenance, backup...)
│   ├── ai_engine.py     # AI features (code gen, error solver, prompt)
│   ├── security.py      # Security (encryption, passwords)
│   └── tools.py         # Misc tools (terminal, installer...)
├── utils/
│   └── system_info.py   # System info collector
├── logs/                # Activity & error logs
├── notes/               # Notes & memory system
├── scripts/             # AI-generated scripts
├── backup/              # System backups
└── ai/                  # Encryption keys & AI data
```

## Menu Options (40 tools)

| # | Tool | Description |
|---|------|-------------|
| 1 | Network Scanning | nmap -sV full network scan |
| 2 | Update Kali | apt update & upgrade |
| 3 | Open Wireshark | Packet analyzer (GUI/CLI) |
| 4 | AI Prompt Mode | Ask JARVIS about any security tool |
| 5 | System Information | Full system report |
| 6 | Open Nmap | Interactive nmap launcher |
| 7 | Vulnerability Scan | nmap --script vuln |
| 8 | Port Scanner | nmap or Python socket scanner |
| 9 | Website Information | WHOIS, DNS, HTTP headers |
| 10 | IP Tracker | Geolocation via ip-api.com |
| 11 | DNS Lookup | A, MX, NS, TXT, CNAME records |
| 12 | Ping Test | ICMP ping test |
| 13 | Connected Devices | arp-scan / netdiscover |
| 14 | Open Metasploit | msfconsole launcher |
| 15 | Open Burp Suite | Web app tester |
| 16 | Password Generator | Cryptographically secure passwords |
| 17 | File Encryption | Fernet AES encryption |
| 18 | Logs Viewer | JARVIS + system logs |
| 19 | Process Monitor | Top processes + kill option |
| 20 | RAM & CPU Monitor | Live resource monitoring |
| 21 | Internet Speed Test | speedtest-cli |
| 22 | MAC Address Changer | Random or custom MAC |
| 23 | Network Traffic Monitor | tcpdump / Python stats |
| 24 | Screenshot Tool | scrot / gnome-screenshot |
| 25 | Webcam Checker | v4l2 device detection |
| 26 | Bluetooth Scanner | bluetoothctl scan |
| 27 | Firewall Status | ufw / iptables status |
| 28 | Start VPN | OpenVPN launcher |
| 29 | AI Code Generator | Generate Python security scripts |
| 30 | AI Error Solver | Diagnose and fix errors |
| 31 | Notes & Memory | JSON-based note system |
| 32 | Auto Maintenance | Full apt maintenance |
| 33 | Open Terminal | Subshell |
| 34 | Custom Script Runner | Run saved scripts |
| 35 | Dark Mode UI | Theme toggle |
| 36 | Tool Installer | Install 25+ pentest tools |
| 37 | Package Fixer | apt --fix-broken |
| 38 | Backup System | tar.gz backup creator |
| 39 | About Owner | Owner profile |
| 0 | Exit | Shutdown JARVIS |

## AI Features

### AI Prompt Mode [4]
Ask questions like:
- "What is nmap?"
- "How to use hydra?"
- "Explain SQL injection"
- "What are common ports?"
- "Explain privilege escalation"

### AI Code Generator [29]
Templates for:
- Port scanner
- Network scanner
- Password generator
- Web scraper
- File encryptor

### AI Error Solver [30]
Auto-detects and fixes:
- `command not found` → auto-installs
- `No module named` → pip auto-install
- `Permission denied` → suggests chmod/sudo
- `Connection refused` → service check
- `Segmentation fault` → debug guidance

## Requirements

- **OS**: Kali Linux (or any Debian-based distro)
- **Python**: 3.8+
- **Privileges**: Some tools require `sudo`

## Owner

```
USER MALIK | ALPHA JARVIS v1.0.0 | OFFLINE MODE
THINK SMARTER. WORK FASTER. STAY SECURE.
```

---
*For authorized penetration testing and security research only.*
