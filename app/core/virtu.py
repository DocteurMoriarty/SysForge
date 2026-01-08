# Imports
import subprocess, os
from typing import List
from app.core.privileges import Privileges


class VirtualisationSoftware:
    """
    Manage virtualization-related software packages on Debian/Ubuntu systems.

    This class can check installed packages and remove them safely.
    """

    def __init__(
            self
    ) -> None:
        """
        Initialize the list of virtualization packages.
        """
        self.priv = Privileges()
        self.__packages: List[str] = [
            "docker.io",
            "docker-compose",
            "docker-doc",
            "podman-docker",
            "containerd",
            "docker-compose-v2",
            "runc"
        ]

    @property
    def packages(
        self
    ) -> List[str]:
        """
        Returns the list of packages managed by this class.

        Returns:
            List[str]: List of package names.
        """
        return self.__packages

    def delete_packages(self) -> None:
        installed_packages = []
        
        for pkg in self.packages:
            result = subprocess.run(
                ["dpkg", "-s", pkg],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                installed_packages.append(pkg)
        
        docker_io_packages = ["containerd.io", "docker-ce", "docker-ce-cli", "docker-buildx-plugin", "docker-compose-plugin"]
        for pkg in docker_io_packages:
            result = subprocess.run(
                ["dpkg", "-s", pkg],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                installed_packages.append(pkg)
        
        print(f"[+] Installed virtualization packages to remove: {installed_packages}")
        
        if installed_packages:
            self.priv.exec(["apt", "remove", "-y"] + installed_packages)
            self.priv.exec(["apt", "autoremove", "-y"])

    def run_command(
        self,
        command: List[str],
        check=True
    ) -> None:
        """Run a shell command safely."""
        subprocess.run(command, check=check)

    def setup_docker_repository(
        self
    ) -> None:
        """Add Docker's official GPG key and repository for Debian/Ubuntu and derivatives."""
        
        derivative_map = {
            "linuxmint": "ubuntu",
            "elementary": "ubuntu",
            "pop": "ubuntu",
            "zorin": "ubuntu",
            "kubuntu": "ubuntu",
            "xubuntu": "ubuntu",
            "lubuntu": "ubuntu",
            "ubuntukylin": "ubuntu",
            "debian": "debian",
            "ubuntu": "ubuntu"
        }

        codename_map = {
            "ulyana": "focal", "ulyssa": "focal", "uma": "focal", "una": "focal",
            "vanessa": "jammy", "vera": "jammy", "victoria": "jammy",
            "wilma": "noble",
            "hera": "focal",
            "juno": "focal",
            "odin": "jammy",
            "20.04": "focal",
            "22.04": "jammy",
            "16": "jammy",
        }

        result = subprocess.run(["/bin/sh", "-c", ". /etc/os-release && echo $ID"], capture_output=True, text=True, check=True)
        distro = result.stdout.strip().lower()
        official_distro = derivative_map.get(distro)
        print(f"[+] Detected distribution: {distro}, using official distro: {official_distro}")
        if official_distro is None:
            raise RuntimeError(f"Unsupported distribution for Docker repository setup: {distro}")

        result = subprocess.run(["/bin/sh", "-c", ". /etc/os-release && echo $VERSION_CODENAME"], capture_output=True, text=True, check=True)
        codename = result.stdout.strip().lower()

        if distro in ["linuxmint", "elementary", "pop", "zorin"]:
            codename = codename_map.get(codename, codename)
            print(f"[+] Remapped codename: {codename}")

        self.priv.exec([
            "curl", "-fsSL",
            f"https://download.docker.com/linux/{official_distro}/gpg",
            "-o", "/etc/apt/keyrings/docker.asc"
        ])
        self.priv.exec(["chmod", "a+r", "/etc/apt/keyrings/docker.asc"])

        sources_content = (
            f"Types: deb\n"
            f"URIs: https://download.docker.com/linux/{official_distro}\n"
            f"Suites: {codename}\n"
            f"Components: stable\n"
            f"Signed-By: /etc/apt/keyrings/docker.asc\n"
        )

        temp_path = "/tmp/docker.sources"
        with open(temp_path, "w") as f:
            f.write(sources_content)

        self.priv.exec(["mv", temp_path, "/etc/apt/sources.list.d/docker.sources"])
        self.priv.exec(["apt", "update"])
        print("[+] Docker repository setup complete.")


    def install_packages(self) -> None:
        """Install required virtualization packages."""
        print("[+] Installing virtualization packages...")
        self.priv.exec(["apt", "install", "-y"] + self.packages)
        print("[OK] Virtualization packages installed successfully.")



    def apply(
        self
    ) -> None:
        """
        Apply the virtualization software setup.

        This method currently sets up the Docker repository.
        """
        print("======= Virtualization Software Setup =======")
        self.delete_packages()
        print("[+] Setting up Docker repository...")
        self.setup_docker_repository()
        self.install_packages()
        print("[OK] Docker repository set up successfully.")
        