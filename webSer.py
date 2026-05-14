import uvicorn, sys, os, asyncio
from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, StreamingResponse

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

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0"
}

@app.get("/camera_frame")
async def get_camera_frame():
    if cam.latest_frame is None:
        return Response(content="Кадр еще не подготовлен нейросетью", status_code=503)
    return Response(content=cam.latest_frame, media_type="image/jpeg", headers=NO_CACHE_HEADERS)


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

# Вариант А: Получение одиночного кадра (Обновлено)
@app.get("/camera_frame")
async def get_camera_frame():
    if cam.latest_frame is None:
        return Response(content="Кадр еще не подготовлен нейросетью", status_code=503)
    return Response(content=cam.latest_frame, media_type="image/jpeg", headers=NO_CACHE_HEADERS)

# Вариант Б: Функция-генератор для плавного MJPEG потока видео без перезагрузки страниц
async def video_stream_generator():
    while True:
        if cam.latest_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cam.latest_frame + b'\r\n')
        await asyncio.sleep(0.03) # Ограничение ~30 FPS для разгрузки процессора

# Вариант Б: Эндпоинт для плавной потоковой передачи видео
@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(video_stream_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
