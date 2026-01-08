# Imports
from typing import List
import re, requests, subprocess, os
from pathlib import Path

class Browser:
    
    def __init__(self) -> None:
        self.__TOR_BASE = "https://dist.torproject.org/torbrowser/"

    def run(self, cmd, check=True) -> None:
        subprocess.run(cmd, check=check)

    def browser_choice(
        self, 
        browsers: List[str]
    ) -> None:
        for browser in browsers:
            match browser:
                case "tor_browser":
                    return self.tor_browser()
                case "firefox":
                    return self.firefox_browser()
                case "min":
                    return self.min_browser()
                case "brave":
                    return self.brave_browser()
                case "mullvad":
                    return self.mullvad_browser()
                case "palemoon":
                    return self.palemoon_browser()
                case "waterfox":
                    return self.waterfox_browser()
                case "librewolf":
                    return self.librewolf_browser()
                
    def tor_browser(
        self
    ) -> None:
        pass

    def firefox_browser(
        self
    ) -> None:
        pass

    def min_browser(
        self
    ) -> None:
        pass

    def brave_browser(
        self
    ) -> None:
        pass    
    
    def mullvad_browser(
        self
    ) -> None:
        pass

    def palemoon_browser(
        self
    ) -> None:
        pass
    def waterfox_browser(
        self
    ) -> None:
        pass

    def librewolf_browser(
        self
    ) -> None:
        pass

    def get_latest_tor_version(self) -> str:
        r = requests.get(self.__TOR_BASE, timeout=10)
        r.raise_for_status()
        versions = re.findall(r'href="(\d+\.\d+\.\d+)/"', r.text)
        if not versions:
            raise RuntimeError("Unable to detect Tor Browser versions")
        versions.sort(key=lambda v: list(map(int, v.split("."))))
        return versions[-1]