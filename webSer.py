
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

# @app.get("/camera_frame")
# async def get_camera_frame():
#     if cam.latest_frame is None:
#         return Response(content="Кадр еще не подготовлен нейросетью", status_code=503)
#
#     return Response(content=cam.latest_frame, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
