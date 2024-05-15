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


def open_body_view():
    press("2")


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


camera_level = 0


def look_up():
    global camera_level
    if camera_level != 1:
        mouse.right_click()
        move_mouse(0, -200)
        mouse.right_click()
        camera_level += 1


def look_down():
    global camera_level
    if camera_level != -1:
        mouse.right_click()
        move_mouse(0, 200)
        mouse.right_click()
        camera_level -= 1


autopilot_work = True


def change_autopilot_state():
    global autopilot_work
    autopilot_work = not autopilot_work
    print("autopilot_work = " + str(autopilot_work))


def init_output():
    keyboard.add_hotkey("ctrl+w", lambda: set_up_camera())
    keyboard.add_hotkey("ctrl+s", lambda: change_autopilot_state())
