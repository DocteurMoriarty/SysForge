# Imports
import sys
import os
from run import Run
from gui import Gui

if "__main__" == __name__:
    if os.name != 'nt':
        if os.getpid() != 0:
            raise PermissionError("This script must be run as root (sudo).")
    selection = Gui().run()
    if selection is None:
        sys.exit(1)

    run = Run()        

    for _, items in selection.items():
        if items:
            run.multi_soft(*items)


    print(run)

    sys.exit(1)
