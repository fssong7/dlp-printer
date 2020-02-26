import time
import RPi.GPIO as gpio #importing GPIO pins for setup

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

lim = 10
gpio.setup(lim,gpio.IN)

counter = 1

while True:
    inputState = gpio.input(lim)
    if inputState == False:
        print('Activating limiters',counter)
        counter += 1
        time.sleep(0.2)