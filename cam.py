import cv2
import numpy as np
import sys
import time

net = cv2.dnn.readNetFromONNX("yolov8n-seg.onnx")
latest_frame = None
demoMode = True

def startCam():
    global latest_frame, demoMode

    if sys.platform.startswith('win'):
        print("[INFO] Запуск на Windows. Поиск доступной камеры...")
        cap = None
        for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF]:
            for idx in [0, 1, 2, 3]:
                cap = cv2.VideoCapture(idx, backend)
                if cap.isOpened():
                    print(
                        f"[INFO] Успешно подключено! Индекс: {idx}, Бэкенд: {'DSHOW' if backend == cv2.CAP_DSHOW else 'MSMF'}")
                    break
            if cap and cap.isOpened():
                break

    else:
        print("[INFO] Запуск на Linux/Raspberry Pi.")
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not cap.isOpened():
            for idx in [2, 4, 1]:
                print(f"[INFO] Индекс 0 недоступен. Пробуем индекс {idx}...")
                cap = cv2.VideoCapture(idx, cv2.CAP_V4L2)
                if cap.isOpened():
                    print(f"[INFO] Успешно подключено к камере на индексе {idx}!")
                    break

    if not cap.isOpened():
        print("[ERROR] Камера недоступна.")
        return

    colors = np.random.randint(0, 255, size=(80, 3), dtype="uint8")

    while True:
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

        preds = np.squeeze(outputs[0])
        preds = preds.T

        boxes, confs, class_ids = [], [], []

        for i in range(len(preds)):
            row = preds[i]
            classes_scores = row[4:84]
            _, score, _, maxLoc = cv2.minMaxLoc(classes_scores)

            # class_id = maxLoc[0]
            class_id = maxLoc[0] if isinstance(maxLoc, (tuple, list)) else maxLoc

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

        if sys.platform.startswith('win') or demoMode:
            cv2.imshow("ELCamera", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        elapsed_time = time.time() - start_time
        sleep_time = 1.0 - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)

    cap.release()
    if sys.platform.startswith('win') or demoMode:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    startCam()
