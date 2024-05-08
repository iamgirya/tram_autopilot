import cv2
import numpy as np
from PIL import ImageGrab
import time

time.process_time()


def wait(sec):
    t = time.process_time()
    while True:
        if time.process_time() - t > sec:
            break


# def main_loop():
#     t = time.process_time()
#     while True:
#         window = cv2.cvtColor(
#             np.array(ImageGrab.grab(bbox=(0, 50, 1280, 720))), cv2.COLOR_BGR2RGB
#         )

#         speed = get_speed(window)

#         # анализ картинки
#         # предсказание
#         # выбор действия

#         # cv2.imshow("frame", cv2.cvtColor(window, cv2.COLOR_BGR2RGB))
#         print(time.process_time() - t)
#         t = time.process_time()
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             cv2.destroyAllWindows()
#             break


def get_speed(frame):
    img = np.array(frame)
    if img.size == 0:
        return 0
    height, width, _ = img.shape

    height_const = 1.34
    width_const = 1.89

    speed_frame = img[
        int(height / height_const) : int(height / height_const) + 97,
        int(width / width_const) : int(width / width_const) + 90,
    ]

    lower_color = np.array([120, 200, 200])
    upper_color = np.array([220, 235, 235])
    speed_hist = cv2.inRange(speed_frame, lower_color, upper_color)
    speed_img = cv2.bitwise_and(speed_frame, speed_frame, mask=speed_hist)
    cv2.imshow("speed_hist", speed_img)
    speed_img = cv2.cvtColor(speed_img, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((2, 2), np.uint8)
    speed_img = cv2.morphologyEx(speed_img, cv2.MORPH_OPEN, kernel, iterations=2)
    kernel = np.ones((3, 3), np.uint8)
    speed_img = cv2.dilate(speed_img, kernel, iterations=1)
    cv2.imshow("speed_clear", speed_img)

    count = 0
    for i in range(speed_img.shape[0]):
        stop = (
            speed_img.shape[1]
            if i < speed_img.shape[0] // 2
            else speed_img.shape[1] // 2
        )
        for j in range(stop):
            if speed_img[i][j] != 0:
                count += 1

    count *= 0.2675
    count /= 4.0 * 10.0 / 7 * 3

    cv2.imshow("speed", speed_frame)

    rounded_count = float(round(count / 2) * 2)
    return rounded_count


# test = cv2.imread("test_lesser_50.png")
# get_speed(test)
# test = cv2.imread("test_30.png")
# get_speed(test)
# test = cv2.imread("test_salon.png")
# get_speed(test)

# main_loop()
