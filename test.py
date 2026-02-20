import sys
import os
sys.path.append(os.path.dirname(__file__))

import asyncio
from audi.aiTxt import *

asyncio.run(loadModel())