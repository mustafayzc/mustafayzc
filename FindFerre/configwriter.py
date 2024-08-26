import cv2
import numpy as np
import configparser
from collections import Counter

def Code(config):
    #config.ini
    lower = np.array(eval(config['lower']))
    upper = np.array(eval(config['upper']))
    threshold_value = int(config['threshold_value'])
    threshold_value_1 = int(config['threshold_value_1'])
    threshold_value_2 = int(config['threshold_value_2'])
    morphologic_1 = int(config['morphologic_1'])
    morphologic_2 = int(config['morphologic_2'])

    #image_path, template , config White Gray Black değiştir
    image_path = '21.jpg'
    image = cv2.imread(image_path)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.inRange(image, lower, upper)
    image = cv2.resize(image, (640, 640))

    LastImage = cv2.imread(image_path)
    LastImage = cv2.resize(LastImage, (640, 640))

    if image is None:
        print("Resim yüklenemedi. Dosya yolu kontrol edin.")
        return

    image = cv2.resize(image, (640, 640))
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, threshold = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(threshold, 100, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rois = []
    mask = np.zeros_like(image)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        contour_area = int(w * h)

        if 35 <= w <= 42 and 12 <= h <= 32 and 500 <= contour_area <= 1000:
            cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
            rois.append((x, y, w, h))

    masked_img = cv2.bitwise_and(image, mask)
    template = cv2.resize(cv2.imread('104.jpg', 0), (0, 0), fx=0.8, fy=0.8)
    _, masked_img = cv2.threshold(masked_img, threshold_value_1, 255, cv2.THRESH_BINARY)
    _, template = cv2.threshold(template, threshold_value_2, 255, cv2.THRESH_BINARY)
    
    morphologic = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morphologic_1, morphologic_2))
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, morphologic)
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_CLOSE, morphologic)
    
    masked_img = cv2.Canny(masked_img, 200, 400)
    template = cv2.Canny(template, 100, 200)
    kernel = np.ones((2, 2), np.uint8)
    masked_img = cv2.dilate(masked_img, kernel, iterations=1)
    template = cv2.dilate(template, kernel, iterations=1)
    K, L = template.shape
    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
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

        bottom_right = (location[0] + L, location[1] + K)
        print(f"Location:{location},Bottom right:{bottom_right}")

        if location[0] == 0 and location[1] == 0:
            print("Bir metotta ferre bulunamadi")
            continue

        locations.append(location)

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

    
# Config dosyasını okuma
config = configparser.ConfigParser()
config.read('config.ini')

# Burdan gönder White Gray Black
foto=Code(config['White'])
