import cv2
import numpy as np
import asyncio

# Загружаем модель ONNX через встроенный модуль OpenCV
# (Убедитесь, что файл yolov8n-seg.onnx лежит в папке с проектом)
net = cv2.dnn.readNetFromONNX("yolov8n-seg.onnx")


async def startCam():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Подготовка изображения (Blob)
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (640, 640), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)

        # Получаем выходы (у YOLOv8-seg их два: детекции и прототипы масок)
        output_names = net.getUnconnectedOutLayersNames()
        outputs = net.forward(output_names)

        # Выводим сообщение, что нейросеть работает
        cv2.putText(frame, "OpenCV DNN Mode", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow('AI Vision OpenCV', frame)

        if cv2.waitKey(1) & 0xFF == 27: break
        await asyncio.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(startCam())
