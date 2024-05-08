import keyboard
import mouse
import win32api, win32con
from time import sleep
from decision_module import TramState


def move_mouse(dx, dy):
    win32api.mouse_event(
        win32con.MOUSEEVENTF_MOVE,
        dx,
        dy,
        0,
        0,
    )


def press(key: str):
    print(key)
    keyboard.press_and_release(key)


def long_press(key: str, time=0.1):
    print(key)
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


acceleration_level = 0


def implementation_of_decision(state, speed):
    global acceleration_level
    lower_move_speed = 10
    upper_move_speed = 15

    if state == TramState.move:
        if lower_move_speed <= speed <= upper_move_speed:
            press("a")
            acceleration_level = 0
        elif lower_move_speed > speed and acceleration_level < 20:
            long_press("q")
            acceleration_level += 1
        elif speed > upper_move_speed:
            long_press("y")
            acceleration_level -= 1
    elif state == TramState.stop:
        if lower_move_speed <= speed:
            if acceleration_level > 0:
                press("a")
            long_press("y", 0.1)
            acceleration_level -= 2
        else:
            if acceleration_level < -10:
                press("a")
            else:
                long_press("y")
                acceleration_level -= 1
    elif state == TramState.wait:
        if speed > 0:
            long_press("y")
            acceleration_level -= 1
        else:
            press("a")
            acceleration_level = 0
    elif state == TramState.boarding:
        if speed > 0:
            long_press("y", 1)
            sleep(1)
        sleep(0.5)
        press("num 1")
        sleep(30)
        press("num 3")
        sleep(3)
        press("a")
        acceleration_level = 0
    elif state == TramState.fast_stop:
        # TODO аварийный тормоз заюзать?
        if speed != 0:
            if acceleration_level > 0:
                press("a")
                acceleration_level = 0
            long_press("y", 0.3)
            acceleration_level -= 6
        else:
            press("a")
            acceleration_level = 0

    print("acceleration_level = " + str(acceleration_level))
