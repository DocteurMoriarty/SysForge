import sys
from app.gui.gui import Gui
from app.run import Run
from app.utils.system import is_admin, get_os_info


def main():
    os_info = get_os_info()

    if os_info["system"] in ("Linux", "Darwin"):
        if not is_admin():
            raise PermissionError("This program must be run as root (sudo).")

    selection = Gui().run()
    if selection is None:
        return 1
    if selection:
        print(f"\nProfil: {selection['user']}")
        print("\nModules sélectionnés:")
        for cat, items in selection['modules'].items():
            if items:
                print(f"  • {cat}: {', '.join(items)}")



    run = Run()

    for _, items in selection.items():
        if items:
            run.multi_soft(*items)

    print(run)
    return 0
