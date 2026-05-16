"""
modules/network.py - ALPHA JARVIS Network Operations Module
Handles all network scanning, monitoring, and information gathering.
"""

import subprocess
import socket
import os
import re
import time
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


def run_cmd(cmd, shell=False, timeout=30):
    """Run a shell command and return output."""
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except FileNotFoundError:
        return "", f"Tool not found: {cmd[0] if isinstance(cmd, list) else cmd}", 1
    except Exception as e:
        return "", str(e), 1


def check_tool(name):
    """Check if a CLI tool is available."""
    out, _, rc = run_cmd(["which", name])
    return rc == 0


class NetworkModule:
    def __init__(self, display, logger):
        self.display = display
        self.logger = logger

    # ── 1. Network Scanning ─────────────────────────────────────────────────

    def network_scan(self):
        self.display.section_header("[1] Network Scanning")
        self.display.jarvis_say("Initiating network scan. Please stand by.")
        target = self.display.prompt_input("Enter target IP/range (e.g. 192.168.1.0/24)")
        if not target:
            self.display.warning("No target specified.")
            return
        if not check_tool("nmap"):
            self.display.error("nmap not found. Install with: sudo apt install nmap")
            return
        self.display.jarvis_say(f"Scanning: {target}")
        out, err, rc = run_cmd(["nmap", "-sV", "--open", target], timeout=120)
        if out:
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        if err and rc != 0:
            self.display.error(err)
        self.logger.log_activity(f"Network scan on target: {target}")
        self.display.success("Network scan completed.")

    # ── 7. Vulnerability Scan ───────────────────────────────────────────────

    def vulnerability_scan(self):
        self.display.section_header("[7] Vulnerability Scan")
        self.display.jarvis_say("Vulnerability scanner armed and ready.")
        target = self.display.prompt_input("Enter target IP/hostname")
        if not target:
            self.display.warning("No target specified.")
            return
        if not check_tool("nmap"):
            self.display.error("nmap not found.")
            return
        self.display.jarvis_say(f"Running vulnerability scripts on {target}...")
        out, err, rc = run_cmd(["nmap", "--script", "vuln", target], timeout=180)
        if out:
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        if err and rc != 0:
            self.display.error(err)
        self.logger.log_activity(f"Vulnerability scan on: {target}")
        self.display.success("Vulnerability scan complete.")

    # ── 8. Port Scanner ─────────────────────────────────────────────────────

    def port_scanner(self):
        self.display.section_header("[8] Port Scanner")
        self.display.jarvis_say("Port scanner module online.")
        target = self.display.prompt_input("Enter target IP/hostname")
        port_range = self.display.prompt_input("Port range (e.g. 1-1000, blank=common ports)")
        if not target:
            self.display.warning("No target specified.")
            return

        if check_tool("nmap"):
            if port_range:
                cmd = ["nmap", "-p", port_range, target]
            else:
                cmd = ["nmap", "--top-ports", "100", target]
            out, err, rc = run_cmd(cmd, timeout=120)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
            if err and rc != 0:
                self.display.error(err)
        else:
            # Pure Python fallback
            self.display.jarvis_say("nmap not found. Using Python socket scanner.")
            start_port, end_port = 1, 1024
            if port_range and "-" in port_range:
                parts = port_range.split("-")
                try:
                    start_port, end_port = int(parts[0]), int(parts[1])
                except ValueError:
                    pass

            open_ports = []
            self.display.jarvis_say(f"Scanning ports {start_port}-{end_port} on {target}...")
            for port in range(start_port, min(end_port + 1, start_port + 200)):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    if s.connect_ex((target, port)) == 0:
                        open_ports.append(port)
                    s.close()
                except Exception:
                    pass
            if open_ports:
                rows = [[str(p), self._get_service(p)] for p in open_ports]
                self.display.print_table(["Port", "Service"], rows, "Open Ports")
            else:
                self.display.jarvis_say("No open ports found in range.")

        self.logger.log_activity(f"Port scan on: {target}")

    def _get_service(self, port):
        common = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
            445: "SMB", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }
        return common.get(port, "Unknown")

    # ── 9. Website Information ──────────────────────────────────────────────

    def website_info(self):
        self.display.section_header("[9] Website Information")
        self.display.jarvis_say("Website intelligence module activated.")
        target = self.display.prompt_input("Enter domain or URL (e.g. example.com)")
        if not target:
            self.display.warning("No target specified.")
            return

        # Strip protocol
        domain = target.replace("https://", "").replace("http://", "").split("/")[0]
        self.display.jarvis_say(f"Gathering information on: {domain}")

        # DNS Resolution
        try:
            ip = socket.gethostbyname(domain)
            self.display.success(f"IP Address: {ip}")
        except socket.gaierror:
            self.display.error(f"Cannot resolve: {domain}")
            ip = None

        # Whois
        if check_tool("whois"):
            out, _, _ = run_cmd(["whois", domain], timeout=15)
            if out:
                lines = [l for l in out.split("\n") if l.strip() and not l.startswith("%")][:30]
                self.display.rprint("[cyan]── WHOIS ──[/cyan]")
                for line in lines:
                    self.display.rprint(f"[dim]{line}[/dim]")

        # DNS records
        if check_tool("dig"):
            for rtype in ["A", "MX", "NS", "TXT"]:
                out, _, _ = run_cmd(["dig", "+short", rtype, domain], timeout=10)
                if out:
                    self.display.rprint(f"[cyan]{rtype}:[/cyan] [bright_white]{out}[/bright_white]")

        # HTTP Headers using curl
        if check_tool("curl"):
            out, _, _ = run_cmd(
                ["curl", "-sI", "--max-time", "5", f"https://{domain}"], timeout=10
            )
            if out:
                self.display.rprint("[cyan]── HTTP Headers ──[/cyan]")
                for line in out.split("\n")[:15]:
                    self.display.rprint(f"[dim]{line}[/dim]")

        self.logger.log_activity(f"Website info gathered for: {domain}")

    # ── 10. IP Tracker ──────────────────────────────────────────────────────

    def ip_tracker(self):
        self.display.section_header("[10] IP Tracker")
        self.display.jarvis_say("IP geolocation module online.")
        ip = self.display.prompt_input("Enter IP address to track (blank = your public IP)")

        if not ip:
            # Get public IP
            out, _, _ = run_cmd(["curl", "-s", "--max-time", "5", "https://api.ipify.org"], timeout=10)
            if out:
                ip = out.strip()
                self.display.jarvis_say(f"Your public IP: {ip}")
            else:
                self.display.error("Could not retrieve public IP. Check internet connection.")
                return

        # Use ip-api.com (free, offline via curl)
        out, err, rc = run_cmd(
            ["curl", "-s", "--max-time", "8",
             f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,lat,lon,timezone"],
            timeout=12
        )
        if out and "{" in out:
            try:
                import json
                data = json.loads(out)
                if data.get("status") == "success":
                    rows = [
                        ["IP", ip],
                        ["Country", data.get("country", "N/A")],
                        ["Region", data.get("regionName", "N/A")],
                        ["City", data.get("city", "N/A")],
                        ["ISP", data.get("isp", "N/A")],
                        ["Org", data.get("org", "N/A")],
                        ["Latitude", str(data.get("lat", "N/A"))],
                        ["Longitude", str(data.get("lon", "N/A"))],
                        ["Timezone", data.get("timezone", "N/A")],
                    ]
                    self.display.print_table(["Field", "Value"], rows, f"IP Info: {ip}")
                else:
                    self.display.error("Could not retrieve IP info.")
            except Exception:
                self.display.rprint(f"[bright_white]{out}[/bright_white]")
        else:
            self.display.error("IP lookup failed. May need internet connection for this feature.")

        self.logger.log_activity(f"IP tracked: {ip}")

    # ── 11. DNS Lookup ──────────────────────────────────────────────────────

    def dns_lookup(self):
        self.display.section_header("[11] DNS Lookup")
        self.display.jarvis_say("DNS lookup module engaged.")
        domain = self.display.prompt_input("Enter domain name")
        if not domain:
            return

        if check_tool("dig"):
            for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
                out, _, _ = run_cmd(["dig", "+short", rtype, domain], timeout=10)
                if out:
                    self.display.rprint(f"  [cyan]{rtype:6s}[/cyan] → [bright_green]{out}[/bright_green]")
                else:
                    self.display.rprint(f"  [cyan]{rtype:6s}[/cyan] → [dim]No record[/dim]")
        elif check_tool("nslookup"):
            out, _, _ = run_cmd(["nslookup", domain], timeout=10)
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        else:
            try:
                ip = socket.gethostbyname(domain)
                self.display.success(f"A record: {ip}")
            except socket.gaierror as e:
                self.display.error(f"DNS resolution failed: {e}")

        self.logger.log_activity(f"DNS lookup: {domain}")

    # ── 12. Ping Test ───────────────────────────────────────────────────────

    def ping_test(self):
        self.display.section_header("[12] Ping Test")
        self.display.jarvis_say("Ping test initiated.")
        target = self.display.prompt_input("Enter target IP/hostname")
        count = self.display.prompt_input("Number of pings (default: 4)")
        if not target:
            return
        count = count if count.isdigit() else "4"
        out, err, rc = run_cmd(["ping", "-c", count, target], timeout=30)
        if out:
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        if rc != 0 and err:
            self.display.error(err)
        self.logger.log_activity(f"Ping test to: {target}")

    # ── 13. Connected Devices ───────────────────────────────────────────────

    def connected_devices(self):
        self.display.section_header("[13] Connected Devices")
        self.display.jarvis_say("Scanning local network for connected devices.")

        if check_tool("arp-scan"):
            iface = self.display.prompt_input("Network interface (e.g. eth0, wlan0, blank=auto)")
            if iface:
                cmd = ["sudo", "arp-scan", f"--interface={iface}", "--localnet"]
            else:
                cmd = ["sudo", "arp-scan", "--localnet"]
            out, err, rc = run_cmd(cmd, timeout=60)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
            else:
                self.display.error(f"arp-scan failed: {err}")
        elif check_tool("netdiscover"):
            self.display.jarvis_say("Using netdiscover...")
            out, err, rc = run_cmd(["sudo", "netdiscover", "-r", "192.168.1.0/24", "-P"], timeout=30)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
        else:
            # Fallback: parse ARP table
            self.display.jarvis_say("Using ARP table fallback...")
            out, _, _ = run_cmd(["arp", "-a"], timeout=10)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
            else:
                self.display.error("No ARP tools available. Install arp-scan: sudo apt install arp-scan")

        self.logger.log_activity("Connected devices scan performed")

    # ── 21. Internet Speed Test ─────────────────────────────────────────────

    def internet_speed_test(self):
        self.display.section_header("[21] Internet Speed Test")
        self.display.jarvis_say("Running speed test. This may take 30-60 seconds...")

        if check_tool("speedtest"):
            out, err, rc = run_cmd(["speedtest"], timeout=90)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
        elif check_tool("speedtest-cli"):
            out, err, rc = run_cmd(["speedtest-cli"], timeout=90)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
        else:
            # Python-based test
            try:
                import speedtest as st
                s = st.Speedtest()
                self.display.jarvis_say("Finding best server...")
                s.get_best_server()
                self.display.jarvis_say("Testing download speed...")
                download = s.download() / 1_000_000
                self.display.jarvis_say("Testing upload speed...")
                upload = s.upload() / 1_000_000
                ping = s.results.ping
                rows = [
                    ["Download", f"{download:.2f} Mbps"],
                    ["Upload", f"{upload:.2f} Mbps"],
                    ["Ping", f"{ping:.2f} ms"],
                ]
                self.display.print_table(["Metric", "Result"], rows, "Speed Test Results")
            except ImportError:
                self.display.error("speedtest-cli not installed. Run: pip install speedtest-cli")

        self.logger.log_activity("Internet speed test performed")

    # ── 22. MAC Address Changer ─────────────────────────────────────────────

    def mac_address_changer(self):
        self.display.section_header("[22] MAC Address Changer")
        self.display.jarvis_say("MAC address changer module loaded.")
        iface = self.display.prompt_input("Enter interface (e.g. eth0, wlan0)")
        if not iface:
            return

        choice = self.display.prompt_input("1=Random MAC, 2=Custom MAC")
        if choice == "1":
            # Generate random MAC
            import random
            mac = "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))
        elif choice == "2":
            mac = self.display.prompt_input("Enter MAC address (XX:XX:XX:XX:XX:XX)")
        else:
            self.display.warning("Invalid choice.")
            return

        self.display.jarvis_say(f"Changing MAC on {iface} to {mac}...")
        cmds = [
            ["sudo", "ip", "link", "set", iface, "down"],
            ["sudo", "ip", "link", "set", iface, "address", mac],
            ["sudo", "ip", "link", "set", iface, "up"],
        ]
        for cmd in cmds:
            _, err, rc = run_cmd(cmd)
            if rc != 0 and err:
                self.display.error(f"Error: {err}")
                return

        self.display.success(f"MAC address changed to: {mac}")
        self.logger.log_activity(f"MAC changed on {iface} to {mac}")

    # ── 23. Network Traffic Monitor ─────────────────────────────────────────

    def network_traffic_monitor(self):
        self.display.section_header("[23] Network Traffic Monitor")
        self.display.jarvis_say("Network traffic monitor armed.")

        choice = self.display.prompt_input("1=tcpdump, 2=iftop, 3=nethogs, 4=Python live stats")
        if choice == "1" and check_tool("tcpdump"):
            iface = self.display.prompt_input("Interface (blank=any)")
            count = self.display.prompt_input("Packets to capture (default 20)")
            count = count if count.isdigit() else "20"
            cmd = ["sudo", "tcpdump", "-c", count, "-nn"]
            if iface:
                cmd += ["-i", iface]
            out, err, rc = run_cmd(cmd, timeout=60)
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        elif choice == "2" and check_tool("iftop"):
            os.system("sudo iftop")
        elif choice == "3" and check_tool("nethogs"):
            os.system("sudo nethogs")
        elif choice == "4":
            self._python_traffic_stats()
        else:
            self._python_traffic_stats()

        self.logger.log_activity("Network traffic monitored")

    def _python_traffic_stats(self):
        """Show live network stats using psutil."""
        if not PSUTIL_AVAILABLE:
            self.display.error("psutil not installed. Run: pip install psutil")
            return
        import psutil, time
        self.display.jarvis_say("Showing live network stats (5 sec). Ctrl+C to stop.")
        try:
            old = psutil.net_io_counters()
            time.sleep(5)
            new = psutil.net_io_counters()
            sent = (new.bytes_sent - old.bytes_sent) / 5 / 1024
            recv = (new.bytes_recv - old.bytes_recv) / 5 / 1024
            rows = [
                ["Bytes Sent/s", f"{sent:.2f} KB/s"],
                ["Bytes Recv/s", f"{recv:.2f} KB/s"],
                ["Total Sent", f"{new.bytes_sent / 1024 / 1024:.2f} MB"],
                ["Total Recv", f"{new.bytes_recv / 1024 / 1024:.2f} MB"],
                ["Packets Sent", str(new.packets_sent)],
                ["Packets Recv", str(new.packets_recv)],
            ]
            self.display.print_table(["Metric", "Value"], rows, "Network Stats")
        except KeyboardInterrupt:
            pass

    # ── 26. Bluetooth Scanner ───────────────────────────────────────────────

    def bluetooth_scanner(self):
        self.display.section_header("[26] Bluetooth Scanner")
        self.display.jarvis_say("Initializing Bluetooth scanner.")

        if check_tool("bluetoothctl"):
            self.display.jarvis_say("Scanning for 10 seconds...")
            out, err, rc = run_cmd(
                "bluetoothctl -- scan on &sleep 10 && bluetoothctl -- devices",
                shell=True, timeout=20
            )
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
            else:
                self.display.warning("No devices found or Bluetooth not available.")
        elif check_tool("hcitool"):
            out, err, rc = run_cmd(["sudo", "hcitool", "scan"], timeout=20)
            if out:
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
        else:
            self.display.error("No Bluetooth tools found. Install: sudo apt install bluetooth bluez")

        self.logger.log_activity("Bluetooth scan performed")

    # ── 27. Firewall Status ─────────────────────────────────────────────────

    def firewall_status(self):
        self.display.section_header("[27] Firewall Status")
        self.display.jarvis_say("Checking firewall status.")

        if check_tool("ufw"):
            out, _, _ = run_cmd(["sudo", "ufw", "status", "verbose"])
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        if check_tool("iptables"):
            self.display.rprint("\n[cyan]── IPTables Rules ──[/cyan]")
            out, _, _ = run_cmd(["sudo", "iptables", "-L", "-n", "--line-numbers"])
            self.display.rprint(f"[bright_green]{out}[/bright_green]")
        if check_tool("firewalld"):
            out, _, _ = run_cmd(["sudo", "firewall-cmd", "--list-all"])
            self.display.rprint(f"[bright_green]{out}[/bright_green]")

        self.logger.log_activity("Firewall status checked")

    # ── 28. Start VPN ───────────────────────────────────────────────────────

    def start_vpn(self):
        self.display.section_header("[28] Start VPN")
        self.display.jarvis_say("VPN module initiated.")

        choice = self.display.prompt_input("1=OpenVPN config file, 2=Check VPN status, 3=Kill VPN")
        if choice == "1":
            config = self.display.prompt_input("Enter path to .ovpn config file")
            if config and os.path.exists(config):
                self.display.jarvis_say(f"Connecting to VPN with config: {config}")
                os.system(f"sudo openvpn --config {config} &")
                self.display.success("VPN process started in background.")
            else:
                self.display.error("Config file not found or not specified.")
        elif choice == "2":
            out, _, _ = run_cmd(["ip", "tun", "show"])
            self.display.rprint(f"[bright_green]{out or 'No active VPN tunnels found.'}[/bright_green]")
            out, _, _ = run_cmd(["pgrep", "-a", "openvpn"])
            if out:
                self.display.success(f"OpenVPN running: {out}")
            else:
                self.display.jarvis_say("OpenVPN not running.")
        elif choice == "3":
            os.system("sudo pkill openvpn")
            self.display.success("VPN terminated.")

        self.logger.log_activity("VPN operation performed")
