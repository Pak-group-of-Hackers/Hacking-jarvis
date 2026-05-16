"""
utils/system_info.py - System information collector
"""

import os
import platform
import socket
from datetime import datetime, timedelta

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfo:
    def get_all(self) -> dict:
        return {
            "os": self._get_os(),
            "user": os.getenv("USER", os.getenv("USERNAME", "root")),
            "shell": os.getenv("SHELL", "bash").split("/")[-1],
            "date": datetime.now().strftime("%m-%d-%Y"),
            "time": datetime.now().strftime("%I:%M:%S %p"),
            "uptime": self._get_uptime(),
            "cpu": self._get_cpu(),
            "ram": self._get_ram(),
            "disk": self._get_disk(),
            "hostname": socket.gethostname(),
        }

    def _get_os(self):
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        return line.split("=")[1].strip().strip('"')
        return platform.system()

    def _get_uptime(self):
        if PSUTIL_AVAILABLE:
            boot = psutil.boot_time()
            delta = datetime.now() - datetime.fromtimestamp(boot)
            hours = int(delta.total_seconds() // 3600)
            minutes = int((delta.total_seconds() % 3600) // 60)
            return f"{hours}h {minutes}m"
        return "N/A"

    def _get_cpu(self):
        if PSUTIL_AVAILABLE:
            pct = psutil.cpu_percent(interval=0.1)
            return f"{pct}%"
        return "N/A"

    def _get_ram(self):
        if PSUTIL_AVAILABLE:
            mem = psutil.virtual_memory()
            used = mem.used / (1024 ** 3)
            total = mem.total / (1024 ** 3)
            return f"{used:.2f}GB / {total:.2f}GB"
        return "N/A"

    def _get_disk(self):
        if PSUTIL_AVAILABLE:
            disk = psutil.disk_usage("/")
            used = disk.used / (1024 ** 3)
            total = disk.total / (1024 ** 3)
            return f"{used:.0f}GB / {total:.0f}GB"
        return "N/A"

    def get_live_cpu(self):
        if PSUTIL_AVAILABLE:
            return psutil.cpu_percent(interval=1)
        return 0

    def get_live_ram(self):
        if PSUTIL_AVAILABLE:
            return psutil.virtual_memory()
        return None
