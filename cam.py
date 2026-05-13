import cv2
import numpy as np
import sys
import time

# Инициализация модели
net = cv2.dnn.readNetFromONNX("yolov8n-seg.onnx")


def startCam():
    if sys.platform.startswith('win'):
        print("[INFO] Запуск на Windows.")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        print("[INFO] Запуск на Linux/Raspberry Pi.")
        cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    if not cap.isOpened():
        print("[ERROR] Камера недоступна.")
        return

    colors = np.random.randint(0, 255, size=(80, 3), dtype="uint8")
    print("[INFO] Камера успешно запущена. Начинаем обработку...")

    # Обычный синхронный цикл (ФИКС ЗАВИСАНИЯ)
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (640, 640), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)

        output_names = net.getUnconnectedOutLayersNames()

        # Теперь вызов выполняется в синхронном потоке и не вешает планировщик asyncio
        outputs = net.forward(output_names)

        # ФИКС ИНДЕКСАЦИИ: Забираем только детекции (первый элемент кортежа из YOLOv8-seg)
        preds = np.squeeze(outputs[0])
        preds = preds.T

        boxes, confs, class_ids = [], [], []

        for i in range(len(preds)):
            row = preds[i]
            classes_scores = row[4:84]
            _, score, _, maxLoc = cv2.minMaxLoc(classes_scores)
            class_id = maxLoc[0]

            if score > 0.5:
                cx, cy, cw, ch = row[0:4]
                x = int((cx - cw / 2) * (w / 640))
                y = int((cy - ch / 2) * (h / 640))
                bw = int(cw * (w / 640))
                bh = int(ch * (h / 640))

                boxes.append([x, y, bw, bh])
                confs.append(float(score))
                class_ids.append(int(class_id))

        indices = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)

        if len(indices) > 0:
            for i in indices.flatten():
                x, y, bw, bh = boxes[i]
                cid = class_ids[i]
                color = colors[cid % 80].tolist()

                cv2.rectangle(frame, (x, y), (x + bw, y + bh), color, 2)
                label = f"ID:{cid} {confs[i]:.2f}"
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Сохраняем готовый снимок на диск для webSer.py
        cv2.imwrite("temp_frame.jpg", frame)

        if sys.platform.startswith('win'):
            cv2.imshow("ELCamera", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Небольшая задержка, чтобы CPU малинки не грелся до 100%
        time.sleep(0.01)

    cap.release()
    if sys.platform.startswith('win'):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        startCam()
    except KeyboardInterrupt:
        print("[INFO] Скрипт остановлен пользователем.")
