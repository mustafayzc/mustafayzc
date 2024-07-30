import cv2 as cv
import numpy as np

def threshold_work():
    

    def nothing(x):
        pass

    image = cv.imread("image/10.jpg", cv.IMREAD_GRAYSCALE)
    #image=cv.GaussianBlur(image,(5,5),0)
    #image=cv.blur(image, (3, 3))

    cv.namedWindow('Thresholded Image', cv.WINDOW_NORMAL)

    cv.createTrackbar('Threshold', 'Thresholded Image', 0, 255, nothing)

    while True:
        threshold_value = cv.getTrackbarPos('Threshold', 'Thresholded Image')

        _, thresholded_img = cv.threshold(image, threshold_value, 255, cv.THRESH_BINARY)

        cv.imshow('Thresholded Image', thresholded_img)
    
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break

    cv.destroyAllWindows()

threshold_work()