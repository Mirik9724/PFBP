import asyncio
import threading
import sys
import os
sys.path.append(os.path.dirname(__file__))

# from cam import startCam
# from audi.au2Txt import *
# from audi.aiTxt import *
# from listenCmd import listC
from PFBP import *

async def start():
    # await asyncio.to_thread(loadModel)
    # cam_thread = threading.Thread(target=startCam, daemon=True)
    # cam_thread.start()
    #
    # listC()

    # await mdlIni()
    # lMt = threading.Thread(target=loadModel, daemon=True)
    # lMt.start()
    # await loadModel()

    # await strLst()

    move(True, True)
    speed(10)
    await asyncio.sleep(1)

    move(False, False)
    speed(10)
    await asyncio.sleep(1)

    stop()

asyncio.run(start())