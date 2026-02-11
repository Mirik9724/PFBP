import cv2
import numpy as np
from ultralytics import YOLO
import asyncio

# Важно: используем модель сегментации
model = YOLO('yolov8n-seg.pt')


async def startCam():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret: break

        results = model(frame, stream=True)

        for r in results:
            # Проверяем, есть ли маски (контуры)
            if r.masks is not None:
                for mask, box in zip(r.masks.xy, r.boxes):
                    # Масштабируем и переводим координаты контура в формат int32
                    polygon = np.array(mask, dtype=np.int32)

                    # Рисуем сам контур
                    cv2.polylines(frame, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

                    # Добавляем текст над объектом
                    cls = int(box.cls[0])
                    name = model.names[cls]
                    cv2.putText(frame, name, tuple(polygon[0]),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('AI Vision Seg', frame)
        if cv2.waitKey(1) & 0xFF == 27: break
        await asyncio.sleep(0.01)

        cv2.waitKey(100)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import asyncio

    asyncio.run(startCam())
