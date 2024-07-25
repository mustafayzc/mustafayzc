from ultralytics import YOLO
import cv2

# Eğitilmiş model dosyasını yükleyin
model = YOLO("runs/detect/train/weights/best.pt")

# Fotoğraf dosyasının yolu
image_path = "11.jpg"

# Görüntüyü yükleyin
image = cv2.imread(image_path)
image=cv2.resize(image,(640,640))

# Modeli kullanarak nesne tespiti yapın
results = model.predict(image)

# Tespit edilen nesneler için sonuçları işleyin
for result in results:
    boxes = result.boxes.xyxy.cpu().numpy()  # Tespit edilen nesnelerin kutuları
    scores = result.boxes.conf.cpu().numpy()  # Her bir tespitin güven skorları
    classes = result.boxes.cls.cpu().numpy()  # Sınıf id'leri
    
    for box, score, cls in zip(boxes, scores, classes):
        if score > 0.2:  # Güven skoru eşiği, daha fazla hassasiyet için ayarlanabilir
            x1, y1, x2, y2 = map(int, box)  # Kutu koordinatlarını int'e çevirin
            label = f"{model.names[int(cls)]}: {score:.2f}"  # Sınıf ismi ve güven skoru
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Kutu çizimi
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Sonucu gösterin
cv2.imshow('YOLO Object Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
