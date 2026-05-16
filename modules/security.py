"""
modules/security.py - ALPHA JARVIS Security Module
Password generation, file encryption, and security utilities.
"""

import os
import secrets
import string
import base64
import hashlib
from datetime import datetime

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

KEYS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai")


class SecurityModule:
    def __init__(self, display, logger):
        self.display = display
        self.logger = logger
        os.makedirs(KEYS_DIR, exist_ok=True)

    # ── 16. Password Generator ──────────────────────────────────────────────

    def password_generator(self):
        self.display.section_header("[16] Password Generator")
        self.display.jarvis_say("Cryptographic password forge activated.")

        length = self.display.prompt_input("Password length (default: 20)")
        try:
            length = int(length)
        except (ValueError, TypeError):
            length = 20
        length = max(8, min(length, 128))

        count = self.display.prompt_input("Number of passwords to generate (default: 5)")
        try:
            count = int(count)
        except (ValueError, TypeError):
            count = 5
        count = max(1, min(count, 50))

        self.display.rprint("\n  [bright_cyan]Include:[/bright_cyan]")
        use_upper = self.display.prompt_input("Uppercase letters? (y/n, default: y)").lower() != "n"
        use_lower = self.display.prompt_input("Lowercase letters? (y/n, default: y)").lower() != "n"
        use_digits = self.display.prompt_input("Digits? (y/n, default: y)").lower() != "n"
        use_symbols = self.display.prompt_input("Symbols? (y/n, default: y)").lower() != "n"

        # Build character set
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            chars = string.ascii_letters + string.digits

        self.display.rprint()
        rows = []
        for i in range(count):
            password = "".join(secrets.choice(chars) for _ in range(length))
            strength = self._calc_strength(password)
            rows.append([str(i + 1), password, strength])

        self.display.print_table(["#", "Password", "Strength"], rows, "Generated Passwords")

        # Hash display
        show_hash = self.display.prompt_input("Show hash of first password? (y/n)")
        if show_hash.lower() == "y" and rows:
            pw = rows[0][1]
            md5 = hashlib.md5(pw.encode()).hexdigest()
            sha256 = hashlib.sha256(pw.encode()).hexdigest()
            self.display.rprint(f"\n  [cyan]MD5:[/cyan]    [dim]{md5}[/dim]")
            self.display.rprint(f"  [cyan]SHA256:[/cyan] [dim]{sha256}[/dim]")

        self.logger.log_activity(f"Generated {count} passwords of length {length}")

    def _calc_strength(self, password):
        score = 0
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*()_+-=[]{}|" for c in password): score += 1
        if len(password) >= 16: score += 1
        if len(password) >= 24: score += 1
        labels = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong", 5: "Very Strong", 6: "Excellent"}
        return labels.get(score, "Strong")

    # ── 17. File Encryption ─────────────────────────────────────────────────

    def file_encryption(self):
        self.display.section_header("[17] File Encryption")
        self.display.jarvis_say("Fernet encryption module initialized.")

        if not CRYPTO_AVAILABLE:
            self.display.error("cryptography library not installed.")
            self.display.jarvis_say("Fix: pip install cryptography")
            return

        choice = self.display.prompt_input(
            "1=Encrypt file, 2=Decrypt file, 3=Generate key, 4=Encrypt text, 5=Decrypt text"
        )

        if choice == "3":
            self._generate_key()
        elif choice == "1":
            self._encrypt_file()
        elif choice == "2":
            self._decrypt_file()
        elif choice == "4":
            self._encrypt_text()
        elif choice == "5":
            self._decrypt_text()

    def _generate_key(self):
        key = Fernet.generate_key()
        key_path = os.path.join(KEYS_DIR, f"jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.key")
        with open(key_path, "wb") as f:
            f.write(key)
        os.chmod(key_path, 0o600)
        self.display.success(f"Encryption key generated: {key_path}")
        self.display.warning("IMPORTANT: Keep this key secure. Losing it means losing your data.")
        self.logger.log_activity(f"Encryption key generated: {key_path}")
        return key_path, key

    def _load_key(self):
        """Load a Fernet key from file."""
        key_path = self.display.prompt_input("Path to key file (blank = generate new)")
        if not key_path:
            path, key = self._generate_key()
            return key
        if not os.path.exists(key_path):
            self.display.error("Key file not found.")
            return None
        with open(key_path, "rb") as f:
            return f.read()

    def _encrypt_file(self):
        filepath = self.display.prompt_input("File to encrypt")
        if not filepath or not os.path.exists(filepath):
            self.display.error("File not found.")
            return
        key = self._load_key()
        if not key:
            return
        f = Fernet(key)
        with open(filepath, "rb") as file:
            data = file.read()
        encrypted = f.encrypt(data)
        out_path = filepath + ".enc"
        with open(out_path, "wb") as file:
            file.write(encrypted)
        self.display.success(f"Encrypted: {out_path}")
        self.logger.log_activity(f"File encrypted: {filepath}")

    def _decrypt_file(self):
        filepath = self.display.prompt_input("File to decrypt (.enc)")
        if not filepath or not os.path.exists(filepath):
            self.display.error("File not found.")
            return
        key = self._load_key()
        if not key:
            return
        try:
            f = Fernet(key)
            with open(filepath, "rb") as file:
                data = file.read()
            decrypted = f.decrypt(data)
            out_path = filepath.replace(".enc", ".dec")
            with open(out_path, "wb") as file:
                file.write(decrypted)
            self.display.success(f"Decrypted: {out_path}")
            self.logger.log_activity(f"File decrypted: {filepath}")
        except Exception as e:
            self.display.error(f"Decryption failed: {e} (wrong key?)")

    def _encrypt_text(self):
        text = self.display.prompt_input("Text to encrypt")
        if not text:
            return
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted = f.encrypt(text.encode())
        self.display.rprint(f"\n[cyan]Key:[/cyan]       [bright_green]{key.decode()}[/bright_green]")
        self.display.rprint(f"[cyan]Encrypted:[/cyan] [bright_green]{encrypted.decode()}[/bright_green]")
        self.display.warning("Save the key! You need it to decrypt.")

    def _decrypt_text(self):
        key_str = self.display.prompt_input("Encryption key")
        encrypted_str = self.display.prompt_input("Encrypted text")
        if not key_str or not encrypted_str:
            return
        try:
            f = Fernet(key_str.encode())
            decrypted = f.decrypt(encrypted_str.encode())
            self.display.success(f"Decrypted: {decrypted.decode()}")
        except Exception as e:
            self.display.error(f"Decryption failed: {e}")
