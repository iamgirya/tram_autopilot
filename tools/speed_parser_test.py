from windows_capture import WindowsCapture, Frame, InternalCaptureControl
from win32gui import GetWindowText, GetForegroundWindow
from time import sleep
import cv2
import threading
import trash.speed_from_image_parser as speed_from_image_parser


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
    capture.start_free_threaded()
    sleep(0.1)

    while True:
        if GetWindowText(GetForegroundWindow()) != "TramSim  ":
            sleep(1)
            continue

        lock.acquire()
        sleep(0.2)
        speed_value = speed_from_image_parser.get_speed(frameg)
        print("speed = " + str(speed_value))

        lock.release()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


# Код
main_loop()
