import sounddevice as sd
import vosk
import queue
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))

from aiTxt import *

# ---------------- CONFIG ----------------

WAKE_WORD = "бот"
SAMPLERATE = 16000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

# ----------------------------------------

audio_queue = queue.Queue()
rec = None
model = None

async def handle_wake_word(command_text):
    print(f">>> Команда после wake word: {command_text}")
    response = await useBot(command_text)
    print("Bot:", response)

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


async def mdlIni():
    global model, rec
    model = vosk.Model(MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, SAMPLERATE)

print(f"Слушаю... (скажите '{WAKE_WORD}')")

async def strLst():
    try:
        with sd.RawInputStream(
            samplerate=SAMPLERATE,
            blocksize=4000,      # 🔥 меньше = ниже задержка
            dtype='int16',
           channels=1,
         callback=audio_callback
        ):

            while True:
                data = audio_queue.get()

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").lower()

                    if text:
                        print("Вы сказали:", text)

                    if WAKE_WORD in text:
                        print(">>> Wake word обнаружено!")

                        # 🔥 получаем текст после wake word
                        command = text.split(WAKE_WORD, 1)[1].strip()

                        await handle_wake_word(command)

                        rec.Reset()

                else:
                   partial = json.loads(rec.PartialResult())
                   text = partial.get("partial", "").lower()

                   if WAKE_WORD in text:
                        print(">>> Wake word обнаружено!")

                        command = text.split(WAKE_WORD, 1)[1].strip()

                        await handle_wake_word(command)

                        rec.Reset()
            await asyncio.sleep(0)

    except KeyboardInterrupt:
       print("\nОстановлено.")