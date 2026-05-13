import cv2
import numpy as np
import asyncio

net = cv2.dnn.readNetFromONNX("yolov8n-seg.onnx")

latest_frame = None

async def startCam():
    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    # cap = cv2.VideoCapture(0)
    colors = np.random.randint(0, 255, size=(80, 3), dtype="uint8")

    while True:
        ret, frame = cap.read()
        if not ret: break

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
            # Исправленное получение индекса класса:
            _, score, _, maxLoc = cv2.minMaxLoc(classes_scores)
            class_id = maxLoc[0]  # Индекс столбца и есть ID класса

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
        global latest_frame
        latest_frame = encoded_img.tobytes()

        cv2.imshow('AI Vision OpenCV', frame)
        await asyncio.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(startCam())
