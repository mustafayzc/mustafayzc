import cv2  
import numpy as np  

  
image = cv2.imread('stove5.jpg')
image=cv2.resize(image,(640,640))

  
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  

 
lower_hsv = np.array([0, 0, 0])  # Alt sınır  
upper_hsv = np.array([179, 36, 255])  # Üst sınır  

 
mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)  


result = cv2.bitwise_and(image, image, mask=~mask)   


lower_blue = np.array([46, 79, 148])
upper_blue = np.array([125, 255, 255])


lower_flame = np.array([0, 59, 155])
upper_flame = np.array([95, 255, 255])


hsv_image = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)


cv2.imshow('HSV Image', hsv_image)


blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)
flame_mask = cv2.inRange(hsv_image, lower_flame, upper_flame)


kernel = np.ones((5,5), np.uint8)
blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel) #içteki gürültüyü engeller
blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel) #dıştaki gürültüyü engeller

flame_mask = cv2.morphologyEx(flame_mask, cv2.MORPH_CLOSE, kernel)
flame_mask = cv2.morphologyEx(flame_mask, cv2.MORPH_OPEN, kernel)


contours_blue, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_flame, _ = cv2.findContours(flame_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

toplam_alan=0  
areas = []  

for i in range(len(contours_blue)):  
    area1 = cv2.contourArea(contours_blue[i])  
    areas.append(area1)  # Alanı listeye ekle  
     
 
for area1 in areas:  
    toplam_alan += area1  

#print(f"Toplam alan blue: {toplam_alan}")  

toplam_alan_flame=0
areas_2=[]

for i in range(len(contours_flame)):  
    area2 = cv2.contourArea(contours_flame[i])  
    areas_2.append(area2)  # Alanı listeye ekle  
    
# Toplam alanı hesapla  
for area2 in areas_2:  
    toplam_alan_flame += area2  
    
#print(f"Toplam alan flame: {toplam_alan_flame}")  

toplam=toplam_alan+toplam_alan_flame
yuzde=toplam_alan/toplam*100
print(f"alev kalitesi: %{yuzde}")




result_image = image.copy()
cv2.drawContours(result_image, contours_blue, -1, (255, 0, 0), 1)  
cv2.drawContours(result_image, contours_flame, -1, (0, 0, 255), 2)  

# Sonucu göster
cv2.imshow('Result Image', result_image)
cv2.waitKey(0) 
cv2.destroyAllWindows() 