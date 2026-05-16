"""
core/display.py - ALPHA JARVIS Display & UI Engine
Handles all terminal rendering, banners, menus, and styled output.
"""

import os
import time
import sys
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich.columns import Columns
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.align import Align
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


BANNER_ART = r"""
     ___   _     ____  _   _    __       _   ___   ____  __   ___  
    / _ | | |   | __ \| | | |  /  \     | | / _ | |  _ \\ \ / / | 
   / /_| || |   |  __/| |_| | / /\ \    | |/ /_| || |_) |\ V /  | 
  / /  |_||_|   |_|   |_____||_/  \_\   |_|/  |_||____/  \_/   |_|
"""

IRON_MAN_ASCII = r"""
        ██████████████
      ██  ██      ██  ██
     █  ████      ████  █
    █  ██  ████████  ██  █
    █ ██  ██████████  ██ █
    █ ██ ████    ████ ██ █
    █  ████  ████  ████  █
     █  ██  ██  ██  ██  █
      ██  ████████████  ██
        ████████████████
          ██        ██
         ████      ████
"""

MENU_ITEMS = [
    (" 1", "Network Scanning"),
    (" 2", "Update Kali"),
    (" 3", "Open Wireshark"),
    (" 4", "AI Prompt Mode"),
    (" 5", "System Information"),
    (" 6", "Open Nmap"),
    (" 7", "Vulnerability Scan"),
    (" 8", "Port Scanner"),
    (" 9", "Website Information"),
    ("10", "IP Tracker"),
    ("11", "DNS Lookup"),
    ("12", "Ping Test"),
    ("13", "Connected Devices"),
    ("14", "Open Metasploit"),
    ("15", "Open Burp Suite"),
    ("16", "Password Generator"),
    ("17", "File Encryption"),
    ("18", "Logs Viewer"),
    ("19", "Process Monitor"),
    ("20", "RAM & CPU Monitor"),
    ("21", "Internet Speed Test"),
    ("22", "MAC Address Changer"),
    ("23", "Network Traffic Monitor"),
    ("24", "Screenshot Tool"),
    ("25", "Webcam Checker"),
    ("26", "Bluetooth Scanner"),
    ("27", "Firewall Status"),
    ("28", "Start VPN"),
    ("29", "AI Code Generator"),
    ("30", "AI Error Solver"),
    ("31", "Notes & Memory"),
    ("32", "Auto Maintenance"),
    ("33", "Open Terminal"),
    ("34", "Custom Script Runner"),
    ("35", "Dark Mode UI"),
    ("36", "Tool Installer"),
    ("37", "Package Fixer"),
    ("38", "Backup System"),
    ("39", "About Owner"),
    (" 0", "Exit"),
]


class Display:
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.theme = "dark"  # dark / light

    def clear_screen(self):
        os.system("clear" if os.name != "nt" else "cls")

    def print_raw(self, text, color="cyan"):
        """Fallback print when rich not available."""
        colors = {
            "cyan": "\033[96m", "green": "\033[92m", "red": "\033[91m",
            "yellow": "\033[93m", "magenta": "\033[95m", "white": "\033[97m",
            "dim": "\033[2m", "bold": "\033[1m"
        }
        reset = "\033[0m"
        c = colors.get(color, "")
        print(f"{c}{text}{reset}")

    def rprint(self, text, style=""):
        if RICH_AVAILABLE:
            self.console.print(text, style=style)
        else:
            print(text)

    def show_boot_animation(self):
        """Display animated boot sequence."""
        if RICH_AVAILABLE:
            self.console.print("\n")
            boot_steps = [
                "Initializing ALPHA JARVIS core systems...",
                "Loading AI neural engine...",
                "Scanning network interfaces...",
                "Checking security modules...",
                "Verifying system integrity...",
                "Establishing secure environment...",
                "Boot sequence complete. Welcome, USER MALIK.",
            ]

            with Progress(
                SpinnerColumn(style="cyan"),
                TextColumn("[cyan]{task.description}"),
                BarColumn(bar_width=40, style="cyan", complete_style="bright_cyan"),
                TextColumn("[bright_green]{task.percentage:>3.0f}%"),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task("Booting ALPHA JARVIS...", total=100)
                for i, step in enumerate(boot_steps):
                    progress.update(task, description=f"[cyan]{step}", advance=100 / len(boot_steps))
                    time.sleep(0.3)
            self.console.print("[bright_green]✓ All systems online.[/bright_green]\n")
            time.sleep(0.5)
        else:
            steps = [
                "Initializing systems", "Loading AI engine", "Checking modules",
                "Verifying integrity", "Boot complete"
            ]
            for step in steps:
                print(f"\033[96m[*] {step}...\033[0m")
                time.sleep(0.3)
            print("\033[92m[✓] Systems online.\033[0m\n")

    def show_banner(self):
        """Display the main JARVIS banner."""
        self.clear_screen()
        if RICH_AVAILABLE:
            # Top border
            self.console.print("[cyan]" + "─" * 80 + "[/cyan]")

            # Title
            title_text = Text()
            title_text.append("  -:-- ", style="cyan")
            title_text.append("ALPHA OFFLINE AI CYBER ASSISTANT", style="bold bright_cyan")
            title_text.append(" -:--", style="cyan")
            self.console.print(Align.center(title_text))
            self.console.print()

            # Iron Man art + JARVIS title side by side
            iron_man = Panel(
                Text(IRON_MAN_ASCII, style="cyan"),
                border_style="cyan",
                width=30,
                padding=(0, 1)
            )

            right_content = Table.grid(padding=1)
            right_content.add_column()

            jarvis_text = Text()
            jarvis_text.append("  ╔╦╗╔═╗╦═╗╦  ╦╦╔═╗\n", style="bold bright_cyan")
            jarvis_text.append("   ║ ╠═╣╠╦╝╚╗╔╝║╚═╗\n", style="bold cyan")
            jarvis_text.append("   ╩ ╩ ╩╩╚═ ╚╝ ╩╚═╝\n", style="bold cyan")

            info_table = Table(box=box.SQUARE, border_style="cyan", show_header=False, padding=(0, 2))
            info_table.add_column(style="cyan")
            info_table.add_column(style="bright_white")
            info_table.add_row("OWNER", ": USER MALIK")
            info_table.add_row("VERSION", ": 1.0.0 OFFLINE")

            tagline = Text()
            tagline.append("  ─A─[ ", style="cyan")
            tagline.append("THINK SMARTER. WORK FASTER. STAY SECURE", style="bold magenta")
            tagline.append(" ]─A─", style="cyan")

            right_content.add_row(jarvis_text)
            right_content.add_row(info_table)
            right_content.add_row(tagline)

            from rich.columns import Columns
            self.console.print(Columns([iron_man, right_content]))
            self.console.print("[cyan]" + "─" * 80 + "[/cyan]\n")
        else:
            print("\033[96m" + "─" * 70 + "\033[0m")
            print("\033[1;96m       -:-- ALPHA OFFLINE AI CYBER ASSISTANT -:--\033[0m")
            print("\033[1;36m              J A R V I S   v1.0.0\033[0m")
            print("\033[96m" + "─" * 70 + "\033[0m\n")

    def show_system_status(self, sysinfo):
        """Display system info status bar."""
        if RICH_AVAILABLE:
            info = sysinfo.get_all()
            status_table = Table(box=box.SIMPLE, border_style="cyan", show_header=False, padding=(0, 2))
            status_table.add_column(style="bright_cyan")
            status_table.add_column(style="bright_white")
            status_table.add_column(style="bright_cyan")
            status_table.add_column(style="bright_white")
            status_table.add_column(style="bright_cyan")
            status_table.add_column(style="bright_white")
            status_table.add_column(style="bright_green")

            status_table.add_row(
                "🐧 OS:", info.get("os", "Kali Linux"),
                "📅 DATE:", info.get("date", datetime.now().strftime("%m-%d-%Y")),
                "⚙ CPU:", info.get("cpu", "N/A"),
                ""
            )
            status_table.add_row(
                "👤 USER:", info.get("user", "root"),
                "🕐 TIME:", info.get("time", datetime.now().strftime("%I:%M:%S %p")),
                "🖥 RAM:", info.get("ram", "N/A"),
                "STATUS:"
            )
            status_table.add_row(
                "💻 SHELL:", info.get("shell", "bash"),
                "⏱ UP:", info.get("uptime", "N/A"),
                "💾 DISK:", info.get("disk", "N/A"),
                "[bright_green]SECURE ✓[/bright_green]"
            )

            panel = Panel(status_table, border_style="cyan", title="[cyan]SYSTEM STATUS[/cyan]")
            self.console.print(panel)
            self.console.print()
        else:
            info = sysinfo.get_all()
            print(f"\033[96m[SYS] CPU: {info.get('cpu')} | RAM: {info.get('ram')} | STATUS: SECURE\033[0m\n")

    def show_menu(self):
        """Display the main numbered menu."""
        if RICH_AVAILABLE:
            self.console.print("[cyan]" + "─" * 80 + "[/cyan]")
            self.console.print(Align.center("[bold bright_cyan]── MAIN MENU ──[/bold bright_cyan]"))
            self.console.print("[cyan]" + "─" * 80 + "[/cyan]")

            # Split menu into 3 columns
            col_size = 14
            col1 = MENU_ITEMS[:col_size]
            col2 = MENU_ITEMS[col_size:col_size*2]
            col3 = MENU_ITEMS[col_size*2:]

            table = Table(
                box=box.SIMPLE,
                show_header=False,
                padding=(0, 1),
                border_style="cyan",
                expand=True
            )
            table.add_column(ratio=1)
            table.add_column(ratio=1)
            table.add_column(ratio=1)

            max_rows = max(len(col1), len(col2), len(col3))
            for i in range(max_rows):
                c1 = self._menu_cell(col1[i] if i < len(col1) else None)
                c2 = self._menu_cell(col2[i] if i < len(col2) else None)
                c3 = self._menu_cell(col3[i] if i < len(col3) else None, last_col=True)
                table.add_row(c1, c2, c3)

            self.console.print(table)
            self.console.print("[cyan]" + "─" * 80 + "[/cyan]")
        else:
            print("\033[96m" + "─" * 60 + "\033[0m")
            print("\033[1;96m           MAIN MENU\033[0m")
            print("\033[96m" + "─" * 60 + "\033[0m")
            for num, label in MENU_ITEMS:
                color = "\033[91m" if num.strip() == "0" else "\033[92m"
                print(f"  \033[96m[{num}]\033[0m {color}{label}\033[0m")
            print("\033[96m" + "─" * 60 + "\033[0m")

    def _menu_cell(self, item, last_col=False):
        """Format a single menu cell."""
        if item is None:
            return ""
        num, label = item
        if num.strip() == "0":
            return f"[cyan][[/cyan][bold red]{num}[/bold red][cyan]][/cyan] [red]{label}[/red]"
        return f"[cyan][[/cyan][bright_green]{num}[/bright_green][cyan]][/cyan] [bright_white]{label}[/bright_white]"

    def get_choice(self):
        """Get user menu choice."""
        if RICH_AVAILABLE:
            self.console.print()
            self.console.print("[bright_cyan]JARVIS>[/bright_cyan] ", end="")
            try:
                choice = input("Enter your choice [0-39]: ").strip()
            except (EOFError, KeyboardInterrupt):
                return "0"
            return choice
        else:
            return input("\n\033[96mJARVIS> \033[0mEnter your choice [0-39]: ").strip()

    def jarvis_say(self, message, style="info"):
        """Print a JARVIS-style message."""
        styles = {
            "info": "bright_cyan",
            "success": "bright_green",
            "error": "bright_red",
            "warning": "yellow",
            "ai": "bright_magenta",
        }
        if RICH_AVAILABLE:
            color = styles.get(style, "bright_cyan")
            self.console.print(f"[{color}][Jarvis]:[/{color}] [white]{message}[/white]")
        else:
            color_map = {
                "info": "\033[96m", "success": "\033[92m", "error": "\033[91m",
                "warning": "\033[93m", "ai": "\033[95m"
            }
            c = color_map.get(style, "\033[96m")
            print(f"{c}[Jarvis]: \033[0m{message}")

    def section_header(self, title):
        """Print a section divider with title."""
        if RICH_AVAILABLE:
            self.console.print()
            self.console.print(Panel(f"[bold bright_cyan]{title}[/bold bright_cyan]", border_style="cyan"))
        else:
            print(f"\n\033[96m{'─'*50}\n  {title}\n{'─'*50}\033[0m")

    def print_table(self, headers, rows, title=""):
        """Render a rich table."""
        if RICH_AVAILABLE:
            table = Table(title=title, box=box.SQUARE, border_style="cyan", header_style="bold bright_cyan")
            for h in headers:
                table.add_column(h, style="bright_white")
            for row in rows:
                table.add_row(*[str(c) for c in row])
            self.console.print(table)
        else:
            print(" | ".join(headers))
            print("-" * 60)
            for row in rows:
                print(" | ".join(str(c) for c in row))

    def prompt_input(self, message):
        """Styled input prompt."""
        if RICH_AVAILABLE:
            self.console.print(f"[cyan]>[/cyan] [bright_white]{message}[/bright_white]: ", end="")
        else:
            print(f"\033[96m> \033[0m{message}: ", end="")
        try:
            return input("").strip()
        except (EOFError, KeyboardInterrupt):
            return ""

    def pause(self):
        """Pause and wait for Enter."""
        try:
            input("\n\033[2m[Press Enter to return to menu...]\033[0m")
        except (EOFError, KeyboardInterrupt):
            pass

    def show_spinner(self, message, duration=2):
        """Show a spinner animation."""
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(style="cyan"),
                TextColumn(f"[cyan]{message}"),
                console=self.console,
                transient=True
            ) as progress:
                task = progress.add_task(message, total=None)
                time.sleep(duration)
        else:
            print(f"\033[96m[*] {message}...\033[0m")
            time.sleep(duration)

    def success(self, msg):
        self.jarvis_say(msg, "success")

    def error(self, msg):
        self.jarvis_say(msg, "error")

    def warning(self, msg):
        self.jarvis_say(msg, "warning")

    def ai_say(self, msg):
        self.jarvis_say(msg, "ai")
