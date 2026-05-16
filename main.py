#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║         ALPHA JARVIS - AI Cybersecurity Assistant             ║
║         Version: 1.0.0 OFFLINE | Owner: USER MALIK           ║
╚═══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.display import Display
from core.menu import Menu
from core.logger import Logger
from utils.system_info import SystemInfo


def main():
    """Main entry point for ALPHA JARVIS."""
    logger = Logger()
    display = Display()
    sysinfo = SystemInfo()
    menu = Menu(display, logger, sysinfo)

    try:
        # Startup sequence
        display.clear_screen()
        display.show_boot_animation()
        display.show_banner()
        display.show_system_status(sysinfo)

        logger.log_activity("ALPHA JARVIS started successfully")

        # Main loop
        while True:
            display.show_menu()
            choice = display.get_choice()

            if choice == "0":
                display.jarvis_say("Shutting down. Goodbye, USER MALIK. Stay secure.")
                logger.log_activity("ALPHA JARVIS shutdown by user")
                time.sleep(1)
                display.clear_screen()
                break

            menu.handle_choice(choice)

    except KeyboardInterrupt:
        display.jarvis_say("Emergency shutdown initiated. Systems offline.")
        logger.log_activity("ALPHA JARVIS force-quit via KeyboardInterrupt")
        sys.exit(0)
    except Exception as e:
        logger = Logger()
        logger.log_error(f"Fatal error: {e}")
        print(f"\n[ERROR] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
