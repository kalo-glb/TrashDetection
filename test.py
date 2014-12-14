import cv2
import numpy as np
from Filter import Filter
# import Tkinter as Tkr
import serial


def draw_circles(frame, circles, color):
    if circles is not None:
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], color, 2)
            cv2.circle(frame, (i[0], i[1]), 2, red, 3)

# root = Tkr.Tk()
# text = Tkr.Entry(root)

ser = serial.Serial("/dev/ttyACM1", 9600)

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

cam = cv2.VideoCapture(1)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cv2.namedWindow("Show", cv2.CV_WINDOW_AUTOSIZE)

# allocate variables
_, img = cam.read()
frame = cv2.cv.CreateImage(img.shape[:2], 16, 3)
frameHSV = np.zeros(img.shape, np.uint16)
blue_filt = Filter(img, "alg", "filt", conf_file="blue ball.conf", config_enable=False, filter_type=1)
green_filt = Filter(img, "green_alg", "green_filt", conf_file="green room.conf", config_enable=False, filter_type=1)
red_filt = Filter(img, "red alg", "red filt", conf_file="red glass.conf", config_enable=False, filter_type=1)

prev_sig = 0

while True:
    _, frame = cam.read()
    frame = cv2.medianBlur(frame, 5)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_area = blue_filt.work(frameHSV)
    green_area = green_filt.work(frameHSV)
    red_area = red_filt.work(frameHSV)

    detection_signal = 0
    if blue_area > 30000:
        detection_signal += 1
    if green_area > 25000:
        detection_signal += 2
    if red_area > 5000:
        detection_signal += 4

    if prev_sig != detection_signal:
        print("r : {} g : {} b : {} sig : {}".format(red_area, green_area, blue_area, detection_signal))
        ser.write(chr(detection_signal))
        prev_sig = detection_signal

    cv2.imshow("Show", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
blue_filt.close()
green_filt.close()
red_filt.close()
