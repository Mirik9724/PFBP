import PySimpleGUI as sg
import serial
import time

# Подключение к COM-порту Windows (например COM5)
ser = serial.Serial('COM5', 9600)
time.sleep(2)

layout = [
    [sg.Button('Вперёд', key='W')],
    [sg.Button('Влево', key='A'), sg.Button('Стоп', key='X'), sg.Button('Вправо', key='D')],
    [sg.Button('Назад', key='S')],
    [sg.Button('Выход')]
]

window = sg.Window('Управление роботом', layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Выход'):
        break
    if event in ['W','A','S','D','X']:
        ser.write(event.encode())
        print(f"Отправлено: {event}")

window.close()
ser.close()