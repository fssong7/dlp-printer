#!/usr/bin/python
import pygame
import os, sys

pygame.init()

path = "/home/pi/Desktop/slices"
dirs = os.listdir( path )
fileNum = 0

for file in dirs:
   fileNum+=1
print(fileNum)