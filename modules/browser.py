# Imports
from typing import List

class Browser:
    
    def __init__(self, browser: List[str]) -> None:
        self.__browsers: List[str] = browser
    
    def browser_choice(
        self, 
        browsers: List[str]
    ) -> function:
        for browser in browsers:
            match browser:
                case "tor":
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