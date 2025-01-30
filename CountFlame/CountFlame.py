import cv2
import numpy as np


image=cv2.imread("stove5.jpg")   
  
image = cv2.resize(image, (390, 530))
mask = np.zeros_like(image)
cv2.circle(mask, (203, 270), 185, (255, 255, 255), -1) 
masked_img = cv2.bitwise_and(image, mask)

mask2 = np.zeros_like(image)
cv2.circle(mask2, (203, 270), 155, (255, 255, 255), -1) 
masked2 = cv2.bitwise_and(image, mask2)

frame = cv2.bitwise_xor(masked2, masked_img)    
 
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

lower_blue = np.array([0, 0, 206])
upper_blue = np.array([179, 255, 255])


mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
  


kernel = np.ones((2,2), np.uint8)


dilated_mask = cv2.dilate(mask_blue, kernel, iterations=3)

eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)
    
   
cv2.imshow("Maske", eroded_mask)


contours, _ = cv2.findContours(eroded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
   
cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
alev_sayisi = len(contours)
    
   
cv2.putText(frame, f'Alev Sayisi: {alev_sayisi}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

cv2.imshow("Orijinal", frame)

cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
cv2.imshow("image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()
