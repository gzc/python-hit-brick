"""
This class represents ball
x,y          ------ the center of a ball
radius       ------ the radius of ball
speed        ------ the speed of ball
filename     ------ ball image url
"""

import pygame
from pygame.locals import *


class Ball:
    
	def __init__(self,screen,x,y,radius,xspeed,yspeed,filename,bounce_sound):	
		self.screen = screen
		self.x = x
		self.y = y
		self.radius = radius
		self.xspeed = xspeed
		self.yspeed = yspeed
		self.imageurl = filename
		self.bounce_sound = bounce_sound

		self.picture = pygame.image.load(filename).convert()

		self.originx = x
		self.originy = y
		self.originxs = xspeed
		self.originys = yspeed

	def run(self,seconds):
		self.x += self.xspeed*seconds
		self.y += self.yspeed*seconds
	
	def translation(self,slide_x,slide_l):
		self.x = slide_x + slide_l/2 - self.radius		

	def draw(self):
		self.screen.blit(self.picture,(self.x,self.y))
		
	def reset(self):
		self.x = self.originx
		self.y = self.originy
		self.xspeed = self.originxs
		self.yspeed = self.originys

	def play_sound(self):
		channel = self.bounce_sound.play()
		if channel is not None:
			channel.set_volume(0.5, 0.5)
