import cv2
import numpy as np

# "stove5.jpg" adlı görüntüyü okuma.
image = cv2.imread("stove5.jpg")

# Görüntüyü belirli bir boyuta yeniden boyutlandırma (390x530). 
# Bu işlem, görüntü üzerinde daha hızlı ve verimli işlem yapmak için kullanılır.
image = cv2.resize(image, (390, 530))

# Maske oluşturmak için, görüntüyle aynı boyutlarda tamamen siyah bir görüntü oluşturuluyor.
mask = np.zeros_like(image)

# İlk maske: Görüntünün merkezinde (203, 270) koordinatlarında 185 yarıçaplı bir daire oluşturuluyor.
# Daire içindeki pikseller beyaza (255, 255, 255) boyanıyor.
cv2.circle(mask, (203, 270), 185, (255, 255, 255), -1)

# İlk maske kullanılarak görüntüyle çarpma işlemi yapılır. Bu işlem sadece dairenin içinde kalan pikselleri korur.
masked_img = cv2.bitwise_and(image, mask)

# İkinci maske: İlk maskeye benzer, ancak daire yarıçapı daha küçüktür (155).
mask2 = np.zeros_like(image)
cv2.circle(mask2, (203, 270), 155, (255, 255, 255), -1)

# İkinci maskeye göre görüntüyle çarpma işlemi yapılır. Yine sadece dairenin içindeki pikseller korunur.
masked2 = cv2.bitwise_and(image, mask2)

# İki maskeli görüntü arasındaki fark alınır.
# Bu işlem, iki daire arasındaki bölgeyi çıkartmak için kullanılır.
frame = cv2.bitwise_xor(masked2, masked_img)

# Görüntü BGR renk formatından HSV renk formatına dönüştürülür.
# HSV, renk tonlarını (Hue), doygunluğu (Saturation) ve parlaklığı (Value) ayırdığı için 
# renk tespitinde daha etkili bir formattır.
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Mavi renk tonlarını tanımlamak için alt ve üst HSV aralığı belirlenir.
# Bu aralık alev rengini tespit etmek için optimize edilmiştir.
lower_blue = np.array([0, 0, 206])  # Alt sınır: Parlak beyaz tonları
upper_blue = np.array([179, 255, 255])  # Üst sınır: Beyazın en parlak hali

# HSV görüntüde belirtilen renk aralığındaki pikselleri tespit etmek için bir maske oluşturulur.
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

# Morfolojik işlemler için küçük bir 2x2 boyutunda bir çekirdek (kernel) oluşturulur.
kernel = np.ones((2, 2), np.uint8)

# Maskeyi genişletmek (dilate) için morfolojik genişletme işlemi uygulanır.
# Bu işlem, küçük boşlukları kapatır ve nesneleri daha belirgin hale getirir.
dilated_mask = cv2.dilate(mask_blue, kernel, iterations=3)

# Maskeyi küçültmek (erode) için morfolojik aşındırma işlemi uygulanır.
# Bu işlem, görüntüdeki küçük gürültüleri azaltır.
eroded_mask = cv2.erode(dilated_mask, kernel, iterations=1)

# İşlenen maskeyi ekranda gösterme. Kullanıcıya hangi bölgelerin tespit edildiğini görme imkanı verir.
cv2.imshow("Maske", eroded_mask)

# Görüntüdeki konturları (nesne kenarlarını) tespit etmek için `findContours` fonksiyonu kullanılır.
# `RETR_EXTERNAL`: Sadece dış konturları tespit eder.
# `CHAIN_APPROX_SIMPLE`: Konturları basitleştirir ve gereksiz noktaları kaldırır.
contours, _ = cv2.findContours(eroded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Tespit edilen konturları yeşil renk ile görüntüye çizer.
cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

# Tespit edilen konturların sayısını alır ve bu sayı, algılanan alevlerin sayısını gösterir.
alev_sayisi = len(contours)

# Görüntünün üzerine tespit edilen alev sayısını yazdırır.
# Yazı rengi mavi (255, 0, 0), yazı tipi `FONT_HERSHEY_SIMPLEX`, boyut 1 ve kalınlık 2'dir.
cv2.putText(frame, f'Alev Sayisi: {alev_sayisi}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# Konturlarla işaretlenmiş son görüntüyü ekranda gösterir.
cv2.imshow("Orijinal", frame)

# Tespit edilen konturları orijinal görüntü üzerine de çizer.
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Orijinal görüntüyü, konturlar ile birlikte gösterir.
cv2.imshow("image", image)

# Görüntülerin açık kalması ve kullanıcı tarafından kapatılmasını sağlamak için bekler.
cv2.waitKey(0)

# Tüm açık pencereyi kapatır.
cv2.destroyAllWindows()
