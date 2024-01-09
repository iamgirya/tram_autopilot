import cv2
import numpy as np
import datetime
from PIL import ImageGrab
import time

time.process_time()


def wait(sec):
    t = time.process_time()
    while True:
        if time.process_time() - t > sec:
            break


def main_loop():
    t = time.process_time()
    while True:
        window = cv2.cvtColor(
            np.array(ImageGrab.grab(bbox=(0, 50, 1280, 720))), cv2.COLOR_BGR2RGB
        )
        # print(time.process_time() - t)
        t = time.process_time()

        print(get_speed(window))

        # cv2.imshow("frame", cv2.cvtColor(window, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


def get_speed(img):
    height, width, _ = img.shape

    speed_frame = img[
        int(height / 1.52) : int(height / 1.52) + 85,
        int(width / 1.93) : int(width / 1.93) + 60,
    ]
    acceleration_img = speed_frame

    lower_red = np.array([100, 222, 222])
    upper_red = np.array([235, 245, 245])
    speed_hist = cv2.inRange(speed_frame, lower_red, upper_red)
    speed_img = cv2.bitwise_and(speed_frame, speed_frame, mask=speed_hist)
    speed_img = cv2.cvtColor(speed_img, cv2.COLOR_RGB2GRAY)

    count = 0
    for i in range(speed_img.shape[0]):
        for j in range(speed_img.shape[1]):
            if speed_img[i][j] != 0:
                count += 1

    count *= 0.2675

    cv2.imshow("speed", speed_frame)
    cv2.imshow("speed_detected", speed_img)
    return count
    # while True:
    #     cv2.imshow("acceleration", acceleration_img)
    #     if cv2.waitKey(1) & 0xFF == ord("q"):
    #         cv2.destroyAllWindows()
    #         break


# test = cv2.imread("test_lesser_50.png")
# get_speed(test)
# test = cv2.imread("test_30.png")
# get_speed(test)
# test = cv2.imread("test_salon.png")
# get_speed(test)

main_loop()
