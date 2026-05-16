"""
core/logger.py - ALPHA JARVIS Logging System
"""

import os
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
ACTIVITY_LOG = os.path.join(LOG_DIR, "activity.log")
ERROR_LOG = os.path.join(LOG_DIR, "error.log")


class Logger:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)

        # Activity logger
        self.activity_logger = logging.getLogger("jarvis.activity")
        self.activity_logger.setLevel(logging.INFO)
        if not self.activity_logger.handlers:
            fh = logging.FileHandler(ACTIVITY_LOG)
            fh.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
            self.activity_logger.addHandler(fh)

        # Error logger
        self.error_logger = logging.getLogger("jarvis.error")
        self.error_logger.setLevel(logging.ERROR)
        if not self.error_logger.handlers:
            fh = logging.FileHandler(ERROR_LOG)
            fh.setFormatter(logging.Formatter("[%(asctime)s] ERROR: %(message)s", "%Y-%m-%d %H:%M:%S"))
            self.error_logger.addHandler(fh)

    def log_activity(self, message: str):
        self.activity_logger.info(message)

    def log_error(self, message: str):
        self.error_logger.error(message)

    def get_recent_activity(self, lines=50):
        return self._tail(ACTIVITY_LOG, lines)

    def get_recent_errors(self, lines=50):
        return self._tail(ERROR_LOG, lines)

    def _tail(self, filepath, n):
        try:
            if not os.path.exists(filepath):
                return []
            with open(filepath, "r") as f:
                return f.readlines()[-n:]
        except Exception:
            return []
