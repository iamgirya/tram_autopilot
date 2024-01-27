import win32gui
import win32con
import cv2
import numpy as np


def rgbint2rgbtuple(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255

    return (red, green, blue)


def get_tram_sim_frame():
    hwnd = win32gui.FindWindow(None, "TramSim  ")
    rect = win32gui.GetWindowRect(hwnd)
    title = win32gui.GetWindowText(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y

    dc = win32gui.GetWindowDC(hwnd)
    win32gui.ReleaseDC(hwnd, dc)
    frame = np.zeros((h, w, 3), np.uint8)
    for i in range(h // 4):
        for j in range(w // 4):
            color = rgbint2rgbtuple(win32gui.GetPixel(dc, j, i))
            # if color[0] != 0 or color[1] != 0 or color[2] != 0:
            #     print(1)
            frame[i][j] = color
    win32gui.ReleaseDC(hwnd, dc)
    cv2.imshow("lol", frame)
    cv2.waitKey(0)

    # эта штука очень медленная и постоянно ломается


# main_loop()
get_tram_sim_frame()
