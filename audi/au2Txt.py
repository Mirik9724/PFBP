import sounddevice as sd
import vosk
import queue
import json
import os

# ---------------- CONFIG ----------------

WAKE_WORD = "эль прима"
SAMPLERATE = 16000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

# ----------------------------------------

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


# ✅ Загружаем модель
model = vosk.Model(MODEL_PATH)
rec = vosk.KaldiRecognizer(model, SAMPLERATE)

print(f"Слушаю... (скажите '{WAKE_WORD}')")


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
                    rec.Reset()

            else:
                partial = json.loads(rec.PartialResult())
                text = partial.get("partial", "").lower()

                # 🔥 можно убрать если спамит
                # print(text)

                if WAKE_WORD in text:
                    print(">>> Wake word обнаружено!")
                    rec.Reset()

except KeyboardInterrupt:
    print("\nОстановлено.")