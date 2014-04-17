#coding:utf-8
#developed by 方一维 and 王婷

import os
import pygame
from pygame.locals import *
from sys import exit
from Rectangle import *
from Slide import *
from Ball import *
from User import *

CRASH_EVENT = USEREVENT+1
my_event = pygame.event.Event(CRASH_EVENT,message="")

#constans
STEP = 25
REC_LENGTH = 40
REC_WIDTH = 20
SLIDE_X = 300
SLIDE_Y = 550
SLIDE_LENGTH = 100
BORDER = 800
SCREEN_LENGTH = 1000
SCREEN_WIDTH = 600
SLIDE_IMAGE_FILENAME = "slide.png"
BALL_IMAGE_FILENAME = "ball.png"
USERLIFE_IMAGE_FILENAME = "life.png"
RULES_IMAGE_FILENAME = "rule.png"
BRICK_IMAGE_NAMES = ['blue-brick.png','pink-brick.png']
BALL_RADIUS = 6


#START actually is a flag
#GATE means how much our player has passed
#GLUE is to see whether Slide and ball is glued
START = False
GATE = 1
XSPEED = 220
YSPEED = -180
RECTANGLES = []
BRICK_IMAGES=[]
GO = False
GLUE = True
RULE_FLAG = False
GAMEINDEX = 1;
PAUSE = False

def game_setting_init(screen):
	global START
	START = True

	#set bricks
	filename = str(GATE) + ".txt"
	filehandle = open(filename)
	setting = filehandle.readline().strip().lstrip()
	while(setting):
		setting = setting.split(',')
		rectangle = Rectangle(int(setting[0]),int(setting[1]),int(setting[2]),int(setting[3]),int(setting[4]))
		RECTANGLES.append(rectangle)
		setting = filehandle.readline().strip().lstrip()
	for filename in BRICK_IMAGE_NAMES:
		background = pygame.image.load(filename).convert()
		BRICK_IMAGES.append(background)

	#set slide
	global slide
	slide = Slide(screen,SLIDE_X,SLIDE_Y,SLIDE_LENGTH,SLIDE_IMAGE_FILENAME)

	#set ball
	global ball
	ball_x = SLIDE_X+SLIDE_LENGTH/2-BALL_RADIUS
	ball_y = SLIDE_Y-BALL_RADIUS*2
	bounce_sound = pygame.mixer.Sound("bounce.ogg")
	ball = Ball(screen,ball_x,ball_y,BALL_RADIUS,XSPEED,YSPEED,BALL_IMAGE_FILENAME,bounce_sound)

	#set user
	global user
	try:
		life = user.lifes
		score = user.score
		user = User(screen,USERLIFE_IMAGE_FILENAME)
		user.set_life(life)
		user.set_score(score)
	except:
		user = User(screen,USERLIFE_IMAGE_FILENAME)



def redraw(screen):
	# draw bricks
	for rec in RECTANGLES:
		screen.blit(BRICK_IMAGES[rec.imageidx],(rec.x,rec.y))

	#draw slide
	slide.draw()

	#draw lines
	pygame.draw.rect(screen,[150,150,150],[BORDER,0,10,SCREEN_WIDTH],1)

	#draw ball
	ball.draw()

	#draw user's life
	user.draw_blood()

	#draw round
	fontname = pygame.font.get_default_font()
	font = pygame.font.Font(fontname,20)
	string = 'Round : '+str(GATE)
	text = font.render(string, True, (24, 122, 100))
	screen.blit(text,(830,30))

	#draw score
	string = 'Score : ' + str(user.score)
	text = font.render(string, True, (24, 122, 100))
	screen.blit(text,(830,130))

	#PAUSE LABEL
	x = pos[0]
	y = pos[1]
	if x > 830 and x < 930 and y > 230 and y < 330:
		screen.blit(text_7,(830,230))
	else:
		screen.blit(text_6,(830,230))

	#save game label
	if x > 830 and x < 930 and y > 330 and y < 430:
		screen.blit(text_9,(830,330))
	else:
		screen.blit(text_8,(830,330))


#start game position:(400,100)
STARTGAME_LABEL = [400,100]
RULE_LABEL = [400,200]
def build_maininterface(screen,pos):
	# draw something like buttons
	x = pos[0]
	y = pos[1]
	if x > 400 and x < 550 and y > 100 and y < 150:
		screen.blit(text_1,STARTGAME_LABEL)
	else:
		screen.blit(text_0,STARTGAME_LABEL)

	if x > 400 and x < 550 and y > 200 and y < 250:
		screen.blit(text_3,RULE_LABEL)
	else:
		screen.blit(text_2,RULE_LABEL)

	if x > 400 and x < 550 and y > 300 and y < 350:
		screen.blit(text_11,(400,300))
	else:
		screen.blit(text_10,(400,300))

	screen.blit(author_image,(800,500))


BACK_LABEL = [500,450]
def show_rules(screen,pos):
	screen.blit(rule_image,(50,50))
	x = pos[0]
	y = pos[1]
	if x > 500 and x < 600 and y > 450 and y < 550:
		screen.blit(text_5,BACK_LABEL)
	else:
		screen.blit(text_4,BACK_LABEL)



def crash_check():
	bong = False
	global GATE
	global START
	global GO
	global GLUE

	#check bricks
	for brick in RECTANGLES:
		num = brick.collide_detect(ball)
		if num != 0:
			ball.play_sound()
			user.add_score(100)
			RECTANGLES.remove(brick)
			break

	if RECTANGLES == False or len(RECTANGLES) == 0:
		GATE = GATE + 1
		START = False
		GO = True
		GLUE = True
		return


	if num == 1 or num == 3:
		ball.xspeed = -ball.xspeed
	elif num == 2 or num == 4:
		ball.yspeed = -ball.yspeed
	elif num == 5 or num == 6 or num == 7 or num == 8:
		ball.xspeed = -ball.xspeed
		ball.yspeed = -ball.yspeed

	xcenter = ball.x + ball.radius
	ycenter = ball.y + ball.radius
	#check left wall
	if xcenter <= ball.radius:
		ball.xspeed = -ball.xspeed
		ball.x += ball.radius

	#check right wall
	if xcenter >= (BORDER - ball.radius):
		ball.xspeed = -ball.xspeed
		ball.x -= ball.radius

	#check top wall
	if ycenter <= ball.radius:
		ball.yspeed = -ball.yspeed
		ball.y += ball.radius

	#check slide
	if ycenter >= (slide.y - ball.radius):
		if xcenter >= (slide.x - ball.radius) and xcenter <= (slide.x + slide.length + ball.radius):
			ball.xspeed += slide.speed
			ball.yspeed = -ball.yspeed
			ball.y -= ball.radius
			if ball.xspeed > 350:
				ball.xspeed = 350
			elif ball.xspeed < -350:
				ball.xspeed = -350
		else:
			#player didn't catch the ball
			user.die()
			if user.isalive() == True:
				GLUE = True
				slide.reset()
				ball.reset()

			else:
			#restart the game
				GLUE = True
				START = False
				GO = True
				GATE = 1
				del RECTANGLES[:]


def save_game():
	fileHandle = open ( 'data.txt', 'w' )

	#gate
	string = str(GATE) + '\n'
	fileHandle.write(string)

	#user
	string = str(user.lifes) + ',' + str(user.score) + ',' + user.imageurl + '\n'
	fileHandle.write(string)
	#ball
	string = str(ball.x) + ',' + str(ball.y) + ',' + str(ball.radius) + ',' + str(ball.xspeed) + ',' + str(ball.yspeed) + ',' + ball.imageurl + '\n'
	fileHandle.write(string)

	#slide
	string = str(slide.x) + ',' + str(slide.y) + ',' + str(slide.length) + ',' + slide.imageurl + '\n'
	fileHandle.write(string)

	#brick
	for i in RECTANGLES:
		string = str(i.x) + ',' + str(i.y) + ',' + str(i.length) + ',' + str(i.width) + ',' + str(i.imageidx) + '\n'
		fileHandle.write(string)

def load_game():

	filename = 'data.txt'
	filehandle = open(filename)

	#gate
	global GATE
	setting = filehandle.readline().strip().lstrip().split(',')
	GATE = int(setting[0])

	#set user
	global user
	setting = filehandle.readline().strip().lstrip().split(',')
	user = User(screen,USERLIFE_IMAGE_FILENAME)
	user.set_life(int(setting[0]))
	user.set_score(int(setting[1]))


	#set ball
	global ball
	setting = filehandle.readline().strip().lstrip().split(',')
	bounce_sound = pygame.mixer.Sound("bounce.ogg")
	ball = Ball(screen,float(setting[0]),float(setting[1]),int(setting[2]),float(setting[3]),float(setting[4]),BALL_IMAGE_FILENAME,bounce_sound)

	#set slide
	global slide
	setting = filehandle.readline().strip().lstrip().split(',')
	slide = Slide(screen,int(setting[0]),int(setting[1]),int(setting[2]),SLIDE_IMAGE_FILENAME)

	#set bricks
	setting = filehandle.readline().strip().lstrip()
	while(setting):
		setting = setting.split(',')
		rectangle = Rectangle(int(setting[0]),int(setting[1]),int(setting[2]),int(setting[3]),int(setting[4]))
		RECTANGLES.append(rectangle)
		setting = filehandle.readline().strip().lstrip()
	for filename in BRICK_IMAGE_NAMES:
		background = pygame.image.load(filename).convert()
		BRICK_IMAGES.append(background)



move_x = 0

pygame.init()
screen = pygame.display.set_caption("Hit Brick")
screen = pygame.display.set_mode((SCREEN_LENGTH,SCREEN_WIDTH),pygame.DOUBLEBUF|pygame.HWSURFACE)

rule_image = pygame.image.load(RULES_IMAGE_FILENAME).convert()
AUTHOR_IMAGE = 'author.png'
author_image = pygame.image.load(AUTHOR_IMAGE).convert()

if not pygame.font:
	print('Warning, Can not found font!')
fontname = pygame.font.get_default_font()
font = pygame.font.Font(fontname,20)
text_0 = font.render('START GAME', True, (84, 52, 243))
text_1 = font.render('START GAME', True, (34, 252, 43))

text_2 = font.render('GAME RULE', True, (84, 52, 243))
text_3 = font.render('GAME RULE', True, (34, 252, 43))

text_4 = font.render('BACK', True, (84, 52, 243))
text_5 = font.render('BACK', True, (34, 252, 43))

text_6 = font.render('PAUSE', True, (84, 52, 243))
text_7 = font.render('PAUSE', True, (34, 252, 43))

text_8 = font.render('SAVE GAME', True, (84, 52, 243))
text_9 = font.render('SAVE GAME', True, (34, 252, 43))

text_10 = font.render('LOAD GAME', True, (84, 52, 243))
text_11 = font.render('LOAD GAME', True, (34, 252, 43))

pygame.time.set_timer(CRASH_EVENT,25)
clock = pygame.time.Clock()


while True:

	if START == False and GO == True:
		game_setting_init(screen)
	elif GO == False:
		pass

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()


		elif event.type == CRASH_EVENT:
			if GLUE == False:
				ball.run(25.0/1000)
				crash_check()

		elif event.type == KEYDOWN:

			if event.key == K_LEFT:
				move_x = -STEP

			elif event.key == K_RIGHT:
				move_x = STEP

			elif event.key == K_SPACE:
				GLUE = False

			elif event.key == K_f and len(RECTANGLES) > 0:
				del RECTANGLES[0]

		elif event.type == KEYUP:
			move_x = 0

		elif event.type == MOUSEMOTION:
			global pos
			pos = pygame.mouse.get_pos()


		elif event.type == MOUSEBUTTONDOWN:
			pressed_array = pygame.mouse.get_pressed()
			for index in range(len(pressed_array)):
				if pressed_array[index]:
					if index == 0:
						if GO == False:
							pos = pygame.mouse.get_pos()
							# left button
							x = pos[0]
							y = pos[1]
							if GAMEINDEX == 1 and x > 400 and x < 500 and y > 100 and y < 150:
								GO = True
								GAMEINDEX = 2

							elif GAMEINDEX == 1 and x > 400 and x < 500 and y > 200 and y < 250:
								RULE_FLAG = True
								GAMEINDEX = 3

							elif GAMEINDEX == 1 and x > 400 and x < 500 and y > 300 and y < 350:
								START = True
								GO = True
								GLUE = False
								GAMEINDEX = 2
								load_game()

							elif GAMEINDEX == 3 and x > BACK_LABEL[0] and x < (BACK_LABEL[0]+100) and y > BACK_LABEL[1] and y < (BACK_LABEL[1]+100):
								RULE_FLAG = False
								GAMEINDEX = 1

						else:
							if GAMEINDEX == 2:
								#pause
								pos = pygame.mouse.get_pos()
								x = pos[0]
								y = pos[1]
								if x > 830 and x < 930 and y > 230 and y < 330:
									if PAUSE == False:
										pygame.time.set_timer(CRASH_EVENT,0)
										PAUSE = True
									else:
										pygame.time.set_timer(CRASH_EVENT,25)
										PAUSE = False
								elif x > 830 and x < 930 and y > 330 and y < 430:
									print 'lalal'
									save_game()

					elif index == 1:
						# mouse wheel
						pass

					elif index == 2:
						pass
						# right button

	#time_passed = clock.tick(40)
	if GAMEINDEX == 3:
		screen.fill((0,0,0))
		show_rules(screen,pos)

	elif GAMEINDEX == 2 and START == True:
		slide.translation(move_x,BORDER)
		if move_x == 0:
			slide.dcc()
		else:
			slide.acc(move_x)

		if GLUE == True:
			ball.translation(slide.x,SLIDE_LENGTH)
		else:
			#time_passed_seconds = time_passed / 1000.0
			#ball.run(time_passed_seconds)
			#crash_check()
			pass
		screen.fill((0,0,0))
		redraw(screen)

	else:
		screen.fill((0,0,0))
		build_maininterface(screen,pos)

	pygame.display.update()



