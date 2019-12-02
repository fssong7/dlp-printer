import pygame
import os
import RPi.GPIO as gpio

pygame.init()

ena = 2
ms1 = 3
ms2 = 4
ms3 = 17
step = 27
direc = 22
lim = 10

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(ena,gpio.OUT)
gpio.setup(ms1,gpio.OUT)
gpio.setup(ms2,gpio.OUT)
gpio.setup(ms3,gpio.OUT)
gpio.setup(step,gpio.OUT)
gpio.setup(direc,gpio.OUT)
gpio.setup(lim,gpio.IN)

curetime = 5000
display_width = 800
display_height = 600

path = "/home/pi/Desktop/slices"
dirs = os.listdir( path )
fileNum = 0

for file in dirs:
    fileNum+=1
    #print(fileNum)

gameDisplay = pygame.display.set_mode((display_width,display_height))#,pygame.FULLSCREEN)
pygame.display.set_caption('bad news bears')

#x = True
limSwitch = gpio.input(lim)
#print(limSwitch)

#while x:
#   limSwitch = gpio.input(lim)
#    print(limSwitch)
#    if limSwitch == 0:
#        x = False

black = (0,0,0)
white = (255,255,255)


def image(x,y):
    gameDisplay.blit(layerImg, (x,y))
    
def stepforward():
    #limSwitch = gpio.input(lim)
    #while not limSwitch:
        gpio.output(direc,False)
        x = 0;
        while x < 1000:
            gpio.output(step,True)
            pygame.time.delay(1)
            gpio.output(step,False)
            pygame.time.delay(1)
            x = x+1

def stepbackward():
    #limSwitch = gpio.input(lim)
    #while not limSwitch:
        gpio.output(direc,True)
        x = 0;
        while x < 1000:
            gpio.output(step,True)
            pygame.time.delay(1)
            gpio.output(step,False)
            pygame.time.delay(1)
            x = x+1
        
x = 0#(display_width * 0.45)
y = 0#(display_height * 0.8)
layer = 1

def reset():
    gpio.output(ena,True)
    gpio.output(ms1,False)
    gpio.output(ms2,False)
    gpio.output(ms3,False)
    gpio.output(step,False)
    gpio.output(direc,False)

gpio.output(ena,False)

while layer <= fileNum:
    if layer <= 10:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out000'+str(layer-1)+'.png')
    elif layer <= 100:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out00'+str(layer-1)+'.png')
    else:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out0'+str(layer-1)+'.png')
    layerImg = pygame.transform.scale(layerImg,(800,600))
    
    limSwitch = gpio.input(lim)
    #if not (limSwitch == 0):
        #if layer % 2 != 0:
           # stepforward()
        #else:
          #  stepbackward()
    #else:
       # break
    stepforward()
    #pygame.time.delay(curetime)
    pygame.display.set_caption('Layer Number: ' + str(layer))
    gameDisplay.fill(black)
    pygame.display.update()
    
    image(0,0)
    pygame.display.update()
    pygame.time.delay(curetime)
    gameDisplay.fill(black)
    pygame.display.update()
    
    stepbackward()
    pygame.time.delay(1000)

    layer = layer + 1
    
reset()
pygame.quit()
quit()