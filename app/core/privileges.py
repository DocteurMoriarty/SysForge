import os
import shutil
import subprocess
from typing import List


class Privileges:
    """
    Privilege escalation helper.

    Tries to obtain root privileges using sudo first,
    then falls back to su if sudo is not available or not permitted.
    """

    def __init__(self):
        self.is_root = os.geteuid() == 0
        self.has_sudo = shutil.which("sudo") is not None
        self.has_su = shutil.which("su") is not None

    def _check_sudo(self) -> bool:
        """
        Check if sudo can be used.
        """
        try:
            subprocess.run(
                ["sudo", "-v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _run(
        self,
        command: List[str],
        verbose: bool = False
    ) -> int:
        """
        Run a command with optional silent output.
        """
        stdout = None if verbose else subprocess.DEVNULL
        stderr = None if verbose else subprocess.DEVNULL

        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"

        return subprocess.call(
            command,
            stdout=stdout,
            stderr=stderr,
            env=env
        )

    def exec(
        self,
        command: List[str],
        verbose: bool = False
    ) -> int:
        """
        Execute a command with the best available privilege method.

        Priority:
        1. Already root
        2. sudo
        3. su
        """
        if self.is_root:
            return self._run(command, verbose)

        if self.has_sudo and self._check_sudo():
            return self._run(["sudo"] + command, verbose)

        if self.has_su:
            cmd = " ".join(command)
            return self._run(["su", "-c", cmd], verbose)

        raise PermissionError(
            "No privilege escalation method available (sudo or su required)"
        )
