from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
import cv2
import numpy as np
from PIL import ImageGrab
import time
import math


def init_yolo():
    time.process_time()
    return YOLO("yolov8n_v2.pt")


def use_yolo_with_annotator(frame, model: YOLO):
    frame = np.array(frame)

    # speed = get_speed(window)
    results = model.predict(
        source=frame, save=False, verbose=False
    )  # save plotted images
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


class YoloWorldModel:
    obstacles = []
    range_to_stop = None
    range_to_stoplight = None
    stoplight_signal = False


class YoloObstacle:
    x = 0.0
    y = 0.0
    name = ""
    xyxy = None


def get_signal_from_stoplight_image(frame, bbox):

    signal_frame = frame[int(bbox[1]) : int(bbox[3]), int(bbox[0]) : int(bbox[2])]

    lower_color = np.array([200, 200, 200])
    upper_color = np.array([255, 255, 255])
    speed_hist = cv2.inRange(signal_frame, lower_color, upper_color)
    signal_frame = cv2.bitwise_and(signal_frame, signal_frame, mask=speed_hist)
    signal_frame = cv2.cvtColor(signal_frame, cv2.COLOR_RGB2GRAY)

    kernel = np.ones((2, 2), np.uint8)
    signal_frame = cv2.morphologyEx(signal_frame, cv2.MORPH_OPEN, kernel, iterations=1)
    kernel = np.ones((2, 2), np.uint8)
    signal_frame = cv2.dilate(signal_frame, kernel, iterations=1)

    top = 0
    for i in range(signal_frame.shape[0]):
        for j in range(signal_frame.shape[1]):
            if signal_frame[i][j] != 0:
                top = i
                break
    left = 0
    for j in range(signal_frame.shape[1]):
        for i in range(signal_frame.shape[0]):
            if signal_frame[i][j] != 0:
                left = j
                break
    bottom = 0
    for i in reversed(range(signal_frame.shape[0])):
        for j in reversed(range(signal_frame.shape[1])):
            if signal_frame[i][j] != 0:
                bottom = i
                break
    right = 0
    for j in reversed(range(signal_frame.shape[1])):
        for i in reversed(range(signal_frame.shape[0])):
            if signal_frame[i][j] != 0:
                right = j
                break
    width = abs(left - right)
    height = abs(top - bottom)

    cv2.imshow("signal frame", signal_frame)

    if width == 0 or height == 0:
        return False

    ratio = height / width
    if ratio >= 0.8:
        return True
    else:
        return False


def use_yolo_with_model(frame, model: YOLO, need_annotation: bool):
    frame = np.array(frame)

    results = model.predict(source=frame, save=False, verbose=False)
    fov = math.pi / 2  # пусть fov будет 90 градусов
    fov_local_height = math.sqrt(1 / (2 * (1 - math.cos(fov))) - 0.25)
    world_model = YoloWorldModel()
    for r in results:
        annotator = Annotator(frame)
        boxes = r.boxes
        max_left_coord_of_stoplight = 0
        for box in boxes:
            b = box.xyxy[0]
            box_borders = (
                box.xyxy[0].cpu().numpy()
            )  # get box coordinates in (left, top, right, bottom) format
            box_name = model.names[int(box.cls)]
            # обрабатываем препятствие
            if box_name == "person" or box_name == "car":
                max_object_size = 0
                if box_name == "person":
                    max_object_size = frame.shape[0] * 0.95
                elif box_name == "car":
                    max_object_size = frame.shape[0] * 0.5
                now_object_size = box_borders[3] - box_borders[1]
                distance = max_object_size / now_object_size

                mid_coords = (box_borders[2] + box_borders[0]) / 2.0
                mid_of_frame = frame.shape[1] / 2.0

                tg_of_angle = (
                    abs(mid_of_frame - mid_coords) / frame.shape[1]
                ) / fov_local_height
                angle = math.atan(tg_of_angle)
                if mid_coords >= mid_of_frame:
                    angle = fov / 2 - angle
                else:
                    angle = angle + fov / 2

                # получили полярные коррдинаты angle, distance, переводим в декартовы
                new_obstacle = YoloObstacle()
                new_obstacle.x = distance * math.cos(angle)
                new_obstacle.y = distance * math.sin(angle)
                new_obstacle.name = box_name
                new_obstacle.xyxy = box_borders
                world_model.obstacles.append(new_obstacle)

                if need_annotation:
                    annotator.box_label(
                        b,
                        str(round(new_obstacle.x, 1))
                        + " "
                        + str(np.round(new_obstacle.y, 1)),
                    )
            elif box_name == "stopcircle":
                distance_to_end = (
                    (frame.shape[0] - box_borders[3]) / frame.shape[0] * 100
                )
                world_model.range_to_stop = distance_to_end

                if need_annotation:
                    annotator.box_label(
                        b,
                        str(round(distance_to_end, 1)),
                    )
            elif box_name == "stoplight":
                if max_left_coord_of_stoplight < box_borders[2]:
                    max_left_coord_of_stoplight = box_borders[2]
                    distance_to_end = (box_borders[1]) / frame.shape[0] * 100
                    world_model.range_to_stoplight = distance_to_end

                    world_model.stoplight_signal = get_signal_from_stoplight_image(
                        frame, box_borders
                    )

                    last_b = b

        if need_annotation and world_model.range_to_stoplight != None:
            annotator.box_label(
                last_b,
                str(round(world_model.range_to_stoplight, 1))
                + " "
                + str(world_model.stoplight_signal),
            )

    if need_annotation:
        annotatored_frame = annotator.result()

        scale_percent = 40  # percent of original size
        width = int(annotatored_frame.shape[1] * scale_percent / 100)
        height = int(annotatored_frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        annotatored_frame = cv2.resize(
            annotatored_frame, dim, interpolation=cv2.INTER_AREA
        )
        return world_model, annotatored_frame
    else:
        return world_model
