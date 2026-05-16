"""
modules/tools.py - ALPHA JARVIS Tools Module
Miscellaneous tools: terminal, screenshots, webcam, installers, etc.
"""

import os
import subprocess
import time
from datetime import datetime

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts")


def run_cmd(cmd, shell=False, timeout=30):
    try:
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timed out", 1
    except Exception as e:
        return "", str(e), 1


def check_tool(name):
    out, _, rc = run_cmd(["which", name])
    return rc == 0


# ── Tool installation catalog ────────────────────────────────────────────────

PENTEST_TOOLS = {
    "nmap": "Network scanner",
    "wireshark": "Packet analyzer",
    "metasploit-framework": "Exploit framework",
    "burpsuite": "Web app tester",
    "sqlmap": "SQL injection tool",
    "hydra": "Password cracker",
    "gobuster": "Directory bruster",
    "nikto": "Web server scanner",
    "aircrack-ng": "WiFi security suite",
    "hashcat": "Password hash cracker",
    "john": "John the Ripper (password cracker)",
    "netcat": "Networking utility",
    "tcpdump": "Packet capture",
    "arp-scan": "Network host discovery",
    "dirb": "Web content scanner",
    "whatweb": "Web tech fingerprinting",
    "theharvester": "OSINT email/subdomain finder",
    "recon-ng": "OSINT framework",
    "maltego": "Visual intelligence platform",
    "enum4linux": "Linux/Samba enumeration",
    "smbclient": "SMB client",
    "wifite": "Automated WiFi auditor",
    "masscan": "Fast port scanner",
    "responder": "LLMNR/NBT-NS poisoner",
    "impacket-scripts": "Windows protocol tools",
    "bloodhound": "AD attack path analyzer",
    "crackmapexec": "Active directory tool",
}


class ToolsModule:
    def __init__(self, display, logger):
        self.display = display
        self.logger = logger
        os.makedirs(SCRIPTS_DIR, exist_ok=True)

    # ── 3. Open Wireshark ───────────────────────────────────────────────────

    def open_wireshark(self):
        self.display.section_header("[3] Open Wireshark")
        self.display.jarvis_say("Launching Wireshark packet analyzer...")
        if check_tool("wireshark"):
            os.system("wireshark &")
            self.display.success("Wireshark launched in background.")
        elif check_tool("tshark"):
            self.display.jarvis_say("GUI Wireshark not found. Launching tshark (CLI)...")
            iface = self.display.prompt_input("Interface (e.g. eth0)")
            os.system(f"sudo tshark -i {iface or 'any'}")
        else:
            self.display.error("Wireshark not installed.")
            install = self.display.prompt_input("Install now? (y/n)")
            if install.lower() == "y":
                os.system("sudo apt install wireshark -y")
        self.logger.log_activity("Wireshark opened")

    # ── 6. Open Nmap ────────────────────────────────────────────────────────

    def open_nmap(self):
        self.display.section_header("[6] Open Nmap")
        self.display.jarvis_say("Nmap network mapper loaded.")
        if not check_tool("nmap"):
            self.display.error("nmap not found. Installing...")
            os.system("sudo apt install nmap -y")
            return

        self.display.rprint("""
[bright_cyan]Quick Nmap Reference:[/bright_cyan]
  [bright_green]nmap -sV <target>[/bright_green]          → Version detection
  [bright_green]nmap -sS <target>[/bright_green]          → SYN stealth scan
  [bright_green]nmap -A <target>[/bright_green]           → Aggressive scan
  [bright_green]nmap --script vuln <target>[/bright_green] → Vulnerability scan
  [bright_green]nmap -p 1-65535 <target>[/bright_green]   → Full port scan
  [bright_green]nmap -sn 192.168.1.0/24[/bright_green]   → Ping sweep
""")
        cmd = self.display.prompt_input("Enter custom nmap command (after 'nmap')")
        if cmd:
            self.display.jarvis_say(f"Running: nmap {cmd}")
            os.system(f"sudo nmap {cmd}")
            self.logger.log_activity(f"Nmap executed: {cmd}")

    # ── 14. Open Metasploit ─────────────────────────────────────────────────

    def open_metasploit(self):
        self.display.section_header("[14] Open Metasploit")
        self.display.jarvis_say("Initializing Metasploit Framework...")
        if check_tool("msfconsole"):
            self.display.jarvis_say("Launching msfconsole. Type 'exit' to return to JARVIS.")
            os.system("msfconsole")
        else:
            self.display.error("Metasploit not found.")
            install = self.display.prompt_input("Install now? (y/n)")
            if install.lower() == "y":
                os.system("sudo apt install metasploit-framework -y")
        self.logger.log_activity("Metasploit opened")

    # ── 15. Open Burp Suite ─────────────────────────────────────────────────

    def open_burp_suite(self):
        self.display.section_header("[15] Open Burp Suite")
        self.display.jarvis_say("Launching Burp Suite web application tester...")
        if check_tool("burpsuite"):
            os.system("burpsuite &")
            self.display.success("Burp Suite launched.")
        else:
            self.display.error("Burp Suite not found.")
            self.display.jarvis_say("Install via: sudo apt install burpsuite")
            self.display.jarvis_say("Or download from: https://portswigger.net/burp")
        self.logger.log_activity("Burp Suite opened")

    # ── 24. Screenshot Tool ─────────────────────────────────────────────────

    def screenshot_tool(self):
        self.display.section_header("[24] Screenshot Tool")
        self.display.jarvis_say("Screenshot module engaged.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = os.path.expanduser("~/screenshots")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"jarvis_{timestamp}.png")

        if check_tool("scrot"):
            delay = self.display.prompt_input("Delay in seconds (0 for immediate)")
            delay = delay if delay.isdigit() else "0"
            os.system(f"scrot -d {delay} {out_path}")
            self.display.success(f"Screenshot saved: {out_path}")
        elif check_tool("import"):
            os.system(f"import -window root {out_path}")
            self.display.success(f"Screenshot saved: {out_path}")
        elif check_tool("gnome-screenshot"):
            os.system(f"gnome-screenshot -f {out_path}")
            self.display.success(f"Screenshot saved: {out_path}")
        else:
            self.display.error("No screenshot tool found.")
            self.display.jarvis_say("Install: sudo apt install scrot")

        self.logger.log_activity(f"Screenshot taken: {out_path}")

    # ── 25. Webcam Checker ──────────────────────────────────────────────────

    def webcam_checker(self):
        self.display.section_header("[25] Webcam Checker")
        self.display.jarvis_say("Scanning for video capture devices.")

        # Check /dev/video* devices
        devices = [f for f in os.listdir("/dev") if f.startswith("video")]
        if devices:
            rows = [[f"/dev/{d}", "Active"] for d in devices]
            self.display.print_table(["Device", "Status"], rows, "Video Devices")
        else:
            self.display.jarvis_say("No video devices found at /dev/video*")

        # v4l2 info
        if check_tool("v4l2-ctl"):
            out, _, _ = run_cmd(["v4l2-ctl", "--list-devices"])
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")

        # FFmpeg preview
        if devices and check_tool("ffplay"):
            preview = self.display.prompt_input("Launch webcam preview? (y/n)")
            if preview.lower() == "y":
                os.system(f"ffplay -f v4l2 /dev/{devices[0]} &")

        self.logger.log_activity("Webcam checked")

    # ── 33. Open Terminal ───────────────────────────────────────────────────

    def open_terminal(self):
        self.display.section_header("[33] Open Terminal")
        self.display.jarvis_say("Spawning subshell. Type 'exit' to return to JARVIS.")
        os.system(os.getenv("SHELL", "bash"))
        self.display.jarvis_say("Returned from subshell.")
        self.logger.log_activity("Subshell terminal opened")

    # ── 34. Custom Script Runner ────────────────────────────────────────────

    def custom_script_runner(self):
        self.display.section_header("[34] Custom Script Runner")
        self.display.jarvis_say("Script execution module online.")

        # List available scripts
        scripts = []
        if os.path.exists(SCRIPTS_DIR):
            scripts = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith((".py", ".sh", ".rb"))]

        if scripts:
            self.display.rprint("\n[cyan]Available scripts:[/cyan]")
            rows = [[str(i + 1), s] for i, s in enumerate(scripts)]
            self.display.print_table(["#", "Script"], rows, "Script Library")

        script_path = self.display.prompt_input(
            "Enter script path or number from list (blank=custom path)"
        )

        if script_path.isdigit() and scripts:
            idx = int(script_path) - 1
            if 0 <= idx < len(scripts):
                script_path = os.path.join(SCRIPTS_DIR, scripts[idx])

        if not script_path or not os.path.exists(script_path):
            self.display.error("Script not found.")
            return

        self.display.jarvis_say(f"Executing: {script_path}")
        if script_path.endswith(".py"):
            os.system(f"python3 {script_path}")
        elif script_path.endswith(".sh"):
            os.system(f"bash {script_path}")
        elif script_path.endswith(".rb"):
            os.system(f"ruby {script_path}")

        self.logger.log_activity(f"Script executed: {script_path}")

    # ── 35. Toggle Dark Mode ────────────────────────────────────────────────

    def toggle_dark_mode(self):
        self.display.section_header("[35] UI Theme Toggle")
        self.display.jarvis_say("Interface theme configuration module.")
        self.display.rprint("\n[dim]Terminal color scheme is managed by your terminal emulator.[/dim]")
        self.display.rprint("[dim]Recommended: Use a dark terminal theme for optimal JARVIS experience.[/dim]\n")

        themes = [
            ("Kali Default Dark", "Dark hacker theme"),
            ("Solarized Dark", "Low-contrast dark"),
            ("Dracula", "Purple-dark aesthetic"),
            ("Monokai", "Vibrant dark theme"),
            ("One Dark Pro", "Atom-inspired dark"),
        ]
        rows = [[str(i + 1), t[0], t[1]] for i, t in enumerate(themes)]
        self.display.print_table(["#", "Theme", "Description"], rows, "Recommended Terminal Themes")
        self.display.jarvis_say("Configure via: Terminal > Preferences > Colors")

        # Toggle UI density
        current = getattr(self.display, "theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        self.display.theme = new_theme
        self.display.success(f"JARVIS UI mode set to: {new_theme.upper()}")

    # ── 36. Tool Installer ──────────────────────────────────────────────────

    def tool_installer(self):
        self.display.section_header("[36] Tool Installer")
        self.display.jarvis_say("Penetration testing tool installer armed.")

        rows = [[str(i + 1), name, desc] for i, (name, desc) in enumerate(PENTEST_TOOLS.items())]
        self.display.print_table(["#", "Tool", "Description"], rows, "Available Tools")

        choice = self.display.prompt_input(
            "Enter tool number, tool name, or 'all' for full suite"
        )

        if choice.lower() == "all":
            confirm = self.display.prompt_input(
                f"Install ALL {len(PENTEST_TOOLS)} tools? This may take a while. (y/n)"
            )
            if confirm.lower() == "y":
                tools_list = " ".join(PENTEST_TOOLS.keys())
                self.display.jarvis_say("Installing full penetration testing suite...")
                os.system(f"sudo apt install {tools_list} -y")
                self.display.success("Full tool suite installed.")
        elif choice.isdigit():
            tools = list(PENTEST_TOOLS.keys())
            idx = int(choice) - 1
            if 0 <= idx < len(tools):
                tool = tools[idx]
                self.display.jarvis_say(f"Installing: {tool}")
                os.system(f"sudo apt install {tool} -y")
                self.display.success(f"{tool} installed.")
        else:
            # Custom tool name
            self.display.jarvis_say(f"Installing: {choice}")
            os.system(f"sudo apt install {choice} -y")

        self.logger.log_activity(f"Tool installer: {choice}")
