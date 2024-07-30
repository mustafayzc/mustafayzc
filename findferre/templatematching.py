import numpy as np
import cv2

img = cv2.resize(cv2.imread('image/8.jpg', 0), (640, 640), fx=0.8, fy=0.8)
template = cv2.resize(cv2.imread('image/101.jpg', 0), (0, 0), fx=0.8, fy=0.8)



img=cv2.GaussianBlur(img,(5,5),0)
img=cv2.blur(img, (3, 3))

_,img = cv2.threshold(img,50, 255, cv2.THRESH_BINARY)


img = cv2.Canny(img, 100, 200)


cv2.imshow('Match8', img)




template=cv2.GaussianBlur(template,(3,3),0)
template=cv2.blur(template, (3, 3)) 

template= cv2.adaptiveThreshold(template, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 5)


template = cv2.Canny(template, 100, 200)



cv2.imshow('waaid', template)





if img is None:
    print(" kontrol et")
    exit()

if template is None:
    print("kontrol et")
    exit()

h, w = template.shape

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

for method in methods:
    img2 = img.copy()

   
    result = cv2.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
   
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        location = min_loc
    else:
        location = max_loc

   
    bottom_right = (location[0] + w, location[1] + h)    
    cv2.rectangle(img2, location, bottom_right, 255, 5)
   
    cv2.imshow('Match', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()