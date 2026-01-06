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
    """UI moderne avec design épuré et sélection des modules."""

    def __init__(self):
        super().__init__()
        self._USER: str | None = None
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
            "VIRTUALISATION": [False],
            "NAVIGATEUR": [False],
            "SECURITE": [False],
            "RESEAU": [False],
            "OUTILS": [False],
            "SERVICES": [False],
        }

    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }
    
    #main_container {
        width: 80;
        height: 90vh;
        background: $panel;
        border: thick $primary;
        border-title-align: center;
    }
    
    #header {
        height: auto;
        width: 100%;
        padding: 1 2;
        background: $primary-background;
        border-bottom: solid $primary;
    }
    
    #title {
        text-style: bold;
        color: $text;
        text-align: center;
        padding-bottom: 1;
    }
    
    #user_section {
        height: auto;
        width: 100%;
        padding: 1 2;
        align: center middle;
    }
    
    #user_select {
        width: auto;
        height: auto;
        background: $surface;
        border: solid $accent;
        padding: 0 1;
    }
    
    RadioButton {
        padding: 0 2;
    }
    
    #content {
        width: 100%;
        height: 1fr;
        padding: 2;
        background: $surface;
    }
    
    Collapsible {
        width: 100%;
        margin-bottom: 1;
        border: solid $accent;
        background: $panel;
    }
    
    Collapsible > Contents {
        padding: 1 2;
    }
    
    Checkbox {
        margin: 0;
        padding: 0;
    }
    
    #footer {
        height: auto;
        width: 100%;
        padding: 1 2;
        align: center middle;
        background: $panel;
        border-top: solid $primary;
    }
    
    #go {
        width: 30;
        min-width: 20;
        background: $success;
        color: $text;
        border: none;
    }
    
    #go:hover {
        background: $success-darken-1;
    }
    
    #go:focus {
        background: $success-darken-2;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="main_container"):
            with Vertical(id="header"):
                yield Static("🔧 Configuration des Modules", id="title")
                
                with Horizontal(id="user_section"):
                    rs = RadioSet(id="user_select")
                    rs.border_title = "Type d'utilisateur"
                    rs._add_child(RadioButton("👤 CLIENT", id="rb_client", value=True))
                    rs._add_child(RadioButton("🖥️  SERVER", id="rb_server"))
                    yield rs

            with VerticalScroll(id="content"):
                self.checkboxes: Dict[str, List[Checkbox]] = {}
                
                for category, items in self.__MODULES.items():
                    with Container(classes="category_container"):
                        yield Static(f"📦 {category}", classes="category_title")
                        
                        with Vertical(classes="checkbox_container"):
                            self.checkboxes[category] = []
                            defaults = self.__DEFAULT.get(category, [False] * len(items))
                            if len(defaults) < len(items):
                                defaults = defaults + [False] * (len(items) - len(defaults))
                            
                            for i, item in enumerate(items):
                                cb = Checkbox(label=str(item), value=defaults[i])
                                self.checkboxes[category].append(cb)
                                yield cb

            with Container(id="footer"):
                yield Button("✓ Valider la sélection", id="go", variant="success")

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
            result = {
                "user": self._USER,
                "modules": selection
            }
            self.exit(result)


if __name__ == "__main__":
    app = Gui()
    result = app.run()
    
    print(f"\nProfil: {result['user']}")
    print("Modules sélectionnés:")
    for cat, items in result['modules'].items():
        if items:
            print(f"  {cat}: {', '.join(items)}")