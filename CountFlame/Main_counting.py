import cv2
import numpy as np


image = cv2.imread("roi.jpg")


mask = np.zeros_like(image)
cv2.circle(mask, (114, 114), 112, (255, 255, 255), -1) 
masked_img = cv2.bitwise_and(image, mask)

mask2 = np.zeros_like(image)
cv2.circle(mask2, (114, 114), 95, (255, 255, 255), -1) 
masked2 = cv2.bitwise_and(image, mask2)

frame = cv2.bitwise_or(masked2, masked_img)


hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

lower_blue = np.array([0, 12,100])
upper_blue = np.array([179, 255, 255])

mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)


edges=cv2.Canny(mask_blue,200,400)
cv2.imshow("dd",edges)


kernel = np.ones((5, 5), np.uint8)


eroded_mask = cv2.erode(mask_blue, kernel, iterations=1)


dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=2)
cv2.imshow("Orijinal2", dilated_mask)

contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)


alev_sayisi = len(contours)
cv2.putText(frame, f'Alev Sayisi: {alev_sayisi}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Sonucu göster
cv2.imshow("Orijinal", frame)

# Çıkış için herhangi bir tuşa basmayı bekle
cv2.waitKey(0)
cv2.destroyAllWindows()
