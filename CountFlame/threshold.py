import cv2  
import numpy as np  

def adaptive_threshold(val):  
    thresh = cv2.adaptiveThreshold(img_gray, val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)  
    cv2.imshow('Adaptive Threshold', thresh)  

img = cv2.imread('stove11.jpg')  
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

cv2.namedWindow('Adaptive Threshold')  
cv2.createTrackbar('Value', 'Adaptive Threshold', 1, 255, adaptive_threshold)  

adaptive_threshold(127)  # Başlangıçta 127 ile uygula  
cv2.waitKey(0)  
cv2.destroyAllWindows()