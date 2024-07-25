from ultralytics import YOLO
import cv2

# Eğitilmiş model dosyasını yükleyin
model = YOLO("runs/detect/train/weights/best.pt")

# Video dosyasının yolu
video_path = "25.mp4"

# VideoCapture ile videoyu okuyun
cap = cv2.VideoCapture(video_path)

# Videonun her karesi için nesne tespiti yapın
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Modeli kullanarak nesne tespiti yapın
    results = model.predict(frame)
    
    # Tespit edilen nesneler için sonuçları işleyin
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Tespit edilen nesnelerin kutuları
        scores = result.boxes.conf.cpu().numpy()  # Her bir tespitin güven skorları
        classes = result.boxes.cls.cpu().numpy()  # Sınıf id'leri
        
        for box, score, cls in zip(boxes, scores, classes):
            if score > 0.2:  # Güven skoru eşiği, daha fazla hassasiyet için ayarlanabilir
                x1, y1, x2, y2 = map(int, box)  # Kutu koordinatlarını int'e çevirin
                label = f"{model.names[int(cls)]}: {score:.2f}"  # Sınıf ismi ve güven skoru
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Kutu çizimi
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # İşlenen kareyi ekranda gösterin
    cv2.imshow('YOLO Object Detection', frame)

    # 'q' tuşuna basarak çıkış yapın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakın
cap.release()
cv2.destroyAllWindows()
