from windows_capture import WindowsCapture, Frame, InternalCaptureControl
from time import sleep, time
import numpy as np
import cv2
import threading
import yolo_predict
import output

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
    while True:
        # sleep(0)
        # Короче, тут происходит потеря данных при передаче между потоками данных при записи
        # 1. Сбор данных
        lock.acquire()
        yolo_frame = yolo_predict.use_yolo(frameg, model)
        # get_speed...

        # cv2.imwrite("trash\lol2.bmp", frameg)
        cv2.imshow("yolo_frame", yolo_frame)
        # предсказание
        # выбор действия

        lock.release()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


# Код
model = yolo_predict.init_yolo()
output.init_output()
capture.start_free_threaded()
main_loop()
