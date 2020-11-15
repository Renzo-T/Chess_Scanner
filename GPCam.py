import os
import urllib.request
import cv2
import numpy as np
import time

def gpcam():
    URL =  'http://192.168.1.196:8080/video'
    cap = cv2.VideoCapture(URL)
    while True:
        ret, frame = cap.read()
        # cv2.imshow('frame',frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
        return frame