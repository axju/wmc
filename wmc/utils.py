"""Some useful tools"""
import sys
from time import sleep


def resize_window(size, wait=1):
    """Resize the current window"""
    sleep(wait)
    if sys.platform in ["win32", "win64"]:
        import win32gui
        hwnd = win32gui.GetForegroundWindow()
        win32gui.MoveWindow(hwnd, *size, True)

    elif sys.platform in ["linux", "linux2"]:
        import Xlib
        import Xlib.display
        display = Xlib.display.Display()
        root = display.screen().root
        wid = root.get_full_property(
            display.intern_atom("_NET_ACTIVE_WINDOW"),
            Xlib.X.AnyPropertyType,
        ).value[0]
        window = display.create_resource_object("window", wid)
        window.configure(
            x=size[0], y=size[1], width=size[2], height=size[3]
        )
        display.sync()
