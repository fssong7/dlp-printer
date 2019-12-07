import pygame #projecting images to HDMI
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
lim = 10

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
gpio.setup(lim,gpio.IN)

#defining curetime in milliseconds
curetime = 5000

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

#limSwitch = gpio.input(lim) 
#print(limSwitch)

#while x:
#   limSwitch = gpio.input(lim)
#    print(limSwitch)
#    if limSwitch == 0:
#        x = False

#defining color RGB values
black = (0,0,0)
white = (255,255,255)

#projecting the image
def image(x,y):
    gameDisplay.blit(layerImg, (x,y))

#moving the stepper motor down
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

#moving the stepper motor up
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

#turning motor off
def reset():
    gpio.output(ena,True)
    gpio.output(ms1,False)
    gpio.output(ms2,False)
    gpio.output(ms3,False)
    gpio.output(step,False)
    gpio.output(direc,False)



#defining x and y coordinates (upper left) of image projected
x = 0#(display_width * 0.45)
y = 0#(display_height * 0.8)

layer = 1 #first layer
gpio.output(ena,False) #enable motors for movement

while layer <= fileNum: #while the layer number is lower than the total number of slices
    #accessing the appropriate image for the layer
    if layer <= 10:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out000'+str(layer-1)+'.png')
    elif layer <= 100:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out00'+str(layer-1)+'.png')
    else:
        layerImg = pygame.image.load('/home/pi/Desktop/slices/out0'+str(layer-1)+'.png')
    #transform image
    layerImg = pygame.transform.scale(layerImg,(display_width,display_height))

    #limSwitch = gpio.input(lim)
    #if not (limSwitch == 0):
        #if layer % 2 != 0:
           # stepforward()
        #else:
          #  stepbackward()
    #else:
       # break

    stepforward() #move downward
    pygame.display.set_caption('Layer Number: ' + str(layer)) #display layer number

    #display black screen
    gameDisplay.fill(black) 
    pygame.display.update()

    #project image for curetime
    image(0,0)
    pygame.display.update()
    pygame.time.delay(curetime)

    #display black screen
    gameDisplay.fill(black)
    pygame.display.update()

    #move back up
    stepbackward()
    pygame.time.delay(1000)

    #increase layer
    layer = layer + 1

reset()
pygame.quit()
quit()
