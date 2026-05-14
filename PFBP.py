import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BCM)

for i in (23, 24, 17, 27, 5, 6):
    gp.setup(i, gp.OUT)

lSp = gp.PWM(5, 100)
rSp = gp.PWM(6, 100)
rSp.start(0)
lSp.start(0)

# Коэффициент скорости для ПРАВОГО мотора (от 0.0 до 1.0)
# Настройте это значение под себя: 0.85 означает, что правый мотор будет работать на 15% медленнее левого
RIGHT_MOTOR_CORRECTION = 0.85


def speed(sp):
    # Ограничиваем входящее значение от 0 до 100
    base_val = max(0, min(100, sp))

    # Левый мотор работает на полной базовой скорости
    lSp.ChangeDutyCycle(base_val)

    # Скорость правого мотора искусственно занижается на коэффициент
    # Округляем до целого числа, так как ChangeDutyCycle принимает int/float
    right_val = max(0, min(100, base_val * RIGHT_MOTOR_CORRECTION))
    rSp.ChangeDutyCycle(right_val)


def move(Lft, Rgt):
    if Lft == True:
        gp.output(17, 1)
        gp.output(27, 0)
    else:
        gp.output(17, 0)
        gp.output(27, 1)

    if Rgt == True:
        gp.output(23, 1)
        gp.output(24, 0)
    else:
        gp.output(23, 0)
        gp.output(24, 1)


def stop():
    gp.output(23, 0)
    gp.output(24, 0)
    gp.output(17, 0)
    gp.output(27, 0)
    speed(0)
