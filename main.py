import cv2
import numpy as np
import win32gui
import win32ui
import win32con
from PIL import Image
import time
import mss
from datetime import datetime
import uuid



global realHwnd
def enumHandler(hwnd, lParam):
    global realHwnd
    if win32gui.IsWindowVisible(hwnd):
        if 'Cemu' in win32gui.GetWindowText(hwnd):
            realHwnd = hwnd

#Get a list of Windows
win32gui.EnumWindows(enumHandler, None)
hwnd = realHwnd
# Get Window Width and Height https://stackoverflow.com/questions/7142342/get-window-position-size-with-python
win32gui.SetForegroundWindow(hwnd)
time.sleep(0.2)

dimensions = win32gui.GetWindowRect(hwnd)
monitor = {'top': dimensions[0], 'left': dimensions[1], 'width': dimensions[2]-dimensions[1], 'height': dimensions[3]-dimensions[0]}


#Source : http://python-mss.readthedocs.io/en/dev/examples.html#pil
#Using multiscreenshot because of the amazing fps
with mss.mss() as sct:
    while 1:
        # Get raw pixels from the screen, save it to a Numpy array
        sct_grab= sct.grab(monitor)
        img = np.array(sct_grab)
        # Display the picture after converting to grayscale
        #Source : http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
        # cv2.imshow('OpenCV/Numpy normal', img)
        # grayscaleimg = cv2.cvtColor(img)q
        im = Image.fromarray(img)
        path= "c:\\BoTWpics\\"+ str(uuid.uuid4())+".png"
        # Save to the picture file
        time.sleep(0.1)
        mss.tools.to_png(sct_grab.rgb, sct_grab.size, path)
        cv2.imshow('BoTW PC View', img)
        print(path)
        #Quit when the Q button is clicked
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


