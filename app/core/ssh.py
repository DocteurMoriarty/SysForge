import random
import subprocess
from pathlib import Path


class SSH:
    def __init__(self):
        self.__port: int = random.randint(9000, 65535)
        self.__config_d_dir = Path("/etc/ssh/sshd_config.d")
        self.__hardening_file = self.__config_d_dir / "99-hardening.conf"

    @property
    def port(self) -> int:
        return self.__port

    def install(self) -> None:
        """Install OpenSSH server if not installed."""
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "openssh-server"], check=True)

    def harden(self) -> None:
        """Apply SSH hardening in sshd_config.d"""
        subprocess.run(["sudo", "mkdir", "-p", str(self.__config_d_dir)], check=True)
        hardened_config = f"""
            # ==============================
            # SSH HARDENING CONFIGURATION
            # ==============================

            Port {self.__port}
            Protocol 2

            PermitRootLogin no
            PasswordAuthentication no
            ChallengeResponseAuthentication no
            UsePAM yes
            PubkeyAuthentication yes
            AuthenticationMethods publickey
            AllowUsers $USER

            MaxAuthTries 3
            LoginGraceTime 20
            PermitEmptyPasswords no
            X11Forwarding no
            AllowAgentForwarding no
            AllowTcpForwarding no
            PermitTunnel no

            Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
            MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
            KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org

            LogLevel VERBOSE

            ClientAliveInterval 300
            ClientAliveCountMax 2
            """

        if self.__hardening_file.exists():
            subprocess.run(["sudo", "cp", str(self.__hardening_file), f"{self.__hardening_file}.bak"], check=True)
        subprocess.run(["sudo", "tee", str(self.__hardening_file)], input=hardened_config, text=True, check=True)

    def restart(self) -> None:
        """Validate and restart SSH service."""
        subprocess.run(["sudo", "sshd", "-t"], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)

    def apply(self) -> None:
        """Install and harden SSH in one step."""
        self.install()
        self.harden()
        self.restart()

class SSHClient:
    def __init__(self, server_ip: str, port: int = 22, user: str = None):
        """
        Initialize SSH client connection parameters.

        Args:
            server_ip (str): The target SSH server IP or hostname.
            port (int): The SSH port (default: 22).
            user (str): The username to connect with. Defaults to current user.
        """
        self.server_ip = server_ip
        self.port = port
        self.user = user or Path.home().name 
        self.key_path = Path.home() / ".ssh" / "id_ed25519"

    def generate_key(
        self, 
        force: bool = False
    ) -> None:
        """
        Generate an Ed25519 SSH key pair for the client.

        Args:
            force (bool): If True, overwrite existing key pair.
        """
        if self.key_path.exists() and not force:
            return

        subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-f", str(self.key_path), "-N", ""],
            check=True
        )

    def copy_key_to_server(
        self
    ) -> None:
        """
        Copy the public key to the server for passwordless login.
        """
        subprocess.run(
            [
                "ssh-copy-id",
                "-i", str(self.key_path) + ".pub",
                "-p", str(self.port),
                f"{self.user}@{self.server_ip}"
            ],
            check=True
        )

    def test_connection(
        self
    ) -> None:
        """
        Test SSH connection using the key.
        """
        subprocess.run(
            [
                "ssh",
                "-i", str(self.key_path),
                "-p", str(self.port),
                f"{self.user}@{self.server_ip}",
                "echo 'SSH connection successful!'"
            ],
            check=True
        )

    def execute_command(
        self, 
        command: str
    ) -> None:
        """
        Execute a remote command on the SSH server.

        Args:
            command (str): Command string to execute remotely.
        """
        subprocess.run(
            [
                "ssh",
                "-i", str(self.key_path),
                "-p", str(self.port),
                f"{self.user}@{self.server_ip}",
                command
            ],
            check=True
        )
