import cv2
import numpy as np

def Ferre():
    image_path = 'image/8.jpg'
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

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rois = []

    # Boş bir maske oluştur
    mask = np.zeros_like(image)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_area = int(w * h)
        
        if 20 <= w <= 52 and 10 <= h <= 27 and 500 <= contour_area <= 800:
            # Maskeye dikdörtgen ekle
            cv2.rectangle(mask, (x-10, y-10), (x + w + 10, y + h + 10), 255, -1)  # Beyaz renk
            
            rois.append((x, y, w, h))
    
    # Orijinal görüntüyü sadece maskeli alanlarda göster
    masked_img = cv2.bitwise_and(image, mask)
    template = cv2.resize(cv2.imread('image/101.jpg', 0), (0, 0), fx=0.8, fy=0.8)

    masked_img=cv2.GaussianBlur(masked_img,(3,3),0)
    template=cv2.GaussianBlur(template,(3,3),0)

    

    K, L = template.shape

    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    for method in methods:
        img2 = masked_img.copy()
    
        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            location = min_loc
        else:
            location = max_loc

        bottom_right = (location[0] + L, location[1] + K)
        cv2.rectangle(img2, location, bottom_right, 255, 5)
    
        cv2.imshow('Masked Image', img2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

Ferre()
