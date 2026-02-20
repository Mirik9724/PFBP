import serial
from PFBP import *

# Подключение к Serial порту (тот же /dev/rfcomm0)
ser = serial.Serial('/dev/rfcomm0', 9600)

print("Ожидаю команды...")

async def listC():
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(1)  # читаем 1 байт
                if data == 'W':
                    move(True, True);
                    speed(80)
                elif data == 'S':
                    move(False, False);
                    speed(80)
                elif data == 'A':
                    move(False, True);
                    speed(60)
                elif data == 'D':
                    move(True, False);
                    speed(60)
                elif data == 'X' or data == 'Z':
                    stop()


except KeyboardInterrupt:
    print("Завершение работы")

ser.close()