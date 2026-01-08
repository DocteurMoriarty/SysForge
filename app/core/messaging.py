import subprocess
from pathlib import Path
import requests
from app.core.privileges import Privileges

class MessagingInstallerDEB:
    """
    Base class for messaging application installers using .deb packages.
    """

    def __init__(
        self
    ) -> None:
        self.download_path: Path = Path.home() / "messaging-latest.deb"
        self.download_url: str | None = None
        self.version: str | None = None
        self.priv = Privileges()

    def download_deb(
        self, 
        url: str, 
        download_url: Path
    ) -> None:
        """Download the .deb package from the specified URL."""
        if download_url is None:
            raise ValueError("Download URL not set. Run fetch_latest_***_deb() first.")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(self.download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def install_deb(
        self, 
        download_path: Path
    ) -> None:
        """Install the downloaded .deb package using apt/dpkg."""
        priv = Privileges()
        priv.exec(["apt", "-qq", "update"])
        priv.exec(["apt", "-qq", "install", "-y", "gdebi-core"])
        priv.exec(["gdebi", "-n", str(download_path)])

class SessionInstallerDEB(
    MessagingInstallerDEB
):

    def __init__(
        self
    ) -> None:
        """
        Initialize the installer for the latest Session version using the official .deb package.
        """
        super().__init__()
        self.version: str | None = None

    @property
    def latest_version(
        self
    ) -> str:
        """
        Returns the latest Session version fetched from GitHub.
        Raises an error if fetch_latest_version() has not been called yet.
        """
        if self.version is None:
            raise ValueError("Latest version not fetched yet. Call fetch_latest_session_deb() first.")
        return self.version

    def fetch_latest_session_deb(
        self
    ) -> None:
        """
        Fetch the latest Session version and .deb download URL from GitHub API
        and store them in self.version and self.download_url.
        """
        api_url = "https://api.github.com/repos/session-foundation/session-desktop/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        release = response.json()
        self.version = release["tag_name"].lstrip("v")

        for asset in release["assets"]:
            if asset["name"].endswith(".deb") and "linux-amd64" in asset["name"]:
                self.download_url = asset["browser_download_url"]
                break

        if not self.download_url:
            raise RuntimeError("No .deb package found in latest Session release")

    def apply(
        self
    ) -> None:
        """Full workflow: fetch latest version, download, and install."""
        print("======= Session DEB Installer =======")
        print("[+] Fetching latest Session .deb package info...")
        self.fetch_latest_session_deb()
        print("[+] Downloading .deb package...")
        self.download_deb(self.download_url, self.download_path)
        print("[OK] Package downloaded.")
        self.install_deb(self.download_path)
        print("[OK] Session installed successfully.")


class SignalInstallerDEB:
    def __init__(
        self
    ):
        super().__init__()
        self.priv = Privileges()
        self.version = None

    def add_repository(
        self
    ) -> None:
        """Add Signal's official APT repository and GPG key."""
        self.priv.exec([
            "bash", "-c",
            "wget -O- https://updates.signal.org/desktop/apt/keys.asc | gpg --dearmor > signal-desktop-keyring.gpg"
        ])
        self.priv.exec([
            "mv", "signal-desktop-keyring.gpg", "/usr/share/keyrings/signal-desktop-keyring.gpg"
        ])
        self.priv.exec([
            "bash", "-c",
            "wget -O signal-desktop.sources https://updates.signal.org/static/desktop/apt/signal-desktop.sources"
        ])
        self.priv.exec([
            "mv", "signal-desktop.sources", "/etc/apt/sources.list.d/signal-desktop.sources"
        ])
    
    def install(
        self
    ) -> None:
        """Install Signal Desktop from APT repository."""
        print("[+] Updating package database and installing Signal Desktop...")
        self.priv.exec(["apt", "-qq", "update"])
        self.priv.exec(["apt", "-qq", "install", "-y", "signal-desktop"])
        print("[OK] Signal Desktop installed.")

    def fetch_version(
        self
    ) -> str:
        """Fetch installed Signal Desktop version."""
        try:
            result = subprocess.run(
                ["dpkg-query", "-W", "-f=${Version}", "signal-desktop"],
                check=True,
                capture_output=True,
                text=True
            )
            self.version = result.stdout.strip()
            print(f"[+] Installed Signal version: {self.version}")
            return self.version
        except subprocess.CalledProcessError:
            raise RuntimeError("Could not determine installed Signal version")

    def apply(
        self
    ) -> None:
        """
        Full workflow: add repo, install key, update and install Signal,
        then fetch the latest version.
        """
        print("======= Signal Desktop Installer =======")
        self.add_repository()
        print("[OK] Repository and GPG key added.")
        self.install()
        print("[+] Installing Signal Desktop...")
        self.fetch_version()
        print(f"[OK] Signal Desktop installed successfully.")



class DiscordInstallerDEB(
    MessagingInstallerDEB
):

    def __init__(
        self
    ) -> None:
        """
        Initialize the installer for the latest Discord version using the official .deb package.
        """
        super().__init__()
        self.download_path = Path.home() / "discord-latest.deb"
        self.download_url = "https://discord.com/api/download?platform=linux&format=deb"
        self.priv = Privileges()

    def apply(
        self
    ) -> None:
        """Full workflow: download and install."""
        print("======= Discord DEB Installer =======")
        print("[+] Downloading .deb package...")
        self.download_deb(self.download_url, self.download_path)
        print("[OK] Package downloaded.")
        self.install_deb(self.download_path)
        print("[OK] Discord installed successfully.")