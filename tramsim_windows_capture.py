from win32gui import GetWindowText, GetForegroundWindow
from windows_capture import WindowsCapture, Frame, InternalCaptureControl
from time import sleep
import threading

# Every Error From on_closed and on_frame_arrived Will End Up Here
capture = WindowsCapture(
    capture_cursor=False,
    draw_border=None,
    monitor_index=None,
    window_name="TramSim  ",
)

frameg = []
lock = threading.Lock()


# Called Every Time A New Frame Is Available
@capture.event
def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
    global frameg, lock, time1

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


def init_capture():
    global lock
    capture.start_free_threaded()
    return lock


def get_frame():
    global frameg
    while GetWindowText(GetForegroundWindow()) != "TramSim  ":
        sleep(1)
    return frameg
