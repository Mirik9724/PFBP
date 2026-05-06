import asyncio
import threading
import sys
import os

sys.path.append(os.path.dirname(__file__))

# from audi.au2Txt import *
# from audi.aiTxt import *
# from listenCmd import listC
from cam import startCam
from PFBP import *

async def start():
    # await asyncio.to_thread(loadModel)
    cam_thread = threading.Thread(target=lambda: asyncio.run(startCam()), daemon=True)
    cam_thread.start()
    #
    # listC()

    # await mdlIni()
    # lMt = threading.Thread(target=loadModel, daemon=True)
    # lMt.start()
    # await loadModel()

    # await strLst()

    # move(True, True)
    # speed(50)
    # await asyncio.sleep(1)
    #
    # move(False, False)
    # speed(50)
    # await asyncio.sleep(1)
    # stop()
    while cam_thread.is_alive():
        await asyncio.sleep(1)

asyncio.run(start())