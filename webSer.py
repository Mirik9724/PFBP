import uvicorn, sys, os, asyncio
from fastapi import FastAPI, Response, Query, HTTPException
from starlette import status
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

SECRET_CODE = "0000"

def check_security(code: str):
    if code != SECRET_CODE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверный код безопасности"
        )

@app.get("/")
async def joystick_page():
    return FileResponse("main.html")

@app.get("/s")
async def stop_robot(code: str = Query(default="")):
    check_security(code)
    stop()
    return {"status": "stop"}

@app.get("/f")
async def forward(speed_val: int = Query(default=100, alias="speed"),code: str = Query(default="")):
    check_security(code)
    speed(speed_val)
    move(True, True)
    return {"status": "f", "speed": speed_val}

@app.get("/b")
async def back(speed_val: int = Query(default=100, alias="speed"),code: str = Query(default="")):
    check_security(code)
    speed(speed_val)
    move(False, False)
    return {"status": "b", "speed": speed_val}

@app.get("/r")
async def right(speed_val: int = Query(default=100, alias="speed"),code: str = Query(default="")):
    check_security(code)
    speed(speed_val)
    move(True, False)
    return {"status": "r", "speed": speed_val}

@app.get("/l")
async def left(speed_val: int = Query(default=100, alias="speed"),code: str = Query(default="")):
    check_security(code)
    speed(speed_val)
    move(False, True)
    return {"status": "l", "speed": speed_val}

@app.get("/camera_frame")
async def get_camera_frame():
    if cam.latest_frame is None:
        return Response(content="Кадр еще не подготовлен нейросетью", status_code=503)
    return Response(content=cam.latest_frame, media_type="image/jpeg", headers=NO_CACHE_HEADERS)

async def video_stream_generator():
    while True:
        if cam.latest_frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cam.latest_frame + b'\r\n')
        await asyncio.sleep(0.03)

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(video_stream_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
