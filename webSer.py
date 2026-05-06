from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import sys, os
import requests
import socket

from starlette.responses import FileResponse

sys.path.append(os.path.dirname(__file__))
from PFBP import *

app = FastAPI()

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
    return FileResponse("index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
