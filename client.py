import pygame,socket,math,time,sys,ast,threading
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from random import randint
import os, os.path

os.chdir(os.path.dirname(os.path.realpath(__file__)))

host = raw_input("host: ")
port = int(raw_input("port: "))
playerColor = raw_input("color: ")
s = socket.socket()
s.connect( ( host , port ) )
pygame.init()



###"""""""""""""""""""""""""""""""""""""### variables

threads = []

playerW = 28
playerH = 28

WIDTH = int(1080 * 0.7)
HEIGTH = int(720 * 0.7)

SCREEN_X = 0
SCREEN_Y = 0

playerPosX = WIDTH / 2
playerPosY = HEIGTH / 2
playerVelX = 0.0
playerVelY = 0.0

CameraX = 0
CameraY = 0

CollisionLeft = False
CollisionRight = False
CollisionTop = False
CollisionBottom = False

speed = 0.1
maxSpeed = 0.5

old_recv = ""

screen_flags = OPENGLBLIT | DOUBLEBUF | OPENGL
# | RESIZABLE# | FULLSCREEN

running = True

users = 0

entities = {}


MAP = {
"0":[100 ,250,40,100,"white"],
"00":[400 ,350,120,100,"white"],
"1":[-140 ,12,400,40,"white"],

}

name = None



#colors
COLORS = {
"red":[1,0,0],
"green":[0,1,0],
"blue":[0,0,1],
"white":[1,1,1],
"gray":[0.4,0.4,0.4],
"cyan":[0,1,1],
"purple":[1,0,1],
"yellow":[1,1,0],
}
###"""""""""""""""""""""""""""""""""""""###

###"""""""""""""""""""""""""""""""""""""### screen
display = (WIDTH,HEIGTH)
screen = pygame.display.set_mode(display, screen_flags)
pygame.display.set_caption("Simple multiplayer game")

glViewport(0, 0, WIDTH, HEIGTH)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0.0, WIDTH, 0.0, HEIGTH, 0.0, 1.0)
glMatrixMode (GL_MODELVIEW)
glLoadIdentity()

###"""""""""""""""""""""""""""""""""""""###

if playerColor not in COLORS:
	playerColor = "red"

def make_dict(data):
	return ast.literal_eval(data)

def load_map(data):
	data = data.replace("/add","")
	if "/add" not in data:
		try:
			data = make_dict(data)

			for i in data:
				entities[str(i)] = data[str(i)]
		except:
			KeyError


def delete(ID):
	ID = ID.replace("/del","")
	if "/del" not in ID:
		try:
			del entities[ID]
		except:
			KeyError


def render():
	try:
		for i in entities:
			rect( entities[i][0] - CameraX, entities[i][1] - CameraY, entities[i][2] , entities[i][3] , COLORS[entities[i][4]])
	except:
		KeyError

def player(x,y):
	rect(x - 15, y - 15, 30 , 30 , COLORS["white"])   #border
	rect((x - playerW / 2), y - playerH / 2, playerW , playerH , COLORS[playerColor]) #main player

def render_map():
	global CameraX , CameraY
	for i in MAP:
		rect(MAP[i][0] - CameraX , MAP[i][1] - CameraY, MAP[i][2] , MAP[i][3], COLORS["white"])

def rect(x,y,w,h,color):
	glColor3f(color[0] , color[1], color[2])
	glBegin(GL_QUADS)
	glVertex2f(x , y)
	glVertex2f(x + w, y)
	glVertex2f(x + w, y + h)
	glVertex2f(x, y + h)
	glEnd()


def clearScreen():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def send_data(x,y,color):
	global s , host , port , running
	s.send("/dat" + str(x) + ","+ str(y) + "," + color + "&")

def recv_data(s , host , port):
	global old_recv , running
	while True:
		try:
			recived = old_recv + s.recv(1024)

			recived = recived.split("&")
			
			old_recv = recived[int(len(recived)) - 1]

			del recived[int(len(recived)) - 1]
			
			for i in range(0, len(recived)):
				if "/add" in recived[i]:
					load_map(recived[i])

				if "/del" in recived[i]:
					delete(recived[i])
		
		except socket.error as error:
			print ("[ERR] " + str(socket.error))
		


def Collision(x , y , w , h):
	for i in MAP:
		if x > MAP[i][0] and x < MAP[i][0] + MAP[i][2]:
			return True
	else:
		return False

def main():
	global users , playerPosX , playerPosY , playerVelX , playerVelY , s , threads , running
	global WIDTH,HEIGTH,SCREEN_X,SCREEN_Y , CollisionLeft , CollisionRight , CollisionTop , CollisionBottom
	global screen , display , CameraX , CameraY
	
	pygame.mouse.set_visible(True)
	pygame.key.set_repeat(1, 0)

	t = threading.Thread(target=recv_data, args=(s , host , port))
	t.start()
	threads.append(t)

	while True:
		CameraX += playerVelX
		CameraY += playerVelY

		mousePos = pygame.mouse.get_pos()
		mouseX = mousePos[0]
		mouseY = WIDTH - mousePos[1]


		if playerVelX > maxSpeed:
			playerVelX = maxSpeed
		
		if playerVelX < -maxSpeed:
			playerVelX = -maxSpeed

		if playerVelY > maxSpeed:
			playerVelY = maxSpeed

		if playerVelY < -maxSpeed:
			playerVelY = -maxSpeed

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					exit()
					
				
				if event.key == pygame.K_w:
					playerVelY += speed
				
				if event.key == pygame.K_s:
					playerVelY += -speed
			
				if event.key == pygame.K_a:
					playerVelX += -speed
				
				if event.key == pygame.K_d:
					playerVelX += speed
			
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_d:
					playerVelX = 0
				if event.key == pygame.K_a:
					playerVelX = 0
				if event.key == pygame.K_w:
					playerVelY = 0
				if event.key == pygame.K_s:
					playerVelY = 0


				
			else:
				break
		
		send_data(CameraX + playerPosX , CameraY + playerPosY, playerColor)
		clearScreen()
		render()
		render_map()
		player(playerPosX , playerPosY)

		pygame.display.flip()
		pygame.time.wait(1)



main()