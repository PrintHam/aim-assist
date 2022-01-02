import time
import cv2
from screen_capture import CaptureScreen

cs = CaptureScreen(0, 0, 1000, 1000, True)

start_time = time.time()

while True:
    screen = cs.capture_specific_application(0x20a7a)
    cv2.imshow("Test", screen)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

    fps = 1 / (time.time() - start_time)
    start_time = time.time()

    print(fps)

#
# CaptureScreen().capture_specific_application()
