import asyncio, threading, sys, os, uvicorn
sys.path.append(os.path.dirname(__file__))

# from audi.au2Txt import *
# from audi.aiTxt import *
from cam import startCam
from PFBP import *
from webSer import app

async def start():
    # await asyncio.to_thread(loadModel)
    cam_thread = threading.Thread(target=startCam, daemon=True)
    cam_thread.start()

    # await mdlIni()
    # lMt = threading.Thread(target=loadModel, daemon=True)
    # lMt.start()
    # await loadModel()

    # await strLst()

    print("[INFO] Запуск веб-сервера на http://raspberrypi.local:5000")
    await asyncio.to_thread(uvicorn.run, app, host="0.0.0.0", port=5000, log_level="info")

asyncio.run(start())