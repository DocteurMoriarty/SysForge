from app.core.privileges import Privileges
import os
import subprocess
import tempfile
import time
import shutil


class SecuritySoftware:
    def __init__(
        self
    ) -> None:
        pass
        self.priv = Privileges()

    def install_nmap(
        self
    ) -> None:
        """Install Nmap security software."""
        print("[+] Installing Nmap...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "nmap"])
        print("[OK] Nmap installed successfully.")
    
    def install_wireshark(
        self
    ) -> None:
        """Install Wireshark security software."""
        print("[+] Installing Wireshark...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "wireshark"])
        print("[OK] Wireshark installed successfully.")
    
    def install_ufw(
        self
    ) -> None:
        """Install UFW firewall software."""
        print("[+] Installing UFW...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "ufw"])
        print("[OK] UFW installed successfully.")

    def install_fail2ban(
        self
    ) -> None:
        """Install Fail2Ban security software."""
        print("[+] Installing Fail2Ban...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "fail2ban"])
        print("[OK] Fail2Ban installed successfully.")
    
    def install_clamav(
        self
    ) -> None:
        """Install ClamAV antivirus software."""
        print("[+] Installing ClamAV...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "clamav", "clamav-daemon"])
        print("[OK] ClamAV installed successfully.")

    def install_rkhunter(
        self
    ) -> None:
        """Install Rkhunter rootkit detection software."""
        print("[+] Installing Rkhunter...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "rkhunter"])
        print("[OK] Rkhunter installed successfully.")
    
    def install_lynis(
        self
    ) -> None:
        """Install Lynis security auditing software."""
        print("[+] Installing Lynis...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "lynis"])
        print("[OK] Lynis installed successfully.")
    
    def install_chkrootkit(
        self
    ) -> None:
        """Install Chkrootkit rootkit detection software."""
        print("[+] Installing Chkrootkit...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "chkrootkit"])
        print("[OK] Chkrootkit installed successfully.")
    
    def install_openvas(
        self
    ) -> None:
        """Install OpenVAS vulnerability scanner."""
        print("[+] Installing OpenVAS...")
        self.priv.exec(["apt", "update"])
        self.priv.exec(["apt", "install", "-y", "openvas"])
        print("[OK] OpenVAS installed successfully.")
