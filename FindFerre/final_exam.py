import cv2
import numpy as np
import time

#Algoritmanin toplam islem suresinin olcumu 
class timer:
    def baslat(self):
        self.baslangic = time.perf_counter()

    def bitir(self):
        self.bitis = time.perf_counter()
        fark = (self.bitis-self.baslangic)*1000
        print(f"{fark} ms'de tamamlandi.")

timer = timer()

#islem suresini baslat
timer.baslat()

#resmi tanımla
image= cv2.imread("capacitor.jpeg")

#resme gaussian filtre uygula
resim = cv2.GaussianBlur(image, (3, 3),0)

#y ekseninde 480 – 680 px araliginda bir roi belirle
y1,y2= 480, 680
roi=resim[y1:y2]

#resmin kopyasini al 
copy=roi.copy()
copy2=roi.copy()

#bacaklarin kenarlarini cizdir
edge = cv2.Canny(roi, 200, 400)

#bacaklarin konturlarini bul 
contours, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


rois_2 = []

c_kordinat=[]

for cnt in contours:
    # Kütle merkezi hesaplama
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])  # x koordinatı
        cy = int(M["m01"] / M["m00"])  # y koordinatı
       
        print(f"Merkez Noktasi: ({cx}, {cy})")
    
    #konturlari ciz    
    cv2.drawContours(copy2, [cnt], -1, (0, 255, 0), 2)

    #Bacaklarin kütle merkez noktalarini c_kordinat listesine ekle
    c_kordinat.append((cx,cy))

    #konturlarin x,y,w,h degerlerini bul
    x, y, w, h = cv2.boundingRect(cnt)
    area = int(w * h)
    
    #konturlari boyutlarina gore filtrele
    if 0 <= w <= 100 and 0 <= h <= 200 and 0 <= area <= 100000000:
        
        #buldugun konturlari dikdortgen cerceveye al 
        cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 3)  
        print(f"Width: {w}, Height: {h}, X:{x},y:{y}")

        #rois_2 listesine degerleri ekle 
        rois_2.append((x, y, w, h))


print(c_kordinat)    

#Bulunan kütle merkez noktalarindan bacaklarin x kordinatini ve bacaklarin y kordinatlarinin en altindan 20 pixel yukarisindaki noktalari adlandir
point1=(c_kordinat[0][0],rois_2[0][3]-20)
point2=(c_kordinat[1][0],rois_2[1][3]-20)

#iki noktayi ciz
image = cv2.circle(copy2, (point1), radius=3, color=(0, 0, 255), thickness=-1)    
image2 = cv2.circle(copy2, (point2), radius=3, color=(0, 0, 255), thickness=-1)

#iki nokta arasinda kirmizi cizgi ciz
cv2.line(copy2, (point1), (point2), (0, 0, 255), thickness=2, lineType=8)

#iki nokta arasida mesafe olcme kuralini uygula
distance = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

#mesafeyi yazdir
print(f"iki merkez noktanin {point1} ve {point2} arasindaki mesafe= {distance:.2f}")

#resmi goster
cv2.imshow("Mesafe ",copy2)

cv2.imwrite("savedimg.jpg",copy2)

#isle suresini olcmeyi bitir
timer.bitir()

cv2.waitKey(0)
cv2.destroyAllWindows()

quit()
