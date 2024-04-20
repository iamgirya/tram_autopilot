from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
import cv2
import numpy as np
from PIL import ImageGrab
import time


def init_yolo():
    time.process_time()
    return YOLO("yolov8n.pt")


def use_yolo(frame, model: YOLO):
    frame = np.array(frame)

    # speed = get_speed(window)
    results = model.predict(source=frame, save=False)  # save plotted images
    for r in results:
        annotator = Annotator(frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)])
    annotatored_frame = annotator.result()

    scale_percent = 40  # percent of original size
    width = int(annotatored_frame.shape[1] * scale_percent / 100)
    height = int(annotatored_frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    annotatored_frame = cv2.resize(annotatored_frame, dim, interpolation=cv2.INTER_AREA)

    return annotatored_frame
    # cv2.imshow("YOLO V8 Detection", annotatored_frame)

    # print(time.process_time() - t)
    # t = time.process_time()


# предсказание
# выбор действия
