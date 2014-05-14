import cv2
import numpy as np
from Filter import Filter
import Tkinter as Tkr


root = Tkr.Tk()
text = Tkr.Entry(root)

blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)

cam = cv2.VideoCapture(1)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
cv2.namedWindow("Show", cv2.CV_WINDOW_AUTOSIZE)
#cv2.namedWindow("Processed", cv2.CV_WINDOW_AUTOSIZE)

# allocate variables
_, img = cam.read()
frame = cv2.cv.CreateImage(img.shape[:2], 16, 3)
frameHSV = np.zeros(img.shape, np.uint16)
blue_filt = Filter(img, "alg", "filt", conf_file="blue ball.conf", config_enable=False, filter_type=0)
green_filt = Filter(img, "green_alg", "green_filt", conf_file="green cup.conf", config_enable=False, filter_type=0)
red_filt = Filter(img, "red alg", "red filt", conf_file="red ball.conf", config_enable=False, filter_type=1)


while True:
    _, frame = cam.read()
    frame = cv2.medianBlur(frame, 5)
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_circles = blue_filt.work(frameHSV)
    green_circles = green_filt.work(frameHSV)
    area = red_filt.work(frameHSV)
    print(area)

    # add circles to original image
    if blue_circles is not None:
        for i in blue_circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], blue, 2)
            cv2.circle(frame, (i[0], i[1]), 2, red, 3)

    if green_circles is not None:
        for i in green_circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], green, 2)
            cv2.circle(frame, (i[0], i[1]), 2, red, 3)

    if blue_circles is None:
        num_blue = 0
    else:
        num_blue = len(blue_circles)

    if green_circles is None:
        num_green = 0
    else:
        num_green = len(green_circles)

    # text.delete(0, len(text.get()))
    # text.insert(Tkr.INSERT, "Detected objects are:\nred : {}\ngreen : {}\nblue : {}"
    #             .format(area, num_green, num_blue))
    # text.pack()
    # root.mainloop(1)
    # text.mainloop(1)
    print("Detected objects are:\nred : {}\ngreen : {}\nblue : {}".format(area, num_green, num_blue))

    cv2.imshow("Show", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
blue_filt.close()
green_filt.close()
red_filt.close()
