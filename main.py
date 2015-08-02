import pygame,socket,math
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from random import randint
import ast

#colors
red = [1.0,0,0]
green = [0.0,1.0,0]
blue = [0,0,1.0]
black = [0,0,0]
white = [1.0,1.0,1.0]

playerW = 30
playerH = 30

playerPosX = 0
playerPosY = 0
playerVelX = 0.0
playerVelY = 0.0

speed = 0.02
maxSpeed = 0.2

#ast.literal_eval()
def make_dict(data):
	return ast.literal_eval(data)

users = 0

entities = {}

data = '{"name":[22,32,44,44] , "name2":[123,321,22,44]}'



def load_map(data):
	for i in data:
		entities[i] = data[i]

	data = make_dict(data)
	

def delete(I):
	del entities[I]

def spawn(name,x,y,w,h):
	entities[name] = [x , y , w ,h]


def enemy():
	for i in entities:
		rect( entities[i][0] , entities[i][1] , entities[i][2] , entities[i][3] , red)


def player(x,y):
	rect(x - playerW / 2 , y - playerH / 2 , playerW , playerH , blue)
	

def rect(x,y,w,h,color):
	glColor3f(color[0] , color[1], color[2])
	glBegin(GL_QUADS)
	glVertex2f(x, y)
	glVertex2f(x + w, y)
	glVertex2f(x + w, y + h)
	glVertex2f(x, y + h)
	glEnd()


def clearScreen():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def main():
	global users,playerPosX,playerPosY,playerVelX,playerVelY

	pygame.init()
	display = (1080,720)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

	glViewport(0, 0, 1080, 720)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, 1080, 0.0, 720, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()
	pygame.mouse.set_visible(True)
	playerPosX = 100
	playerPosY = 100
	pygame.key.set_repeat(1, 0)
	
	while True:
		playerPosX += playerVelX
		playerPosY += playerVelY

		mousePos = pygame.mouse.get_pos()
		mouseX = mousePos[0]
		mouseY = 720 - mousePos[1]


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				if event.key == pygame.K_e:
					pygame.key.set_repeat(50, 50)
					spawn(str(users),mouseX,mouseY,30,30)
					users += 1
					pygame.key.set_repeat(1, 0)

				if event.key == pygame.K_w:
					playerVelY += speed
				
				if event.key == pygame.K_s:
					playerVelY += -speed
				
				if event.key == pygame.K_a:
					playerVelX += -speed
				
				if event.key == pygame.K_d:
					playerVelX += speed
				


				
			else:
				break

		clearScreen()
		enemy()
		player(playerPosX,playerPosY)
		pygame.display.flip()
		pygame.time.wait(2)
main()