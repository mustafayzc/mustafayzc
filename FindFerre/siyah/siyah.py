import cv2
import numpy as np

def Ferre():
    image_path = 'image/7.jpg'
    image = cv2.imread(image_path, 0)
    LastImage=cv2.imread(image_path)
    LastImage=cv2.resize(LastImage,(640,640))

    if image is None:
        print("Resim yüklenemedi. Dosya yolu kontrol edin.")
        return
    
    image = cv2.resize(image, (640, 640))

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    #cv2.imshow('Blurred Image', blurred)
    

    threshold_value = 25
    _, threshold = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(threshold, 100, 200)
    #cv2.imshow('Edges', edges)
    

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rois = []

    mask = np.zeros_like(image)
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_area = int(w * h)
        
        if 35 <= w <= 42 and 12 <= h <= 32 and 500 <= contour_area <= 1000:
        
            cv2.rectangle(mask, (x, y), (x + w , y + h ), 255, -1)  # Beyaz renk
            
            rois.append((x, y, w, h))
            
    # maskeleri alanda göster
    masked_img = cv2.bitwise_and(image, mask)
    template = cv2.resize(cv2.imread('image/103.jpg', 0), (0, 0), fx=0.8, fy=0.8)

    _, masked_img = cv2.threshold(masked_img, 47, 255, cv2.THRESH_BINARY)
    _, template = cv2.threshold(template, 47, 255, cv2.THRESH_BINARY)

    morphologic = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, morphologic)
    masked_img= cv2.morphologyEx(masked_img, cv2.MORPH_CLOSE, morphologic)
    

    masked_img = cv2.Canny(masked_img, 100, 200)
    template = cv2.Canny(template, 100, 200)
    kernel = np.ones((2, 2), np.uint8)
    
    masked_img = cv2.dilate(masked_img, kernel, iterations=1) 
    template = cv2.dilate(template, kernel, iterations=1) 
    
    #cv2.imshow('Masked Image1', masked_img)
    #cv2.imshow('Masked Image2', template)

    K, L = template.shape

    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,
               cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    print(f"k:{K} ,L:{L}")

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
        
        # Check if the match value meets the threshold
        
        bottom_right = (location[0] + L, location[1] + K)
        
        print(f"Location:{location},Bottom right:{bottom_right}")

        if location[0]==0 and location[1]==0:
            print("bir metotta ferre bulunamadi ")
            continue
        
        #cv2.rectangle(LastImage, location, bottom_right, (0,255,0),2)
        cv2.rectangle(img2, location, bottom_right, (255,255,255),5)
        cv2.namedWindow('Masked Image',cv2.WINDOW_NORMAL)
        cv2.imshow('Masked Image', img2)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

Ferre()
