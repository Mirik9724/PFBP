import asyncio
import threading
import sys
import os
sys.path.append(os.path.dirname(__file__))

from cam import startCam
from audi.au2Txt import *
from audi.aiTxt import *

async def start():
    await asyncio.to_thread(loadModel)
    cam_thread = threading.Thread(target=startCam, daemon=True)
    cam_thread.start()



    # await mdlIni()
    # lMt = threading.Thread(target=loadModel, daemon=True)
    # lMt.start()
    # await loadModel()

    # await strLst()

asyncio.run(start())