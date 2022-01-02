import time

import numpy as np
import cv2
import win32con
import win32gui
import win32ui
from PIL import ImageGrab
from PIL.Image import Image
from win32api import GetSystemMetrics


class CaptureScreen:
    def __init__(self, top=0, left=0, width=0, height=0, specific_part=False):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.specific_part = specific_part
        self.img = np.array([])

    def capture(self):
        if self.specific_part:
            self.img = ImageGrab.grab(bbox=(self.top, self.left, self.width, self.height))
        else:
            self.img = ImageGrab.grab()

        self.img = np.array(self.img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        return self.img

    def capture_specific_application(self, hwnd):
        w, h = GetSystemMetrics(0), GetSystemMetrics(1)

        # if window_name:
        #     hwnd = win32gui.FindWindow(None, window_name)
        # else:
        #     hwnd = win32gui.GetDesktopWindow()

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

        self.img = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype='uint8')
        self.img.shape = (h, w, 4)

        return self.img

    @staticmethod
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))


win32gui.EnumWindows(CaptureScreen().winEnumHandler, None)

