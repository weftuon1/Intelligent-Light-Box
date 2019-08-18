import time
import os
import datetime

import numpy as np
import argparse
import cv2

import serial
import struct

# 115200, 8, N, 1
ser = serial.Serial('/dev/serial0', 115200, timeout=None,
                    parity=serial.PARITY_NONE)
print(ser.name)


while True:
    d1 = time.strftime("%Y_%m_%d-%H_%M_%S")
    #action = "fswebcam -r 480x480 -S 5 --no-banner -d /dev/video0 " + "./images/" + "test" + ".jpg"
    action = "fswebcam -r 480x480 -S 5 --no-banner -d /dev/video0 " + "./images/" + d1 + ".jpg"
    os.system(action)

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    #ap.add_argument("-i", "--image", help = "path to the image file")
    #ap.add_argument("-r", "--radius", type = int, help = "radius of Gaussian blur; must be odd")
    args = vars(ap.parse_args())

    args["radius"] = 41
    # load the image and convert it to grayscale
    #image = cv2.imread(args["image"])
    
    #image = cv2.imread("./images/test.jpg")
    image = cv2.imread("./images/" + d1 + ".jpg")
    
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply a Gaussian blur to the image then find the brightest
    # region
    gray = cv2.GaussianBlur(gray, (args["radius"], args["radius"]), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    image = orig.copy()
    cv2.circle(image, minLoc, args["radius"], (255, 0, 0), 2)

    # display the results of our newly improved method
    #cv2.imshow("Robust", image)
    #cv2.waitKey(0)
    
    #cv2.imwrite("./images/test2.jpg", image)
    cv2.imwrite("./images/" + d1 + "_2.jpg", image)

    print("minLoc: ", minLoc)
    print("Finished finding darkest area.")
    print("Sending location to ARC.")

    mesg=str(minLoc[0])+','+str(minLoc[1])
    ser.write(mesg.encode())
    ser.write(b'\r\n')

    time.sleep(1*10)

ser.close()
