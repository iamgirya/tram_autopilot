import keyboard
import mouse
import pyautogui
import win32api, win32con
from time import sleep


# while True:
#     keyboard.wait("1")
#     keyboard.write("\n The key '1' was pressed!")
def move_mouse(dx, dy):
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE,
        dx,
        dy,
        0,
        0,
    )


def set_up_camera():
    sleep(1)
    keyboard.press("3")
    sleep(0.15)
    keyboard.press("space")
    keyboard.press("space")
    sleep(0.3)
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


set_up_camera()
