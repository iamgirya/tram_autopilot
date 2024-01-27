from windows_capture import WindowsCapture, Frame, InternalCaptureControl
from time import sleep, time
import numpy as np
import cv2

# Every Error From on_closed and on_frame_arrived Will End Up Here
capture = WindowsCapture(
    capture_cursor=False,
    draw_border=None,
    monitor_index=None,
    window_name="TramSim  ",
)

time1 = time()
frameg = np.zeros((10, 10, 3), np.uint8)


# Called Every Time A New Frame Is Available
@capture.event
def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
    global time1, frameg
    print("New Frame Arrived" + str(time() - time1))
    time1 = time()

    # Save The Frame As An Image To The Specified Path
    frameg = frame.frame_buffer[..., :3]

    # Gracefully Stop The Capture Thread


# Called When The Capture Item Closes Usually When The Window Closes, Capture
# Session Will End After This Function Ends
@capture.event
def on_closed():
    print("Capture Session Closed")


capture.start_free_threaded()
while True:
    cv2.imwrite("image.jpg", frameg)
    cv2.imshow("lol", frameg)
    sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
