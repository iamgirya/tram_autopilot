from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
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


def main_loop():
    t = time.process_time()

    model = YOLO("yolov8n.pt")
    while True:
        frame = cv2.cvtColor(
            np.array(ImageGrab.grab(bbox=(0, 50, 1280, 720 + 50))), cv2.COLOR_BGR2RGB
        )

        # speed = get_speed(window)
        results = model.predict(source=frame, save=False)  # save plotted images
        for r in results:
            annotator = Annotator(frame)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[
                    0
                ]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])
        annotatored_frame = annotator.result()

        scale_percent = 40  # percent of original size
        width = int(annotatored_frame.shape[1] * scale_percent / 100)
        height = int(annotatored_frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        annotatored_frame = cv2.resize(
            annotatored_frame, dim, interpolation=cv2.INTER_AREA
        )

        cv2.imshow("YOLO V8 Detection", annotatored_frame)
        # предсказание
        # выбор действия

        # cv2.imshow("frame", cv2.cvtColor(window, cv2.COLOR_BGR2RGB))
        print(time.process_time() - t)
        t = time.process_time()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
