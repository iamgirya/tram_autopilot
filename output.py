import keyboard
import mouse
import win32api, win32con
from time import sleep


def move_mouse(dx, dy):
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE,
        dx,
        dy,
        0,
        0,
    )


def press(key: str):
    # print(key)
    keyboard.press_and_release(key)


def long_press(key: str, time=0.1):
    # print(key)
    keyboard.press(key)
    sleep(time)
    keyboard.release(key)


def open_cabine_view():
    press("1")


def open_nose_view():
    press("3")


def set_up_camera():
    sleep(1)
    press("3")
    press("space")
    sleep(0.15)
    mouse.right_click()
    keyboard.press("up")
    sleep(0.67)
    keyboard.release("up")
    sleep(0.05)
    move_mouse(790, 0)
    keyboard.press("up")
    sleep(0.403)
    keyboard.release("up")
    move_mouse(1052, 0)
    sleep(0.05)
    mouse.right_click()


def init_output():
    keyboard.add_hotkey("ctrl+w", lambda: set_up_camera())
