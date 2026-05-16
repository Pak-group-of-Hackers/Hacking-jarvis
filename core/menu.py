"""
core/menu.py - ALPHA JARVIS Menu Router
Routes numbered menu selections to the appropriate modules.
"""

import os
import sys


class Menu:
    def __init__(self, display, logger, sysinfo):
        self.display = display
        self.logger = logger
        self.sysinfo = sysinfo

        # Lazy imports (modules loaded on demand)
        self._network = None
        self._system = None
        self._ai_engine = None
        self._tools = None
        self._security = None

    # ── Module Loaders ──────────────────────────────────────────────────────

    @property
    def network(self):
        if not self._network:
            from modules.network import NetworkModule
            self._network = NetworkModule(self.display, self.logger)
        return self._network

    @property
    def system(self):
        if not self._system:
            from modules.system import SystemModule
            self._system = SystemModule(self.display, self.logger, self.sysinfo)
        return self._system

    @property
    def ai_engine(self):
        if not self._ai_engine:
            from modules.ai_engine import AIEngine
            self._ai_engine = AIEngine(self.display, self.logger)
        return self._ai_engine

    @property
    def tools(self):
        if not self._tools:
            from modules.tools import ToolsModule
            self._tools = ToolsModule(self.display, self.logger)
        return self._tools

    @property
    def security(self):
        if not self._security:
            from modules.security import SecurityModule
            self._security = SecurityModule(self.display, self.logger)
        return self._security

    # ── Main Router ─────────────────────────────────────────────────────────

    def handle_choice(self, choice: str):
        """Route menu choice to correct handler."""
        self.logger.log_activity(f"Menu selection: [{choice}]")

        handlers = {
            "1":  self.network.network_scan,
            "2":  self.system.update_kali,
            "3":  self.tools.open_wireshark,
            "4":  self.ai_engine.ai_prompt_mode,
            "5":  self.system.show_system_info,
            "6":  self.tools.open_nmap,
            "7":  self.network.vulnerability_scan,
            "8":  self.network.port_scanner,
            "9":  self.network.website_info,
            "10": self.network.ip_tracker,
            "11": self.network.dns_lookup,
            "12": self.network.ping_test,
            "13": self.network.connected_devices,
            "14": self.tools.open_metasploit,
            "15": self.tools.open_burp_suite,
            "16": self.security.password_generator,
            "17": self.security.file_encryption,
            "18": self.system.logs_viewer,
            "19": self.system.process_monitor,
            "20": self.system.ram_cpu_monitor,
            "21": self.network.internet_speed_test,
            "22": self.network.mac_address_changer,
            "23": self.network.network_traffic_monitor,
            "24": self.tools.screenshot_tool,
            "25": self.tools.webcam_checker,
            "26": self.network.bluetooth_scanner,
            "27": self.network.firewall_status,
            "28": self.network.start_vpn,
            "29": self.ai_engine.ai_code_generator,
            "30": self.ai_engine.ai_error_solver,
            "31": self.system.notes_memory,
            "32": self.system.auto_maintenance,
            "33": self.tools.open_terminal,
            "34": self.tools.custom_script_runner,
            "35": self.tools.toggle_dark_mode,
            "36": self.tools.tool_installer,
            "37": self.system.package_fixer,
            "38": self.system.backup_system,
            "39": self.system.about_owner,
        }

        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except KeyboardInterrupt:
                self.display.warning("Operation cancelled by user.")
            except Exception as e:
                self.logger.log_error(f"Error in menu [{choice}]: {e}")
                self.display.error(f"An error occurred: {e}")
            self.display.pause()
        else:
            self.display.warning(f"Invalid choice: '{choice}'. Please enter a number between 0 and 39.")
