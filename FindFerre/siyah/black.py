import cv2
import numpy as np
from collections import Counter

def Ferre():
    image_path = 'image/10.jpg'
    image = cv2.imread(image_path, 0)
    LastImage=cv2.imread(image_path)
    LastImage=cv2.resize(LastImage, (640,640))

    if image is None:
        print("Resim yüklenemedi. Dosya yolu kontrol edin.")
        return
    
    image = cv2.resize(image, (640, 640))

    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    threshold_value = 25
    _, threshold = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(threshold, 100, 200)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rois = []

    mask = np.zeros_like(image)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_area = int(w * h)
        
        if 35 <= w <= 42 and 12 <= h <= 32 and 500 <= contour_area <= 1000:
            cv2.rectangle(mask, (x, y), (x + w , y + h ), 255, -1)  # Beyaz renk
            rois.append((x, y, w, h))
    
    masked_img = cv2.bitwise_and(image, mask)
    template = cv2.resize(cv2.imread('image/103.jpg', 0), (0, 0), fx=0.8, fy=0.8)

    _, masked_img = cv2.threshold(masked_img, 47, 255, cv2.THRESH_BINARY)
    _, template = cv2.threshold(template, 47, 255, cv2.THRESH_BINARY)

    morphologic = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, morphologic)
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_CLOSE, morphologic)

    masked_img = cv2.Canny(masked_img, 100, 200)
    template = cv2.Canny(template, 100, 200)
    kernel = np.ones((2, 2), np.uint8)
    
    masked_img = cv2.dilate(masked_img, kernel, iterations=1) 
    template = cv2.dilate(template, kernel, iterations=1) 
    
    K, L = template.shape

    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    locations = []
    
    for method in methods:
        img2 = masked_img.copy()
        result = cv2.matchTemplate(img2, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            match_value = min_val
            location = min_loc
        else:
            match_value = max_val
            location = max_loc
        
        if location[0] == 0 and location[1] == 0:
            print("Bir metotta ferre bulunamadi")
            continue
        print('match value:',match_value)
        locations.append(location)

    # Koordinat say
    coordinate_counts = Counter(locations)
    most_common_coordinate, count = coordinate_counts.most_common(1)[0]

    
    if count >= 2:
        top_left = most_common_coordinate
        bottom_right = (top_left[0] + L, top_left[1] + K)
        cv2.rectangle(LastImage, top_left, bottom_right, (0, 255, 0), 2)
        cv2.imshow('Masked Image', LastImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("En az 2 metot tutmadi.")

Ferre()
