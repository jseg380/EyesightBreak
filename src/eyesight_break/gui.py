from __future__ import annotations

import tkinter
from random import choice as random_choice
from typing import Generator

from screeninfo import get_monitors

from .config import BREAKS, BreakType, WinConfig


def create_window(root: tkinter.Tk, geometry: dict[str, int], text: str, timer: Generator) -> tkinter.Toplevel:
    """Create a tkinter window that will be used as a skeleton for breaks.

    Args:
        root (tkinter.Tk): parent window (aka "the orchestrator")
        geometry (Dict[str, int]): size of the window to create
            {
                'width': width of screen in px,
                'height': height of the scren in px,
                'offset_x': monitor.x,
                'offset_y': monitor.y,
            }
        text (str): message to display in the window
        timer (Generator): generator object returned by a function with yield
            that counts down from a certain time to 0

    Returns:
        (tkinter.Toplevel): a child window of the root window passed as a parameter

    """
    win: tkinter.Toplevel = tkinter.Toplevel(root)
    win.title(WinConfig.title)
    win.config(bg=WinConfig.bg_color)

    width: int = geometry['width']
    height: int = geometry['height']
    off_x: int = geometry['offset_x']
    off_y: int = geometry['offset_y']
    win.geometry(f'{width}x{height}+{off_x}+{off_y}')

    # Message with the break advice (static)
    label_text: str = text
    label: tkinter.Label = tkinter.Label(
        win, text=label_text, font=WinConfig.font, fg=WinConfig.fg_color, bg=WinConfig.bg_color
    )
    label.place(relx=0.5, rely=0.44, anchor='center')

    # Message with the timer (dynamic)
    timer_label = tkinter.Label(
        win, text=next(timer), font=WinConfig.font, bg=WinConfig.bg_color, fg=WinConfig.fg_color
    )
    timer_label.place(relx=0.5, rely=0.50, anchor='center')

    def update_timer_label(timer: Generator) -> None:
        time_left = next(timer)

        # Timer ran out
        if time_left is None:
            root.destroy()
            return

        # Update new time left and issue the next update of the label
        timer_label.config(text=time_left)
        root.after(1000, update_timer_label, timer)

    update_timer_label(timer)

    # Setting the background color of the windows transparent
    # This code MUST be executed after setting the geometry to work properly
    win.wait_visibility(win)  # Needed for transparency to work in X11
    # These two lines must be after wait_visibility
    win.attributes('-alpha', WinConfig.alpha)
    win.attributes('-fullscreen', True)

    return win


def format_time(seconds: int) -> str:
    """Format time in seconds to minutes and seconds.

    Args:
        seconds (int): time in seconds

    Returns:
        (str): time formatted in MM:SS where MM is minutes and SS seconds

    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return f'{minutes:02}:{remaining_seconds:02}'


def timer(seconds: int) -> Generator:
    """Timer function to create a generator.

    Args:
        seconds (int): number of second the timer counts down to

    Returns:
        (Generator): when the timer is still up
        (None): when the timer rans out

    """
    n = seconds
    while n >= 0:
        yield format_time(n)
        n -= 1

    yield None


def show_break(break_type: BreakType) -> bool:
    """Show break in all windows.

    Args:
        break_type (BreakType): type of break to display

    Returns:
        (bool): True if the break was postponed, False otherwise

    """
    # Create root window, which is used as a puppeteer to control an undefined
    # number of windows painlessly
    root: tkinter.Tk = tkinter.Tk()
    # Hide root window, only used as a controller, does not display anything
    root.withdraw()
    # Control whether the break has been postponed or not
    postponed: bool = False

    # Function to close all windows
    def close_windows():
        root.destroy()

    # Skipping a break simply means closing the windows and continuing
    def skip_break(event=None):
        close_windows()

    # Postponing break, we have to inform of the postponing by returning True
    def postpone_break(event=None):
        nonlocal postponed
        postponed = True
        close_windows()

    message = random_choice(BREAKS[break_type].messages)

    for monitor in get_monitors():
        geometry = {
            'width': monitor.width,
            'height': monitor.height,
            'offset_x': monitor.x,
            'offset_y': monitor.y,
        }

        # message = random_choice(BREAKS[break_type].messages)

        timer_generator = timer(BREAKS[break_type].duration)

        # Create one window per monitor to cover all screens/monitors
        win = create_window(root, geometry, message, timer_generator)
        win.bind('<Escape>', skip_break)
        win.bind('<space>', postpone_break)

    root.mainloop()

    return postponed
