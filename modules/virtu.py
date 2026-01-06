# Imports
import subprocess
from typing import List


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
        self.__packages: List[str] = [
            "docker.io",
            "docker-compose",
            "docker-doc",
            "podman-docker",
            "containerd",
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

    def delete_packages(
            self
    ) -> None:
        """
        Remove all installed packages from the list.

        This method checks which packages are installed using `dpkg -s`
        and removes them using `apt remove -y`.

        Notes:
            - This script must be run as root (sudo) to remove packages.
        """
        installed_packages = []
        for pkg in self.packages:
            result = subprocess.run(
                ["dpkg", "-s", pkg],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                installed_packages.append(pkg)

        if installed_packages:
            subprocess.run(
                ["apt", "remove", "-y"] + installed_packages
            )
        else:
            print("No packages to remove.")

    def run_command(
        self,
        command: List[str],
        check=True
    ):
        """Run a shell command safely."""
        subprocess.run(command, check=check)

    def setup_docker_repository(
        self
    ):
        """Add Docker's official GPG key and repository on Debian."""
        self.run_command(["apt", "update"])
        self.run_command(["apt", "install", "-y", "ca-certificates", "curl"])
        self.run_command(["install", "-m", "0755", "-d", "/etc/apt/keyrings"])
        self.run_command([
            "curl", "-fsSL",
            "https://download.docker.com/linux/debian/gpg",
            "-o", "/etc/apt/keyrings/docker.asc"
        ])
        self.run_command(["chmod", "a+r", "/etc/apt/keyrings/docker.asc"])
        result = subprocess.run(
            ["/bin/sh", "-c", ". /etc/os-release && echo $VERSION_CODENAME"],
            capture_output=True,
            text=True,
            check=True
        )
        codename = result.stdout.strip()
        sources_content = f"""Types: deb
            URIs: https://download.docker.com/linux/debian
            Suites: {codename}
            Components: stable
            Signed-By: /etc/apt/keyrings/docker.asc
        """
        with open("/etc/apt/sources.list.d/docker.sources", "w") as f:
            f.write(sources_content)
        self.run_command(["apt", "update"])
