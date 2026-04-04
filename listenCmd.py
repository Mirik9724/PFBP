import serial
from PFBP import *
import asyncio

# Подключение к Serial порту (тот же /dev/rfcomm0)
ser = serial.Serial('/dev/rfcomm0', 9600)

print("Ожидаю команды...")

async def listC():
    if not ser: return  # Если порт не открылся, выходим

    try:
        while True:
            if ser.in_waiting > 0:
                # Декодируем байты в строку, чтобы сравнение работало
                data = ser.read(1).decode('utf-8')

                if data == 'W':
                    move(True, True)
                    speed(80)
                elif data == 'S':
                    move(False, False)
                    speed(80)
                elif data == 'A':
                    move(False, True)
                    speed(60)
                elif data == 'D':
                    move(True, False)
                    speed(60)
                elif data == 'X' or data == 'Z':
                    stop()

            await asyncio.sleep(0.01)

    except KeyboardInterrupt:
        print("Завершение работы")

    finally:
        ser.close()