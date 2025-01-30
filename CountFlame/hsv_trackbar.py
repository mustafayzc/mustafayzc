import cv2
import numpy as np

def nothing(x):
    pass

# Boş bir siyah pencere oluştur
cv2.namedWindow('frame')

# İzlenecek nesnenin başlangıç değerleri
hsv_lower = np.array([0, 50, 50])
hsv_upper = np.array([50, 255, 255])

# Trackbarlar oluştur
cv2.createTrackbar('Hue Lower', 'frame', 0, 179, nothing)
cv2.createTrackbar('Saturation Lower', 'frame', 50, 255, nothing)
cv2.createTrackbar('Value Lower', 'frame', 50, 255, nothing)
cv2.createTrackbar('Hue Upper', 'frame', 50, 179, nothing)
cv2.createTrackbar('Saturation Upper', 'frame', 255, 255, nothing)
cv2.createTrackbar('Value Upper', 'frame', 255, 255, nothing)

img = cv2.imread('stove5.jpg')  # Fotoğrafı yükle
img=cv2.resize(img,(640,640))

while True:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Trackbar değerlerini al
    hsv_lower[0] = cv2.getTrackbarPos('Hue Lower', 'frame')
    hsv_lower[1] = cv2.getTrackbarPos('Saturation Lower', 'frame')
    hsv_lower[2] = cv2.getTrackbarPos('Value Lower', 'frame')
    hsv_upper[0] = cv2.getTrackbarPos('Hue Upper', 'frame')
    hsv_upper[1] = cv2.getTrackbarPos('Saturation Upper', 'frame')
    hsv_upper[2] = cv2.getTrackbarPos('Value Upper', 'frame')

    # Maskeleme
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    res = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('frame', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
