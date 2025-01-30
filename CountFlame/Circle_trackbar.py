import cv2  
import numpy as np  

def draw_ellipse(val):  
    img = cv2.imread("stove5.jpg")  # Resmi oku  
    img = cv2.resize(img, (535, 535))  # Resmin boyutunu ayarla  

    axes_length = cv2.getTrackbarPos('Axes Length', 'Ellipse')  # İlk trackbar'ın değerini al  
    axes = cv2.getTrackbarPos('Axes', 'Ellipse')  # İkinci trackbar'ın değerini al  
    cv2.ellipse(img, (280, 272), (axes_length, axes), 0, 0, 360, (255, 255, 255), 1)  
    cv2.imshow('Ellipse', img)  

cv2.namedWindow('Ellipse')  
cv2.createTrackbar('Axes Length', 'Ellipse', 10, 300, draw_ellipse)  
cv2.createTrackbar('Axes', 'Ellipse', 10, 300, draw_ellipse)   

draw_ellipse(0)  # İlk gereksinimi geçmek için bir çağrı  
cv2.waitKey(0)  
cv2.destroyAllWindows()