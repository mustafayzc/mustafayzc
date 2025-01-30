import cv2  
import numpy as np  

# Resmi yükle  
img = cv2.imread('stove5.jpg')
img = cv2.resize(img, (390, 530))
# Çember çizme fonksiyonu  
def draw_circle(val):  
    # Resmi kopyala  
    img_copy = img.copy()  
    # Trackbar'dan gelen değerle çember yarıçapını ayarla  
    radius = val  
    center = (203, 270)  # Çember merkezi  
    # Çember çiz  
    cv2.circle(img_copy, center, radius, (0, 255, 0), 2)  
    # Çemberi göster  
    cv2.imshow("Cember", img_copy)  

# Pencere ve trackbar oluştur  
cv2.namedWindow("Cember")  
cv2.createTrackbar("Radius", "Cember", 0, 300, draw_circle)  

# İlk başta çember çizmeden görüntüyü göster
draw_circle(0)

while True:  
    if cv2.waitKey(1) & 0xFF == 27:  # 'Esc' tuşuna basılınca çıkış  
        break  

cv2.destroyAllWindows()
