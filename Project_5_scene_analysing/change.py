import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('C:/Users/Anya/Projects/homework/01_first_images/homework/task_1/20 by 20 orthogonal maze.png')  # загрузить тестовую картинку
img = cv2.inRange(img, (240, 240, 240), (255, 255, 255))
cv2.imshow('image',img)
cv2.waitKey(0)

def skeletonize(img):
    """ OpenCV function to return a skeletonized version of img, a Mat object"""

    # hat tip to http://felix.abecassis.me/2011/09/opencv-morphological-skeleton/

    img = img.copy() # don't clobber original
    skel = img.copy()

    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

    while True:
        eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img[:,:] = eroded[:,:]
        if cv2.countNonZero(img) == 0:
            break

    return skel

skel = skeletonize(img)
cv2.imshow('image',skel)
cv2.waitKey(0)