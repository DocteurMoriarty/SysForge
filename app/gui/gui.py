# Imports
from __future__ import annotations
from typing import Dict, List
from textual.app import App, ComposeResult
from textual.widgets import Static, Checkbox, Button, RadioSet, RadioButton, Collapsible
from textual.containers import VerticalScroll, Vertical, Horizontal, Container


def as_text(label) -> str:
    """Normalise le label de Checkbox en str (évite TypeError au join)."""
    if isinstance(label, str):
        return label
    plain = getattr(label, "plain", None)
    if isinstance(plain, str):
        return plain
    return str(label)


class Gui(App):
    """UI épurée et simple avec collapsibles."""

    def __init__(self):
        super().__init__()
        self._USER: str | None = "CLIENT"
        self.__MODULES: Dict[str, List[str]] = {
            "VIRTUALISATION": [
                "Docker",
                "Podman",
            ],
            "NAVIGATEUR": [
                "Tor Browser",
                "Firefox",
                "Waterwolf",
                "Librewolf",
                "Min Browser",
                "Brave",
                "Mullvad",
                "Palemoon",
            ],
            "SECURITE": [
                "UFW",
                "Iptables",
                "Fail2ban",
                "AppArmor",
                "Auditd",
                "SELinux",
            ],
            "RESEAU": [
                "WireGuard",
                "OpenVPN",
                "Tor",
            ],
            "OUTILS": [
                "GnuPG",
                "KeePassXC",
                "HTop",
                "Curl",
                "Wget",
            ],
            "SERVICES": [
                "OpenSSH",
                "Nginx",
                "PostgreSQL",
                "MySQL",
                "MariaDB",
                "MongoDB",
                "GraphQL",
            ],
        }
        
        self.__DEFAULT: Dict[str, List[bool]] = {
            "VIRTUALISATION": [False, False],
            "NAVIGATEUR": [False, False, False, False, False, False, False, False],
            "SECURITE": [False, False, False, False, False, False],
            "RESEAU": [False, False, False],
            "OUTILS": [False, False, False, False, False],
            "SERVICES": [False, False, False, False, False, False, False],
        }

    CSS = """
    Screen {
        background: #1a1a1a;
    }
    
    #app {
        width: 100%;
        height: 100%;
        padding: 2 4;
    }
    
    #title {
        text-style: bold;
        color: #ffffff;
        text-align: center;
        padding: 1 0 2 0;
    }
    
    #user_section {
        width: 100%;
        height: auto;
        padding: 0 0 2 0;
        align: center middle;
    }
    
    #user_select {
        width: 50;
        border: solid #4a9eff;
    }
    
    RadioButton {
        padding: 0 1;
    }
    
    #content {
        width: 100%;
        height: 1fr;
    }
    
    Collapsible {
        width: 100%;
        background: #2a2a2a;
        border: solid #3a3a3a;
        margin-bottom: 1;
    }
    
    Collapsible:focus {
        border: solid #4a9eff;
    }
    
    Collapsible > Contents {
        padding: 1;
    }
    
    Checkbox {
        padding: 0 0 0 2;
    }
    
    #footer {
        width: 100%;
        height: auto;
        padding: 2 0 0 0;
        align: center middle;
    }
    
    #go {
        width: 40;
        background: #28a745;
        color: white;
    }
    
    #go:hover {
        background: #218838;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="app"):
            yield Static("⚙️  Configuration des Modules", id="title")
            
            with Horizontal(id="user_section"):
                rs = RadioSet(id="user_select")
                rs.border_title = "Profil"
                rs._add_child(RadioButton("CLIENT", id="rb_client", value=True))
                rs._add_child(RadioButton("SERVER", id="rb_server"))
                yield rs

            with VerticalScroll(id="content"):
                self.checkboxes: Dict[str, List[Checkbox]] = {}
                
                for category, items in self.__MODULES.items():
                    with Collapsible(title=category, collapsed=True):
                        self.checkboxes[category] = []
                        defaults = self.__DEFAULT.get(category, [False] * len(items))
                        if len(defaults) < len(items):
                            defaults = defaults + [False] * (len(items) - len(defaults))
                        
                        for i, item in enumerate(items):
                            cb = Checkbox(label=str(item), value=defaults[i])
                            self.checkboxes[category].append(cb)
                            yield cb

            with Container(id="footer"):
                yield Button("✓ Valider", id="go", variant="success")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        pressed = event.pressed
        if pressed is not None:
            label = getattr(pressed, "label", "")
            self._USER = "CLIENT" if "CLIENT" in str(label).upper() else "SERVER"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go":
            selection = {
                category: [as_text(cb.label) for cb in cbs if cb.value]
                for category, cbs in self.checkboxes.items()
            }
            result = {"user": self._USER, "modules": selection}
            self.exit(result)

