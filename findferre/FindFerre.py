import cv2
import numpy as np

def Ferre():
   
    image_path = 'image/10.jpg'
    image = cv2.imread(image_path, 0)
    
    if image is None:
        print("Resim yüklenemedi. Dosya yolu kontrol edin.")
        return
    
    image = cv2.resize(image, (640, 640))

    
    blurred = cv2.GaussianBlur(image, (5, 5), 0) 
    cv2.imshow('Blurred Image', blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    threshold_value = 34
    _, threshold = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)

    
    edges = cv2.Canny(threshold, 100, 200)
    cv2.imshow('Edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Konturları bul
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Orijinal görüntüyü geri yükle
    image_colored = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    rois=[]

    # Belirli bir genişlik ve yüksekliğe sahip konturları bul
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_area = int(w * h)
        
        if 20 <= w <= 52 and 10 <= h <= 27 and 500 <= contour_area <= 800:
            cv2.rectangle(image_colored, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Yeşil renkle sınırlayıcı dikdörtgen çiz
            #print(f"Genişlik: {w}, Yükseklik: {h}")
            #print(f"Alan: {contour_area}")

            #print(f"x kordinat:{x},y kordinat{y}")
            
            rois.append((x,y,w,h))
            roi=rois[-1]
            
            for roi in rois:

            



    # Sonuçları göster
    cv2.imshow('Highlighted Rectangle', image_colored)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

Ferre()

