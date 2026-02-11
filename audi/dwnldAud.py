import os
import urllib.request
import zipfile

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"
MODEL_DIR = "model"
ZIP_FILE = "model.zip"


def download_model():
    if os.path.exists(MODEL_DIR):
        print("Модель уже есть 👍")
        return

    print("Скачиваю модель...")
    urllib.request.urlretrieve(MODEL_URL, ZIP_FILE)

    print("Распаковываю...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall()

    # внутри архива имя длинное → переименуем
    extracted_folder = "vosk-model-small-ru-0.22"
    os.rename(extracted_folder, MODEL_DIR)

    os.remove(ZIP_FILE)

    print("Модель готова 🚀")


download_model()