
import uvicorn, sys, os
from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

sys.path.append(os.path.dirname(__file__))
from PFBP import *
import cam

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import StreamingResponse
import asyncio

# Функция-генератор кадров из памяти модуля cam
async def frame_generator():
    while True:
        if cam.latest_frame is not None:
            # Отдаем кадр в формате чанка multipart/x-mixed-replace
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cam.latest_frame + b'\r\n')
        # Ограничиваем частоту опроса буфера памяти (примерно 30 FPS максимум)
        await asyncio.sleep(0.03)

@app.get("/camera_stream")
async def camera_stream():
    # Нативный MJPEG стрим, который браузеры умеют воспроизводить на лету
    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/s")
async def stop_robot():
    stop()
    return {"status": "stop"}

@app.get("/f")
async def forward():
    move(True, True); speed(50)
    return {"status": "f"}

@app.get("/b")
async def back():
    move(False, False); speed(50)
    return {"status": "b"}

@app.get("/r")
async def right():
    move(True, False); speed(50)
    return {"status": "r"}

@app.get("/l")
async def left():
    move(False, True); speed(50)
    return {"status": "l"}

@app.get("/")
async def joystick_page():
    return FileResponse("main.html")

# @app.get("/camera_frame")
# async def get_camera_frame():
#     if cam.latest_frame is None:
#         return Response(content="Кадр еще не подготовлен нейросетью", status_code=503)
#
#     return Response(content=cam.latest_frame, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
