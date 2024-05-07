from windows_capture import WindowsCapture, Frame, InternalCaptureControl
from time import sleep, time
import numpy as np
import cv2
import yolo_predict


def main_loop():
    # 0. Инициализация
    model = yolo_predict.init_yolo()

    cap = cv2.VideoCapture(r".\datasets\video21_cut.mp4", cv2.CAP_ANY)

    while True:
        ret, frameg = cap.read()
        if not ret:
            exit()
        world, yolo_frame = yolo_predict.use_yolo_with_model(frameg, model, True)
        cv2.imshow("yolo_frame", yolo_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


# Код
main_loop()
