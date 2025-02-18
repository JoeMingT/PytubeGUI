import tkinter as tk

_DEFAULT_PAD_X = 10
_DEFAULT_PAD_Y = 10

_HEADING_FAMILY = "Ubuntu"
_PARAGRAPH_FAMILY = "Arial"
_H1_FONT = (_HEADING_FAMILY, 23, "bold")
_H2_FONT = (_HEADING_FAMILY, 18, "bold")
_H3_FONT = (_HEADING_FAMILY, 14, "bold")
_P_FONT = (_PARAGRAPH_FAMILY, 14)

_THEME_FILE_LOCATION = "./themes/lavender.json"


def get_curr_screen_geometry():
    """
    Workaround to get the size of the current screen in a multi-screen setup.

    Returns:
        geometry (str): The standard Tk geometry string.
            [width]x[height]+[left]+[top]
    """
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    root.destroy()
    return geometry

_SCREEN_WIDTH, _SCREEN_HEIGHT = list(map(int, get_curr_screen_geometry().split('+')[0].split('x')))

