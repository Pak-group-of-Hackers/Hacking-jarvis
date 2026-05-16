#!/bin/bash
# ALPHA JARVIS - Installation Script
# Run as root or with sudo

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║      ALPHA JARVIS - Installation Script                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}[*] Updating package lists...${NC}"
sudo apt update

echo -e "${CYAN}[*] Installing Python dependencies...${NC}"
pip3 install rich psutil tqdm cryptography speedtest-cli --break-system-packages 2>/dev/null || \
pip3 install rich psutil tqdm cryptography speedtest-cli

echo -e "${CYAN}[*] Installing essential system tools...${NC}"
sudo apt install -y nmap curl wget whois dnsutils arp-scan net-tools \
    python3-psutil python3-cryptography 2>/dev/null

echo -e "${CYAN}[*] Setting permissions...${NC}"
chmod +x main.py
mkdir -p logs notes scripts backup ai

echo -e "${GREEN}[✓] ALPHA JARVIS installation complete!${NC}"
echo -e "${GREEN}[✓] Run with: python3 main.py${NC}"
echo ""
