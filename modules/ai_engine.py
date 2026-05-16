"""
modules/ai_engine.py - ALPHA JARVIS AI Engine
Offline AI-powered code generation, error solving, and prompt mode.
Uses local knowledge base and pattern matching for offline operation.
"""

import os
import re
import subprocess
import time
from datetime import datetime

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")

# ── Knowledge Base ──────────────────────────────────────────────────────────

TOOL_KNOWLEDGE = {
    "nmap": {
        "description": "Network Mapper - powerful open-source network scanner",
        "usage": "nmap [options] <target>",
        "examples": [
            "nmap -sV 192.168.1.1       # Service version detection",
            "nmap -sn 192.168.1.0/24    # Ping scan (host discovery)",
            "nmap -p 1-65535 target     # Full port scan",
            "nmap --script vuln target  # Vulnerability scripts",
            "nmap -A target             # Aggressive scan (OS, service, scripts)",
        ],
        "flags": {"-sV": "Version detection", "-sS": "SYN stealth scan", "-O": "OS detection",
                  "-A": "Aggressive", "-p": "Port specification", "--script": "Run NSE scripts",
                  "-oN": "Output to file", "-Pn": "Skip host discovery"}
    },
    "netstat": {
        "description": "Network statistics - display network connections and routing tables",
        "usage": "netstat [options]",
        "examples": [
            "netstat -tuln     # Show listening TCP/UDP ports",
            "netstat -anp      # All connections with process names",
            "netstat -r        # Routing table",
            "ss -tuln          # Modern replacement (socket statistics)",
        ]
    },
    "wireshark": {
        "description": "Network protocol analyzer - GUI-based packet capture and analysis",
        "usage": "wireshark / tshark (CLI version)",
        "examples": [
            "wireshark                          # Launch GUI",
            "tshark -i eth0                     # Capture on interface",
            "tshark -r file.pcap               # Read pcap file",
            "tshark -i eth0 -f 'port 80'       # Filter by port",
        ]
    },
    "metasploit": {
        "description": "Advanced penetration testing framework",
        "usage": "msfconsole",
        "examples": [
            "msfconsole                         # Launch Metasploit",
            "use exploit/multi/handler          # Set listener",
            "search type:exploit name:smb       # Search exploits",
            "show payloads                      # List available payloads",
        ]
    },
    "hydra": {
        "description": "Fast password cracker supporting many protocols",
        "usage": "hydra [options] <target>",
        "examples": [
            "hydra -l admin -P passwords.txt ssh://target",
            "hydra -L users.txt -P pass.txt ftp://target",
            "hydra -l user -P pass.txt http-post-form '/login:user=^USER^&pass=^PASS^:F=incorrect'",
        ]
    },
    "gobuster": {
        "description": "Directory/file & DNS busting tool",
        "usage": "gobuster [mode] [options]",
        "examples": [
            "gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt",
            "gobuster dns -d target.com -w subdomains.txt",
        ]
    },
    "sqlmap": {
        "description": "Automatic SQL injection detection and exploitation",
        "usage": "sqlmap [options]",
        "examples": [
            "sqlmap -u 'http://target/page?id=1' --dbs",
            "sqlmap -u 'http://target/page?id=1' -D dbname --tables",
        ]
    },
    "aircrack-ng": {
        "description": "WiFi network security suite",
        "usage": "aircrack-ng [options] <capture file>",
        "examples": [
            "airmon-ng start wlan0              # Enable monitor mode",
            "airodump-ng wlan0mon               # Scan networks",
            "aircrack-ng -w wordlist.txt capture.cap",
        ]
    },
    "burpsuite": {
        "description": "Web application security testing platform",
        "usage": "burpsuite (GUI)",
        "examples": [
            "Launch via: Applications > Web Application Analysis > Burp Suite",
            "Configure browser proxy: 127.0.0.1:8080",
            "Use Proxy > Intercept to capture requests",
        ]
    },
    "tcpdump": {
        "description": "Command-line packet analyzer",
        "usage": "tcpdump [options]",
        "examples": [
            "tcpdump -i eth0                    # Capture on interface",
            "tcpdump -i eth0 port 80            # Filter by port",
            "tcpdump -w output.pcap             # Write to file",
            "tcpdump -r input.pcap              # Read from file",
        ]
    }
}

CODE_TEMPLATES = {
    "port scanner": '''#!/usr/bin/env python3
"""Auto-generated port scanner by ALPHA JARVIS"""
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return port if result == 0 else None
    except Exception:
        return None

def port_scanner(host, start=1, end=1024, threads=100):
    print(f"[*] Scanning {host} ports {start}-{end}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        results = ex.map(lambda p: scan_port(host, p), range(start, end+1))
        for port in results:
            if port:
                open_ports.append(port)
                print(f"  [OPEN] Port {port}")
    print(f"\\n[+] Found {len(open_ports)} open ports.")
    return open_ports

if __name__ == "__main__":
    host = input("Target IP: ")
    port_scanner(host, 1, 1024)
''',
    "network scanner": '''#!/usr/bin/env python3
"""Auto-generated network scanner by ALPHA JARVIS"""
import subprocess
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", str(ip)],
            capture_output=True, timeout=2
        )
        return str(ip) if result.returncode == 0 else None
    except Exception:
        return None

def scan_network(network="192.168.1.0/24"):
    print(f"[*] Scanning network: {network}")
    hosts = list(ipaddress.IPv4Network(network, strict=False).hosts())
    live = []
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = ex.map(ping_host, hosts)
        for ip in results:
            if ip:
                live.append(ip)
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                    print(f"  [UP] {ip} ({hostname})")
                except Exception:
                    print(f"  [UP] {ip}")
    print(f"\\n[+] {len(live)} hosts alive.")
    return live

if __name__ == "__main__":
    net = input("Network (e.g. 192.168.1.0/24): ") or "192.168.1.0/24"
    scan_network(net)
''',
    "password generator": '''#!/usr/bin/env python3
"""Auto-generated password generator by ALPHA JARVIS"""
import secrets
import string

def generate_password(length=16, use_symbols=True):
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|"
    return "".join(secrets.choice(chars) for _ in range(length))

if __name__ == "__main__":
    n = int(input("How many passwords? ") or "5")
    length = int(input("Length? (default 16): ") or "16")
    for i in range(n):
        print(f"  [{i+1}] {generate_password(length)}")
''',
    "web scraper": '''#!/usr/bin/env python3
"""Auto-generated web scraper by ALPHA JARVIS"""
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[!] Install: pip install requests beautifulsoup4")
    exit(1)

def scrape(url):
    headers = {"User-Agent": "Mozilla/5.0 (JARVIS Scanner 1.0)"}
    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.content, "html.parser")
    print(f"Title: {soup.title.string if soup.title else 'N/A'}")
    print(f"\\nLinks found:")
    for a in soup.find_all("a", href=True)[:20]:
        print(f"  {a['href']}")
    print(f"\\nForms found: {len(soup.find_all('form'))}")

if __name__ == "__main__":
    url = input("URL to scrape: ")
    scrape(url)
''',
    "file encryptor": '''#!/usr/bin/env python3
"""Auto-generated file encryptor by ALPHA JARVIS"""
try:
    from cryptography.fernet import Fernet
except ImportError:
    print("[!] Install: pip install cryptography")
    exit(1)
import os

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as f:
        f.write(key)
    print(f"[+] Key saved to secret.key")
    return key

def encrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        data = file.read()
    encrypted = f.encrypt(data)
    with open(filepath + ".enc", "wb") as file:
        file.write(encrypted)
    print(f"[+] Encrypted: {filepath}.enc")

def decrypt_file(filepath, key):
    f = Fernet(key)
    with open(filepath, "rb") as file:
        data = file.read()
    decrypted = f.decrypt(data)
    out = filepath.replace(".enc", ".dec")
    with open(out, "wb") as file:
        file.write(decrypted)
    print(f"[+] Decrypted: {out}")

if __name__ == "__main__":
    action = input("1=Encrypt, 2=Decrypt, 3=Generate key: ")
    if action == "3":
        generate_key()
    elif action in ("1", "2"):
        filepath = input("File path: ")
        keyfile = input("Key file (blank=generate): ")
        if keyfile and os.path.exists(keyfile):
            with open(keyfile, "rb") as f:
                key = f.read()
        else:
            key = generate_key()
        if action == "1":
            encrypt_file(filepath, key)
        else:
            decrypt_file(filepath, key)
''',
    "keylogger": "# [!] JARVIS: Keylogger generation blocked. Use only for authorized testing.\n",
    "reverse shell": "# [!] JARVIS: Reverse shell generation restricted. Use Metasploit for authorized engagements.\n",
}

ERROR_SOLUTIONS = {
    "command not found": {
        "description": "The command or program is not installed or not in PATH.",
        "fixes": [
            "Check if installed: which <command>",
            "Install via apt: sudo apt install <package>",
            "Install via pip: pip install <package>",
            "Check PATH: echo $PATH",
        ]
    },
    "permission denied": {
        "description": "Insufficient permissions to execute the command or access the file.",
        "fixes": [
            "Run as root: sudo <command>",
            "Check file permissions: ls -la <file>",
            "Change permissions: chmod +x <file>",
            "Change ownership: chown $USER:<group> <file>",
        ]
    },
    "no module named": {
        "description": "Python module is not installed.",
        "fixes": [
            "Install module: pip install <module_name>",
            "Install with pip3: pip3 install <module_name>",
            "Check Python version: python3 --version",
            "Install system package: sudo apt install python3-<module>",
        ]
    },
    "connection refused": {
        "description": "Service is not running or port is closed.",
        "fixes": [
            "Check if service is running: systemctl status <service>",
            "Start service: sudo systemctl start <service>",
            "Check if port is open: nmap -p <port> localhost",
            "Check firewall: sudo ufw status",
        ]
    },
    "broken pipe": {
        "description": "The process receiving data has closed its end of the pipe.",
        "fixes": [
            "This is often harmless; try redirecting output to a file.",
            "Use: command 2>/dev/null to suppress error",
            "Check if receiving process is still running",
        ]
    },
    "segmentation fault": {
        "description": "Program accessed memory it shouldn't (crash).",
        "fixes": [
            "Run with gdb for debug: gdb <program>",
            "Check for corrupt input files",
            "Reinstall the program: sudo apt reinstall <package>",
            "Update the system: sudo apt update && sudo apt upgrade",
        ]
    },
    "apt lock": {
        "description": "Another process is using apt package manager.",
        "fixes": [
            "Wait for other apt process to finish",
            "Kill apt: sudo killall apt",
            "Remove lock: sudo rm /var/lib/dpkg/lock-frontend",
            "Fix: sudo dpkg --configure -a",
        ]
    },
}


class AIEngine:
    def __init__(self, display, logger):
        self.display = display
        self.logger = logger
        os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # ── 4. AI Prompt Mode ───────────────────────────────────────────────────

    def ai_prompt_mode(self):
        self.display.section_header("[4] AI Prompt Mode")
        self.display.jarvis_say("AI cognitive systems online. Ask me anything about cybersecurity.")
        self.display.jarvis_say("Type 'exit' to return to main menu.")
        self.display.rprint("\n[dim]Examples: 'What is nmap?' | 'How to use hydra?' | 'Explain SQL injection'[/dim]\n")

        while True:
            query = self.display.prompt_input("You")
            if not query or query.lower() in ("exit", "quit", "back"):
                self.display.jarvis_say("Returning to command deck.")
                break

            self._process_query(query)
            self.logger.log_activity(f"AI Prompt: {query}")

    def _process_query(self, query: str):
        """Process a natural language query."""
        q = query.lower()
        self.display.rprint()

        # Tool-specific queries
        for tool, info in TOOL_KNOWLEDGE.items():
            if tool in q or tool.replace("-", "") in q:
                self.display.ai_say(f"Query confirmed. Here's my intelligence report on {tool}:")
                self.display.rprint(f"\n  [bright_cyan]Description:[/bright_cyan] {info['description']}")
                self.display.rprint(f"  [bright_cyan]Usage:[/bright_cyan] {info['usage']}")
                if "examples" in info:
                    self.display.rprint("  [bright_cyan]Examples:[/bright_cyan]")
                    for ex in info["examples"]:
                        self.display.rprint(f"    [bright_green]{ex}[/bright_green]")
                if "flags" in info:
                    self.display.rprint("  [bright_cyan]Common Flags:[/bright_cyan]")
                    for flag, desc in info["flags"].items():
                        self.display.rprint(f"    [yellow]{flag}[/yellow]: {desc}")
                return

        # General cybersecurity concepts
        if any(w in q for w in ["sql injection", "sqli"]):
            self._explain_concept("SQL Injection",
                "SQL injection is a web security vulnerability where an attacker interferes with SQL queries. "
                "Attackers insert malicious SQL code into input fields to bypass authentication, extract data, "
                "or modify the database. Prevention: use parameterized queries, ORM, input validation.",
                ["' OR '1'='1", "'; DROP TABLE users;--", "1 UNION SELECT * FROM users"])

        elif any(w in q for w in ["xss", "cross site scripting"]):
            self._explain_concept("Cross-Site Scripting (XSS)",
                "XSS allows attackers to inject malicious scripts into web pages viewed by other users. "
                "Types: Stored (persisted), Reflected (URL-based), DOM-based. "
                "Prevention: sanitize output, use CSP headers, encode special characters.",
                ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"])

        elif any(w in q for w in ["port", "ports"]):
            self.display.ai_say("Common network ports you should know:")
            rows = [
                ["21", "FTP - File Transfer Protocol"],
                ["22", "SSH - Secure Shell"],
                ["23", "Telnet (insecure remote access)"],
                ["25", "SMTP - Email sending"],
                ["53", "DNS - Domain Name System"],
                ["80", "HTTP - Web traffic"],
                ["443", "HTTPS - Encrypted web"],
                ["445", "SMB - Windows file sharing"],
                ["3306", "MySQL database"],
                ["3389", "RDP - Remote Desktop"],
                ["6379", "Redis database"],
                ["8080", "HTTP alternative"],
            ]
            self.display.print_table(["Port", "Service"], rows, "Common Ports")

        elif any(w in q for w in ["osint"]):
            self.display.ai_say("OSINT (Open Source Intelligence) is gathering intelligence from public sources.")
            self.display.rprint("\n  [bright_cyan]Tools:[/bright_cyan] theHarvester, Maltego, Shodan, Recon-ng")
            self.display.rprint("  [bright_cyan]Resources:[/bright_cyan] whois, LinkedIn, GitHub, Google Dorks")
            self.display.rprint("  [bright_cyan]Google Dorks:[/bright_cyan]")
            dorks = ['site:example.com filetype:pdf', 'intitle:"index of"', 'inurl:admin', '"password" filetype:txt']
            for d in dorks:
                self.display.rprint(f"    [bright_green]{d}[/bright_green]")

        elif any(w in q for w in ["reconnaissance", "recon"]):
            self.display.ai_say("Reconnaissance is Phase 1 of the Penetration Testing lifecycle.")
            steps = [
                "Passive: WHOIS, DNS lookup, Google Dorks, Shodan, LinkedIn",
                "Active: Nmap scans, Banner grabbing, Service enumeration",
                "Tools: nmap, theHarvester, gobuster, nikto, recon-ng",
            ]
            for s in steps:
                self.display.rprint(f"  [bright_cyan]→[/bright_cyan] {s}")

        elif any(w in q for w in ["privilege escalation", "privesc"]):
            self.display.ai_say("Privilege Escalation techniques (for authorized testing):")
            techs = [
                "SUID binaries: find / -perm -4000 2>/dev/null",
                "Sudo rights: sudo -l",
                "Writable cron jobs: cat /etc/crontab",
                "Kernel exploits: uname -a (check version)",
                "PATH hijacking, weak file permissions",
                "Tools: linPEAS, linux-exploit-suggester",
            ]
            for t in techs:
                self.display.rprint(f"  [bright_green]→[/bright_green] {t}")

        else:
            # Generic helpful response
            self.display.ai_say(f"Query received: '{query}'")
            self.display.rprint("\n  [dim]I have knowledge on: nmap, netstat, wireshark, metasploit, hydra,")
            self.display.rprint("  gobuster, sqlmap, aircrack-ng, burpsuite, tcpdump, port numbers,")
            self.display.rprint("  SQL injection, XSS, OSINT, recon, privilege escalation, and more.[/dim]")
            self.display.rprint("\n  [dim]Try: 'What is nmap?' or 'Explain SQL injection'[/dim]")

    def _explain_concept(self, name, description, examples=None):
        self.display.ai_say(f"Explaining: {name}")
        self.display.rprint(f"\n  [bright_white]{description}[/bright_white]")
        if examples:
            self.display.rprint("  [bright_cyan]Examples:[/bright_cyan]")
            for ex in examples:
                self.display.rprint(f"    [bright_red]{ex}[/bright_red]")

    # ── 29. AI Code Generator ───────────────────────────────────────────────

    def ai_code_generator(self):
        self.display.section_header("[29] AI Code Generator")
        self.display.jarvis_say("Code fabrication unit online. Specify your target.")
        self.display.rprint("\n[dim]Examples: 'port scanner', 'network scanner', 'password generator', 'web scraper', 'file encryptor'[/dim]\n")

        request = self.display.prompt_input("What code should I generate?").lower()
        if not request:
            return

        # Find matching template
        code = None
        matched_key = None
        for key, template in CODE_TEMPLATES.items():
            if key in request or any(word in request for word in key.split()):
                code = template
                matched_key = key
                break

        if not code:
            self.display.jarvis_say("No template matched. Generating generic script framework...")
            code = self._generate_generic_script(request)
            matched_key = request.replace(" ", "_")

        # Safety check
        if code.startswith("# [!] JARVIS"):
            self.display.warning(code)
            return

        # Show code
        self.display.rprint("\n[cyan]── Generated Code ──[/cyan]")
        self.display.rprint(f"[bright_green]{code}[/bright_green]")

        # Save option
        save = self.display.prompt_input("Save to file? (y/n)")
        if save.lower() == "y":
            filename = self.display.prompt_input(
                f"Filename (blank = jarvis_{matched_key.replace(' ', '_')}.py)"
            ) or f"jarvis_{matched_key.replace(' ', '_')}.py"

            if not filename.endswith(".py"):
                filename += ".py"

            filepath = os.path.join(SCRIPTS_DIR, filename)
            with open(filepath, "w") as f:
                f.write(code)
            os.chmod(filepath, 0o755)
            self.display.success(f"Code saved: {filepath}")

            # Run option
            run = self.display.prompt_input("Run now? (y/n)")
            if run.lower() == "y":
                self.display.jarvis_say(f"Executing {filename}...")
                os.system(f"python3 {filepath}")

        self.logger.log_activity(f"AI Code generated: {request}")

    def _generate_generic_script(self, request):
        """Generate a basic script skeleton."""
        return f'''#!/usr/bin/env python3
"""
Auto-generated by ALPHA JARVIS AI Engine
Task: {request}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

import subprocess
import socket
import os

def main():
    """Main function for: {request}"""
    print("[JARVIS] Script loaded. Customize as needed.")
    # TODO: Implement {request} logic here
    pass

if __name__ == "__main__":
    main()
'''

    # ── 30. AI Error Solver ─────────────────────────────────────────────────

    def ai_error_solver(self):
        self.display.section_header("[30] AI Error Solver")
        self.display.jarvis_say("Diagnostic systems online. Paste your error message.")
        self.display.jarvis_say("Type 'exit' to return.")

        while True:
            error = self.display.prompt_input("Error message")
            if not error or error.lower() in ("exit", "quit", "back"):
                break

            self._diagnose_error(error)
            self.logger.log_activity(f"AI Error solved: {error[:60]}")

    def _diagnose_error(self, error: str):
        """Analyze and solve an error message."""
        error_lower = error.lower()
        matched = False

        for pattern, solution in ERROR_SOLUTIONS.items():
            if pattern in error_lower:
                matched = True
                self.display.ai_say(f"Error pattern identified: '{pattern}'")
                self.display.rprint(f"\n  [bright_cyan]Diagnosis:[/bright_cyan] {solution['description']}")
                self.display.rprint("  [bright_cyan]Solutions:[/bright_cyan]")
                for fix in solution["fixes"]:
                    self.display.rprint(f"    [bright_green]→[/bright_green] {fix}")

                # Auto-fix for "no module named"
                if "no module named" in error_lower:
                    module_match = re.search(r"no module named ['\"]?(\w[\w.]*)['\"]?", error_lower)
                    if module_match:
                        module = module_match.group(1)
                        auto_fix = self.display.prompt_input(
                            f"Auto-install '{module}' with pip? (y/n)"
                        )
                        if auto_fix.lower() == "y":
                            self.display.jarvis_say(f"Installing {module}...")
                            os.system(f"pip install {module}")

                # Auto-fix for "command not found"
                if "command not found" in error_lower:
                    cmd_match = re.search(r"(\w[\w-]*): command not found", error_lower)
                    if cmd_match:
                        cmd = cmd_match.group(1)
                        auto_fix = self.display.prompt_input(
                            f"Auto-install '{cmd}' with apt? (y/n)"
                        )
                        if auto_fix.lower() == "y":
                            self.display.jarvis_say(f"Installing {cmd}...")
                            os.system(f"sudo apt install {cmd} -y")
                break

        if not matched:
            self.display.ai_say("Error pattern not in database. Running general analysis...")
            # Try to extract useful info
            if "python" in error_lower or "traceback" in error_lower:
                self.display.rprint("  [bright_cyan]→[/bright_cyan] Python error detected.")
                self.display.rprint("    Check: syntax, imports, file paths, variable names")
            elif any(w in error_lower for w in ["network", "connection", "timeout"]):
                self.display.rprint("  [bright_cyan]→[/bright_cyan] Network error detected.")
                self.display.rprint("    Check: firewall, DNS, target availability, internet connection")
            else:
                self.display.rprint("  [dim]General advice:[/dim]")
                self.display.rprint("    → Search: https://stackoverflow.com (offline: paste to search when online)")
                self.display.rprint("    → Check man page: man <command>")
                self.display.rprint("    → Check --help: <command> --help")
