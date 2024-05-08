from windows_capture import WindowsCapture, Frame, InternalCaptureControl
from time import sleep, time
import numpy as np
import cv2
import threading
import yolo_predict
import output
import speed_from_image_parser
import decision_module

# Every Error From on_closed and on_frame_arrived Will End Up Here
capture = WindowsCapture(
    capture_cursor=False,
    draw_border=None,
    monitor_index=None,
    window_name="TramSim  ",
)

# time1 = time()
frameg = []
lock = threading.Lock()


# Called Every Time A New Frame Is Available
@capture.event
def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
    global frameg, lock, time1
    sleep(0)
    # print("New Frame Arrived " + str(time() - time1))
    # time1 = time()

    # Тут происходит потеря данных при передаче между потоками данных при записи в файл, но на видео всё норм
    # frame.save_as_image("lol1.jpg")
    # Save The Frame As An Image To The Specified Path
    lock.acquire()
    frameg = frame.frame_buffer[..., :3]
    lock.release()
    # Gracefully Stop The Capture Thread


# Called When The Capture Item Closes Usually When The Window Closes, Capture
# Session Will End After This Function Ends
@capture.event
def on_closed():
    print("Capture Session Closed")


def main_loop():
    # 0. Инициализация
    model = yolo_predict.init_yolo()
    framegId = 0
    output.init_output()
    output.set_up_camera()
    capture.start_free_threaded()
    sleep(0.5)

    output.open_cabine_view()
    sleep(0.1)
    # TODO сейчас просто на верим, что за н-ное время кадр успел смениться. Но так плохо делать
    speed_value = speed_from_image_parser.get_speed(frameg)
    output.open_nose_view()

    while True:
        framegId += 1
        # 1. Сбор данных и получение модели
        lock.acquire()
        if framegId <= 10:
            world_model, yolo_frame = yolo_predict.use_yolo_with_model(
                frameg, model, need_annotation=True
            )
        else:
            output.open_cabine_view()
            sleep(0.1)
            speed_value = speed_from_image_parser.get_speed(frameg)
            output.open_nose_view()
            framegId = 0

        cv2.imshow("yolo_frame", yolo_frame)

        # 2. Принятие решения
        state = decision_module.make_decision(world_model, speed_value)
        # 3. Реализация решения
        output.implementation_of_decision(state)

        lock.release()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


# Код
main_loop()
