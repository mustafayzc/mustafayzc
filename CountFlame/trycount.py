import cv2
import numpy as np


img = cv2.imread('stove12.jpg')
img = cv2.medianBlur(img,5)
img=cv2.resize(img,(580,810))

image=img.copy()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([49, 34, 82])
upper_blue = np.array([179, 255, 255])


mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)


edges = cv2.Canny(mask_blue,100,200)

circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,1, 50 ,param1=80,param2=20,minRadius=25,maxRadius=110)


circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    #dairenin cevresi
    
    
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    cv2.circle(img,(i[0],i[1]),i[2]+25,(0,255,0),2)

    
    if 88<i[2]<100:
        cv2.putText(img, f'En Buyuk Bek : {i[2]}', (i[0]-70, i[1]-i[2]-50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
        


    elif 45<i[2]<55:
        cv2.putText(img, f'Orta Bek : {i[2]}', (i[0]-70, i[1]-i[2]-50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

    
    elif 30<i[2]<44:
        cv2.putText(img, f'Kucuk Bek : {i[2]}', (i[0]-70, i[1]-i[2]-50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)    
    
    else:
        print("thats ok")
    #dairenin merkezini ciz
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

  


    

     





print(circles)
cv2.imshow('círculos detectados',img)
cv2.waitKey(0)
cv2.destroyAllWindows()