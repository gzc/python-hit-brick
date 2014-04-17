"""
This class represents brick
x,y          ------ position
length,width ------ brick parameter
image        ------ brick image url
"""

import pygame
from pygame.locals import *
from Ball import *

class Rectangle:
    
	def __init__(self,x,y,length,width,imageidx):	
		self.x = x
		self.y = y
		self.length = length
		self.width = width
		self.imageidx = imageidx

	def collide_detect(self,ball):
 	
			  #2
		###############
		#5     		 6#
		#			  #
		#1			 3#	 	
		#			  #
		#8	  #4 	 7#
		###############

		#first step: check edge 1
		xcenter = ball.x + ball.radius
		ycenter = ball.y + ball.radius

		cornerx_1 = self.x
		cornery_1 = self.y
		cornerx_2 = self.x + self.length
		cornery_2 = self.y
		cornerx_3 = self.x + self.length
		cornery_3 = self.y + self.width
		cornerx_4 = self.x
		cornery_4 = self.y + self.width
		
		if ycenter >= self.y and ycenter <= (self.y+self.width) and xcenter >= (self.x-ball.radius) and xcenter < self.x:
			return 1

		#second: check edge 2
		elif xcenter >= self.x and xcenter <= (self.x+self.length) and ycenter >= (self.y-ball.radius) and ycenter < self.y: 
			return 2
			
		#third: check edge 3
		elif ycenter >= self.y and ycenter <= (self.y+self.width) and xcenter <= (self.x+self.length+ball.radius) and xcenter > (self.x+self.length):
			return 3
		
		#last: check edge 4
		elif xcenter >= self.x and xcenter <= (self.x+self.length) and ycenter <= (self.y+self.width+ball.radius) and ycenter > (self.y+self.width):
			return 4


		#check for corners
		elif ((xcenter - cornerx_1)**2 + (ycenter - cornery_1)**2)  <= ( ball.radius**2 ):
			return 5
		elif ((xcenter - cornerx_2)**2 + (ycenter - cornery_2)**2)  <= ( ball.radius**2 ):
			return 6
		elif ((xcenter - cornerx_3)**2 + (ycenter - cornery_3)**2)  <= ( ball.radius**2 ):
			return 7
		elif ((xcenter - cornerx_4)**2 + (ycenter - cornery_4)**2)  <= ( ball.radius**2 ):
			return 8
		else:
			return 0
