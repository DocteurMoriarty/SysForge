import subprocess
from typing import List

class LanguagesSoftware:

    def rust_packages(self) -> List[str]:
        """
        Retourne la liste des packages Rust à installer.
        """
        return [
            "cargo",
            "rustc",
            "rustfmt",
            "clippy",
            "rust-analyzer"
        ]

    def install_rust(self, default: bool = True) -> None:
        """
        Installe Rust via rustup et configure les packages par défaut.

        Args:
            default (bool): si True, installe les packages 'rust_packages'.
        """
        try:
            subprocess.run(
                ["curl", "--proto", "=https", "--tlsv1.2", "-sSf", "https://sh.rustup.rs"],
                check=True
            )
            subprocess.run(["sh", "sh.rustup.rs", "-y"], check=True)
            
            if default:
                for pkg in self.rust_packages():
                    subprocess.run(["cargo", "install", pkg], check=True)
        except subprocess.CalledProcessError as e:
            print({e})


    def php_packages(self) -> List[str]:
        """
        Returns the list of PHP packages to install.

        Returns:
            List[str]: A list of PHP package names.
        """
        return [
            "php",
            "php-cli",
            "php-fpm",
            "php-mysql",
            "php-xml",
            "php-curl",
            "php-mbstring",
            "php-zip",
            "php-gd"
        ]

    def install_php(self, default: bool = True) -> None:
        """
        Installs PHP and optional default PHP packages.

        Args:
            default (bool): If True, installs all packages returned by php_packages().
        """
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)

            if default:
                for pkg in self.php_packages():
                    subprocess.run(["sudo", "apt", "install", "-y", pkg], check=True)
                
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during PHP installation: {e}")
