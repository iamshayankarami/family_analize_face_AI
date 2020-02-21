import numpy as np
import cv2
from time import sleep
import os
import sqlite3


cap = cv2.VideoCapture(0)
while True:
    cv2.namedWindow('frame', 0)
    cv2.resizeWindow('frame', 600, 600)
    _,frame = cap.read()
    cv2.imshow('frame', frame)
    key = cv2.waitKey(10)
    #ok stuped people out there non of you can't undrastand what am i doing hear becuse Iam the best
    cv2.rectangle(frame, (200, 200), (250, 250), (255, 0, 0), 2)
    cv2.rectangle(frame, (300, 200), (350, 350), (0, 0, 255), -1)

