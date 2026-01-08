import sys
from app.gui.gui import Gui
from app.run import Run
from app.utils.system import is_admin, get_os_info


def main():
    print(get_os_info())

    selection = Gui().run()
    run       = Run()

    if selection is None:
        return 1
    if selection:
        run.user = selection['user']
        print(run)
        for cat, items in selection['modules'].items():
            if items:
                run.multi_soft(*items)
                print(run.soft)
        run.check_packages_install()
    return 0
