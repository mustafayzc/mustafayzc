import cv2
import numpy as np

# Görüntüyü dosyadan yükle
# 'stove16.jpg' adlı görüntü okunarak bir NumPy dizisine aktarılır
img = cv2.imread('stove16.jpg')

# Görüntüdeki gürültüyü azaltmak için orta noktaya dayalı bulanıklık filtresi uygulanır
img = cv2.medianBlur(img, 5)

# Görüntü, işlem kolaylığı için 580x810 boyutlarına yeniden boyutlandırılır
img = cv2.resize(img, (580, 810))

# Orijinal görüntünün bir kopyası alınır
# Bu kopya üzerinde işlem yapılarak sonuç görüntüsü elde edilecektir
image = img.copy()

# Görüntü, BGR renk uzayından HSV (Ton, Doygunluk, Parlaklık) renk uzayına dönüştürülür
# HSV renk uzayı, belirli renk aralıklarının tespit edilmesinde daha etkili olduğu için tercih edilir
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Tespit edilmek istenen belirli bir renk aralığını tanımlıyoruz
# Burada 'blue' olarak adlandırılan, beklerin çevresindeki mavi renkli alanları hedefliyoruz
lower_blue = np.array([49, 34, 82])  # HSV renk uzayında alt sınır
upper_blue = np.array([179, 255, 255])  # HSV renk uzayında üst sınır

# Tanımlanan HSV aralığına uyan piksellerin bulunduğu bir maske oluşturulur
# Bu maske, yalnızca belirtilen renk aralığına sahip pikselleri beyaz olarak işaretler
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

# Kenar tespiti yapılır
# Canny algoritması kullanılarak maskelenmiş görüntüdeki kenarlar belirlenir
edges = cv2.Canny(mask_blue, 100, 200)

# Kenar tespitine dayalı olarak daire tespiti yapılır
# Hough Dairesel Dönüşümü kullanılarak dairesel yapılar algılanır
circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 50, param1=80, param2=20, minRadius=25, maxRadius=110)

# Eğer herhangi bir daire tespit edilmişse:
if circles is not None:
    # Tespit edilen dairelerin koordinatları ve yarıçapları tam sayıya yuvarlanır
    circles = np.uint16(np.around(circles))

    # Birleştirilecek tüm maskeleri saklamak için boş bir maske oluşturulur
    combined_mask = np.zeros_like(image)

    # Her bir tespit edilen daire için işlemler yapılır
    for i in circles[0, :]:
        # Her bir daire için geçici bir maske oluşturulur
        mask = np.zeros_like(image)

        # Tespit edilen dairenin dış sınırını (çember) çizeriz
        # Dış sınır genişletilir (içeriye doğru siyah çember ile sınır eklenir)
        cv2.circle(mask, (i[0], i[1]), i[2] + 25, (255, 255, 255), -1)  # Dış çember
        cv2.circle(mask, (i[0], i[1]), i[2] + 8, (0, 0, 0), -1)  # İç çember

        # Geçici maske, birleşik maske ile birleştirilir
        combined_mask = cv2.bitwise_or(combined_mask, mask)

        # Tespit edilen bek, boyutuna göre sınıflandırılır:
        if 85 < i[2] < 100:  # En büyük bek tespiti
            cv2.putText(image, f'En Buyuk Bek : {i[2]}', (i[0] - 70, i[1] - i[2] - 50), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
        elif 45 < i[2] < 55:  # Orta boy bek tespiti
            cv2.putText(image, f'Orta Bek : {i[2]}', (i[0] - 70, i[1] - i[2] - 50), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
        elif 30 < i[2] < 44:  # Küçük bek tespiti
            cv2.putText(image, f'Kucuk Bek : {i[2]}', (i[0] - 70, i[1] - i[2] - 50), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

        # Tespit edilen dairenin merkezini küçük bir kırmızı nokta ile işaretleriz
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

    # Tüm maskeler birleştirilerek nihai maskeli görüntü elde edilir
    result = cv2.bitwise_and(image, combined_mask)

    # Tespit edilen dairelerin özelliklerini (merkez ve yarıçap bilgileri) yazdırıyoruz
    print(circles)

    # Tespit edilen dairelerin sayısını belirliyoruz
    matris = circles[0]
    satir_sayisi = matris.shape[0]
    print("Tespit edilen toplam bek sayisi:", satir_sayisi)

    # Tüm tespit edilen bekler üzerinde işlemler yapılır
    for x in range(satir_sayisi):
        r = circles[0][x][2]  # Bekin yarıçapı alınır

        # En büyük bek üzerinde işlemler yapılır
        if 85 < r < 100:
            cx, cy = circles[0][x][0], circles[0][x][1]
            r = np.uint16(np.around(r * 1.3))  # Bekin boyutu genişletilir
            top_left = (cx - r, cy - r)
            bottom_right = (cx + r, cy + r)
            cv2.putText(result, "En Buyuk Bek", (cx - r, cy + r + 30), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
            cv2.rectangle(result, top_left, bottom_right, (255, 0, 0), 2)

        # Orta boy bek için işlemler yapılır
        elif 45 < r < 55:
            cx, cy = circles[0][x][0], circles[0][x][1]
            r = np.uint16(np.around(r * 1.5))
            top_left = (cx - r, cy - r)
            bottom_right = (cx + r, cy + r)
            cv2.rectangle(result, top_left, bottom_right, (255, 0, 0), 2)
            cv2.putText(result, "Orta Bek", (cx - r, cy + r + 30), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

        # Küçük bek için işlemler yapılır
        elif 30 < r < 44:
            cx, cy = circles[0][x][0], circles[0][x][1]
            r = np.uint16(np.around(r * 1.8))
            top_left = (cx - r, cy - r)
            bottom_right = (cx + r, cy + r)
            cv2.rectangle(result, top_left, bottom_right, (255, 0, 0), 2)
            cv2.putText(result, "Kucuk Bek", (cx - r, cy + r + 30), 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

    # Nihai sonucu içeren görüntü ekranda gösterilir
    cv2.imshow('Sonuc', result)

# Klavye girdisi beklenir ve tüm pencereler kapatılır
cv2.waitKey(0)
cv2.destroyAllWindows()
