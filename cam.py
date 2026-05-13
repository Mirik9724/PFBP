import cv2
import numpy as np
import sys
import time

net = cv2.dnn.readNetFromONNX("yolov8n-seg.onnx")
latest_frame = None


def startCam():
    global latest_frame

    if sys.platform.startswith('win'):
        print("[INFO] Запуск на Windows.")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        print("[INFO] Запуск на Linux/Raspberry Pi.")
        cap = cv2.VideoCapture(1, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("[ERROR] Камера недоступна.")
        return

    colors = np.random.randint(0, 255, size=(80, 3), dtype="uint8")

    while True:
        # Засекаем время начала цикла обработки
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (640, 640), (0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)

        output_names = net.getUnconnectedOutLayersNames()
        outputs = net.forward(output_names)

        preds = np.squeeze(outputs)
        preds = preds.T

        boxes, confs, class_ids = [], [], []

        for i in range(len(preds)):
            row = preds[i]
            classes_scores = row[4:84]
            _, score, _, maxLoc = cv2.minMaxLoc(classes_scores)
            class_id = maxLoc

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

        _, encoded_img = cv2.imencode('.jpg', frame)
        latest_frame = encoded_img.tobytes()

        if sys.platform.startswith('win'):
            cv2.imshow("ELCamera", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Вычисляем, сколько времени заняла детекция
        elapsed_time = time.time() - start_time

        # Динамическая пауза: спим ровно столько, сколько осталось до 1 секунды
        sleep_time = 1.0 - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

    cap.release()
    if sys.platform.startswith('win'):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    startCam()
