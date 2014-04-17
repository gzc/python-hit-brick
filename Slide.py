"""
This class represents slide
x,y          ------ position
length,width ------ brick parameter
image        ------ brick image url
"""

import pygame
from pygame.locals import *


class Slide:
    
	def __init__(self,screen,x,y,length,filename):	
		self.screen = screen
		self.x = x
		self.y = y
		self.length = length
		self.imageurl = filename

		self.picture = pygame.image.load(filename).convert()

		self.originx = x
		self.originy = y
		self.speed = 0

	def translation(self,move_x,border):
		tmp = self.x + move_x
		r_border = border - self.length
		if tmp < 0 or tmp > r_border:
			return
		self.x += move_x

	def draw(self):
		self.screen.blit(self.picture,(self.x,self.y))

	def reset(self):
		self.x = self.originx
		self.y = self.originy
		self.speed = 0

	def acc(self,parm):
		self.speed += parm

	def dcc(self):
		if self.speed > 0:
			self.speed -= 15
			if self.speed < 0:
				self.speed = 0
		elif self.speed < 0:
			self.speed += 15
			if self.speed > 0:
				self.speed = 0
		
