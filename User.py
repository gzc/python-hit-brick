"""
This class represents User
life     ------ 
"""

import pygame
from pygame.locals import *


class User:
    
	def __init__(self,screen,filename):	
		self.lifes = 3
		self.screen = screen
		self.imageurl = filename

		self.picture = pygame.image.load(filename).convert()
		self.score = 0

	def die(self):
		self.lifes = self.lifes-1

	def isalive(self):
		if(self.lifes == 0):
			return False
		return True

	def draw_blood(self):
		for i in range (self.lifes):
			x = 10+i*30
			y = 570
			self.screen.blit(self.picture,(x,y))

	def add_score(self,score):
		self.score += score

	def reset(self):
		self.lifes = 3
		self.score = 0

	def set_life(self,n):
		self.lifes = n

	def set_score(self,score):
		self.score = score
