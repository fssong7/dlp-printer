#Full code for stepper movement/limit switch control, projection 

import pygame #for projecting images to HDMI
import os
import RPi.GPIO as gpio #importing GPIO pins for setup

pygame.init() #initializing image projection software

#defining GPIO pins
ena = 2
ms1 = 3
ms2 = 4
ms3 = 17
step = 27
direc = 22
topLim = 10
botLim = 9

#set to bcm mode for pin definition
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#setting gpio pins to output or input
gpio.setup(ena,gpio.OUT)
gpio.setup(ms1,gpio.OUT)
gpio.setup(ms2,gpio.OUT)
gpio.setup(ms3,gpio.OUT)
gpio.setup(step,gpio.OUT)
gpio.setup(direc,gpio.OUT)
gpio.setup(topLim,gpio.IN)
gpio.setup(botLim,gpio.IN)

#defining curetime in milliseconds
curetime = 5000

#defining desired layer height
layerHeight = 0.150

#to convert from mm to steps, multiply by this factor
distanceToSteps = 40.1


#defining size of image cured
display_width = 800
display_height = 800

#setting location of sliced images
path = "/home/pi/Desktop/slices"
dirs = os.listdir( path )
fileNum = 0

#counting the total number of images, equal to number of layers to cure
for file in dirs:
    fileNum+=1

#initializes projection
gameDisplay = pygame.display.set_mode((display_width,display_height))#,pygame.FULLSCREEN)
pygame.display.set_caption('Initializing Print')

#defining color RGB values
black = (0,0,0)
white = (255,255,255)

#projecting the image
def image(x,y):
    gameDisplay.blit(layerImg, (x,y))

#moving the stepper motor down
#distance is in mm
def stepforward(distance):
    gpio.output(direc,False)
    x = 0;
    while x < distance * distanceToSteps:
        gpio.output(step,True)
        pygame.time.delay(1)
        gpio.output(step,False)
        pygame.time.delay(1)
        x += 1

#moving the stepper motor up
#distance is in mm
def stepbackward(distance):
    gpio.output(direc,True)
    x = 0;
    while x < distance * distanceToSteps:
        gpio.output(step,True)
        pygame.time.delay(1)
        gpio.output(step,False)
        pygame.time.delay(1)
        x += 1

#moving stepper down until hits bot limit switch
def motorCalibrate():
    gpio.output(direc,False)
    inputState = gpio.input(botLim)
    while inputState = False:
        gpio.output(step,True)
        pygame.time.delay(5)
        gpio.output(step,False)
        pygame.time.delay(5)
        inputState = gpio.input(botLim)
    reset()
    gpio.output(ena,False)

#moving stepper up until hits top limit switch
def motorHome():
    gpio.output(direc,True)
    inputState = gpio.input(topLim)
    while inputState = False:
        gpio.output(step,True)
        pygame.time.delay(5)
        gpio.output(step,False)
        pygame.time.delay(5)
        inputState = gpio.input(topLim)
    reset()
    gpio.output(ena,False)

#turning motor off
def reset():
    gpio.output(ena,True)
    gpio.output(ms1,False)
    gpio.output(ms2,False)
    gpio.output(ms3,False)
    gpio.output(step,False)
    gpio.output(direc,False)

#defining x and y coordinates (upper left) of image projected
x = 0
y = 0

layer = 1 #first layer
gpio.output(ena,False) #enable motors for movement
gameDisplay.fill(black) #display black screen 
pygame.display.update()

#home position (top limit switch)
#stepbackward function until hit top limit switch
motorHome()

#calibration to bottom limit switch
#stepforward function until hit bottom limit switch
motorCalibrate()

#move up 1 layer height
stepbackward(layerHeight)

#begin curing, repeat until no more layers
while layer <= fileNum: #while the layer number is lower than the total number of slices
    #accessing the appropriate image for the layer
    if layer <= 10:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out000'+str(layer-1)+'.png')
    elif layer <= 100:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out00'+str(layer-1)+'.png')
    else:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out0'+str(layer-1)+'.png')

    #transform image
    #layerImg = pygame.transform.scale(layerImg,(display_width,display_height))
    #pygame.display.set_caption('Layer Number: ' + str(layer)) #display layer number

    #display black screen
    #gameDisplay.fill(black) 
    #pygame.display.update()

    #project image for curetime
    image(0,0)
    pygame.display.update()
    pygame.time.delay(curetime)

    #display black screen
    gameDisplay.fill(black)
    pygame.display.update()
    
    #fileNum*layerHeight = part height
    #move back up
    stepbackward(fileNum*layerHeight+10-layer*layerHeight)
    pygame.time.delay(3000)

    #increase layer
    layer = layer + 1

    #move back down to new position   
    stepforward(fileNum*layerHeight+10-layer*layerHeight)

#reset to home position
motorHome()

reset()
pygame.quit()
quit()
