import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BCM)

for i in (23, 24, 17, 27, 5, 6):
    gp.setup(i, gp.OUT)

lSp = gp.PWM(5, 100)
rSp = gp.PWM(6, 100)
rSp.start(0)
lSp.start(0)

lCof = 1.0
rCof = 0.9

def speed(sp):
    base_val = max(0, min(100, sp))

    left_val = max(0, min(100, base_val * lCof))
    lSp.ChangeDutyCycle(left_val)

    right_val = max(0, min(100, base_val * rCof))
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
