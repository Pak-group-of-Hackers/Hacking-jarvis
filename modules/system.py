"""
modules/system.py - ALPHA JARVIS System Operations Module
Handles system info, maintenance, backup, notes, and process monitoring.
"""

import os
import subprocess
import time
import json
import shutil
from datetime import datetime

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

NOTES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes", "memory.json")


def run_cmd(cmd, shell=False, timeout=60):
    try:
        result = subprocess.run(
            cmd, shell=shell, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timed out", 1
    except Exception as e:
        return "", str(e), 1


class SystemModule:
    def __init__(self, display, logger, sysinfo):
        self.display = display
        self.logger = logger
        self.sysinfo = sysinfo

    # ── 2. Update Kali ──────────────────────────────────────────────────────

    def update_kali(self):
        self.display.section_header("[2] Update Kali Linux")
        self.display.jarvis_say("Initiating system update sequence.")
        confirm = self.display.prompt_input("This will run apt update & upgrade. Continue? (y/n)")
        if confirm.lower() != "y":
            self.display.warning("Update cancelled.")
            return
        self.display.jarvis_say("Running: apt update...")
        os.system("sudo apt update")
        self.display.jarvis_say("Running: apt upgrade...")
        os.system("sudo apt upgrade -y")
        self.display.success("Kali Linux updated successfully.")
        self.logger.log_activity("Kali system update performed")

    # ── 5. System Information ───────────────────────────────────────────────

    def show_system_info(self):
        self.display.section_header("[5] System Information")
        self.display.jarvis_say("Compiling system intelligence report.")

        info = self.sysinfo.get_all()

        rows = []
        # Basic info
        rows.append(["OS", info.get("os", "N/A")])
        rows.append(["Hostname", info.get("hostname", "N/A")])
        rows.append(["User", info.get("user", "N/A")])
        rows.append(["Shell", info.get("shell", "N/A")])
        rows.append(["Uptime", info.get("uptime", "N/A")])
        rows.append(["CPU Usage", info.get("cpu", "N/A")])
        rows.append(["RAM Usage", info.get("ram", "N/A")])
        rows.append(["Disk Usage", info.get("disk", "N/A")])

        if PSUTIL_AVAILABLE:
            rows.append(["CPU Cores", str(psutil.cpu_count())])
            rows.append(["CPU Freq", f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "N/A"])
            rows.append(["Swap", f"{psutil.swap_memory().used / 1024**3:.2f}GB / {psutil.swap_memory().total / 1024**3:.2f}GB"])

        # Network interfaces
        out, _, _ = run_cmd(["ip", "-brief", "address"], timeout=5)
        if out:
            rows.append(["Network IFs", out.replace("\n", " | ")])

        self.display.print_table(["Property", "Value"], rows, "System Report")
        self.logger.log_activity("System info viewed")

    # ── 18. Logs Viewer ─────────────────────────────────────────────────────

    def logs_viewer(self):
        self.display.section_header("[18] Logs Viewer")
        self.display.jarvis_say("Log analysis system online.")

        choice = self.display.prompt_input(
            "1=JARVIS Activity Log, 2=JARVIS Error Log, 3=System Log (syslog), 4=Auth Log"
        )

        if choice == "1":
            lines = self.logger.get_recent_activity(50)
            if lines:
                for line in lines:
                    self.display.rprint(f"[bright_green]{line.rstrip()}[/bright_green]")
            else:
                self.display.jarvis_say("Activity log is empty.")
        elif choice == "2":
            lines = self.logger.get_recent_errors(50)
            if lines:
                for line in lines:
                    self.display.rprint(f"[bright_red]{line.rstrip()}[/bright_red]")
            else:
                self.display.jarvis_say("Error log is empty.")
        elif choice == "3":
            for path in ["/var/log/syslog", "/var/log/messages"]:
                if os.path.exists(path):
                    out, _, _ = run_cmd(["tail", "-50", path])
                    self.display.rprint(f"[bright_green]{out}[/bright_green]")
                    break
        elif choice == "4":
            if os.path.exists("/var/log/auth.log"):
                out, _, _ = run_cmd(["tail", "-50", "/var/log/auth.log"])
                self.display.rprint(f"[bright_green]{out}[/bright_green]")
            else:
                self.display.error("Auth log not found.")

    # ── 19. Process Monitor ─────────────────────────────────────────────────

    def process_monitor(self):
        self.display.section_header("[19] Process Monitor")
        self.display.jarvis_say("Process monitoring module engaged.")

        if not PSUTIL_AVAILABLE:
            out, _, _ = run_cmd(["ps", "aux", "--sort=-%cpu"])
            self.display.rprint(f"[bright_green]{out[:3000]}[/bright_green]")
            return

        procs = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status"]):
            try:
                p = proc.info
                procs.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        procs.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)
        top = procs[:25]

        rows = [
            [
                str(p.get("pid", "")),
                str(p.get("name", ""))[:20],
                f"{p.get('cpu_percent', 0):.1f}%",
                f"{p.get('memory_percent', 0):.1f}%",
                str(p.get("status", ""))
            ]
            for p in top
        ]
        self.display.print_table(
            ["PID", "Name", "CPU%", "MEM%", "Status"], rows, "Top Processes by CPU"
        )

        kill_pid = self.display.prompt_input("Enter PID to kill (blank to skip)")
        if kill_pid and kill_pid.isdigit():
            try:
                proc = psutil.Process(int(kill_pid))
                proc.terminate()
                self.display.success(f"Process {kill_pid} terminated.")
                self.logger.log_activity(f"Process {kill_pid} killed")
            except Exception as e:
                self.display.error(f"Failed to kill process: {e}")

    # ── 20. RAM & CPU Monitor ───────────────────────────────────────────────

    def ram_cpu_monitor(self):
        self.display.section_header("[20] RAM & CPU Monitor")
        self.display.jarvis_say("System resource monitor active.")

        if not PSUTIL_AVAILABLE:
            os.system("top -b -n 1 | head -20")
            return

        duration = self.display.prompt_input("Monitor for how many seconds? (default 10)")
        try:
            duration = int(duration)
        except ValueError:
            duration = 10

        self.display.jarvis_say(f"Monitoring for {duration} seconds...")
        samples = []
        for i in range(duration):
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            samples.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "cpu": cpu,
                "ram_used": mem.used / 1024**3,
                "ram_pct": mem.percent
            })
            self.display.rprint(
                f"  [cyan]{samples[-1]['time']}[/cyan] | "
                f"CPU: [{'bright_red' if cpu > 80 else 'bright_green'}]{cpu:5.1f}%[/{'bright_red' if cpu > 80 else 'bright_green'}] | "
                f"RAM: [{'bright_red' if mem.percent > 80 else 'bright_green'}]{mem.percent:5.1f}%[/{'bright_red' if mem.percent > 80 else 'bright_green'}] "
                f"({mem.used / 1024**3:.2f}GB)"
            )

        if samples:
            avg_cpu = sum(s["cpu"] for s in samples) / len(samples)
            avg_ram = sum(s["ram_pct"] for s in samples) / len(samples)
            self.display.rprint(f"\n[cyan]Averages:[/cyan] CPU: [bright_green]{avg_cpu:.1f}%[/bright_green] | RAM: [bright_green]{avg_ram:.1f}%[/bright_green]")

        self.logger.log_activity("RAM/CPU monitor used")

    # ── 31. Notes & Memory System ───────────────────────────────────────────

    def notes_memory(self):
        self.display.section_header("[31] Notes & Memory System")
        self.display.jarvis_say("Memory banks online. Ready for input.")

        os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)

        # Load existing notes
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r") as f:
                notes = json.load(f)
        else:
            notes = []

        choice = self.display.prompt_input("1=Add Note, 2=View Notes, 3=Delete Note, 4=Search")

        if choice == "1":
            title = self.display.prompt_input("Note title")
            content = self.display.prompt_input("Note content")
            tag = self.display.prompt_input("Tag (e.g. recon, tool, target)")
            if title:
                notes.append({
                    "id": len(notes) + 1,
                    "title": title,
                    "content": content,
                    "tag": tag,
                    "timestamp": datetime.now().isoformat()
                })
                with open(NOTES_FILE, "w") as f:
                    json.dump(notes, f, indent=2)
                self.display.success(f"Note '{title}' saved.")
                self.logger.log_activity(f"Note added: {title}")

        elif choice == "2":
            if not notes:
                self.display.jarvis_say("No notes stored. Start adding some!")
                return
            rows = [[str(n["id"]), n["title"], n.get("tag", ""), n["timestamp"][:16]] for n in notes]
            self.display.print_table(["ID", "Title", "Tag", "Date"], rows, "Memory Bank")
            view_id = self.display.prompt_input("Enter ID to view full note (blank to skip)")
            if view_id.isdigit():
                for n in notes:
                    if str(n["id"]) == view_id:
                        self.display.rprint(f"\n[cyan]Title:[/cyan] {n['title']}")
                        self.display.rprint(f"[cyan]Tag:[/cyan] {n.get('tag', 'none')}")
                        self.display.rprint(f"[cyan]Date:[/cyan] {n['timestamp'][:16]}")
                        self.display.rprint(f"[cyan]Content:[/cyan]\n{n['content']}")

        elif choice == "3":
            rows = [[str(n["id"]), n["title"]] for n in notes]
            self.display.print_table(["ID", "Title"], rows, "Notes")
            del_id = self.display.prompt_input("Enter ID to delete")
            if del_id.isdigit():
                notes = [n for n in notes if str(n["id"]) != del_id]
                with open(NOTES_FILE, "w") as f:
                    json.dump(notes, f, indent=2)
                self.display.success("Note deleted.")

        elif choice == "4":
            term = self.display.prompt_input("Search term").lower()
            results = [n for n in notes if term in n["title"].lower() or term in n.get("content", "").lower()]
            if results:
                rows = [[str(n["id"]), n["title"], n.get("tag", "")] for n in results]
                self.display.print_table(["ID", "Title", "Tag"], rows, f"Search: '{term}'")
            else:
                self.display.jarvis_say(f"No notes found matching '{term}'.")

    # ── 32. Auto Maintenance ────────────────────────────────────────────────

    def auto_maintenance(self):
        self.display.section_header("[32] Auto Maintenance")
        self.display.jarvis_say("Auto maintenance sequence initiated.")
        confirm = self.display.prompt_input("Run full system maintenance? (y/n)")
        if confirm.lower() != "y":
            return

        steps = [
            ("sudo apt update", "Updating package lists"),
            ("sudo apt upgrade -y", "Upgrading packages"),
            ("sudo apt autoremove -y", "Removing unused packages"),
            ("sudo apt autoclean", "Cleaning apt cache"),
            ("sudo journalctl --vacuum-time=7d", "Cleaning journal logs"),
        ]
        for cmd, desc in steps:
            self.display.jarvis_say(f"{desc}...")
            os.system(cmd)
            self.display.success(f"{desc} complete.")

        self.display.success("Auto maintenance complete. System optimized.")
        self.logger.log_activity("Auto maintenance performed")

    # ── 37. Package Fixer ───────────────────────────────────────────────────

    def package_fixer(self):
        self.display.section_header("[37] Package Fixer")
        self.display.jarvis_say("Package repair module online.")

        steps = [
            "sudo apt --fix-broken install -y",
            "sudo dpkg --configure -a",
            "sudo apt update --fix-missing",
        ]
        for cmd in steps:
            self.display.jarvis_say(f"Running: {cmd}")
            os.system(cmd)

        self.display.success("Package fix completed.")
        self.logger.log_activity("Package fixer ran")

    # ── 38. Backup System ───────────────────────────────────────────────────

    def backup_system(self):
        self.display.section_header("[38] Backup System")
        self.display.jarvis_say("Backup module engaged.")

        backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backup")
        os.makedirs(backup_dir, exist_ok=True)

        choice = self.display.prompt_input("1=Backup JARVIS data, 2=Backup custom path, 3=View backups")

        if choice == "1":
            src = os.path.dirname(os.path.dirname(__file__))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = os.path.join(backup_dir, f"jarvis_backup_{timestamp}.tar.gz")
            self.display.jarvis_say(f"Creating backup: {dest}")
            _, err, rc = run_cmd(
                ["tar", "-czf", dest, "-C", os.path.dirname(src), os.path.basename(src)],
                timeout=120
            )
            if rc == 0:
                size = os.path.getsize(dest) / 1024
                self.display.success(f"Backup created: {dest} ({size:.1f} KB)")
                self.logger.log_activity(f"Backup created: {dest}")
            else:
                self.display.error(f"Backup failed: {err}")

        elif choice == "2":
            src = self.display.prompt_input("Path to backup")
            if src and os.path.exists(src):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name = os.path.basename(src.rstrip("/"))
                dest = os.path.join(backup_dir, f"{name}_{timestamp}.tar.gz")
                _, err, rc = run_cmd(["tar", "-czf", dest, src], timeout=300)
                if rc == 0:
                    self.display.success(f"Backup created: {dest}")
                else:
                    self.display.error(f"Backup failed: {err}")
            else:
                self.display.error("Invalid path.")

        elif choice == "3":
            files = [f for f in os.listdir(backup_dir) if f.endswith(".tar.gz")]
            if files:
                rows = []
                for f in sorted(files, reverse=True):
                    path = os.path.join(backup_dir, f)
                    size = os.path.getsize(path) / 1024
                    rows.append([f, f"{size:.1f} KB"])
                self.display.print_table(["File", "Size"], rows, "Backups")
            else:
                self.display.jarvis_say("No backups found.")

    # ── 39. About Owner ─────────────────────────────────────────────────────

    def about_owner(self):
        self.display.section_header("[39] About Owner")
        self.display.rprint("""
[bright_cyan]╔══════════════════════════════════════════════════════════╗[/bright_cyan]
[bright_cyan]║           ALPHA JARVIS - OWNER PROFILE                   ║[/bright_cyan]
[bright_cyan]╠══════════════════════════════════════════════════════════╣[/bright_cyan]
[bright_cyan]║[/bright_cyan]  [bright_white]Name    :[/bright_white] [bright_green]USER MALIK[/bright_green]                                    [bright_cyan]║[/bright_cyan]
[bright_cyan]║[/bright_cyan]  [bright_white]System  :[/bright_white] [bright_green]ALPHA JARVIS v1.0.0[/bright_green]                           [bright_cyan]║[/bright_cyan]
[bright_cyan]║[/bright_cyan]  [bright_white]Mode    :[/bright_white] [bright_green]OFFLINE AI Cybersecurity Assistant[/bright_green]            [bright_cyan]║[/bright_cyan]
[bright_cyan]║[/bright_cyan]  [bright_white]Platform:[/bright_white] [bright_green]Kali Linux[/bright_green]                                    [bright_cyan]║[/bright_cyan]
[bright_cyan]║[/bright_cyan]  [bright_white]Purpose :[/bright_white] [bright_green]Penetration Testing & Security Research[/bright_green]       [bright_cyan]║[/bright_cyan]
[bright_cyan]╠══════════════════════════════════════════════════════════╣[/bright_cyan]
[bright_cyan]║[/bright_cyan]  [magenta]THINK SMARTER. WORK FASTER. STAY SECURE.[/magenta]              [bright_cyan]║[/bright_cyan]
[bright_cyan]╚══════════════════════════════════════════════════════════╝[/bright_cyan]
""")
