#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import time
from eight_queen.msg import queens

def callback(data):
    img = np.zeros((8,8,3), np.uint8)
    for row_index, row in enumerate(img):
        for col_index, pixel in enumerate(row):
            if row_index % 2 != col_index %2:
                img[row_index][col_index] = [255,255,255]
            if data.result[row_index] == col_index:
                img[row_index][col_index] = [0,0,255]
    cv2.imshow('result', img)
    cv2.waitKey(1)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("solution", queens, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
