import pygame,socket,math,time,sys,ast,threading
import OpenGL
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
from random import randint

host = raw_input("host: ")
port = int(raw_input("port: "))
playerColor = raw_input("color: ")
s = socket.socket()
s.connect( ( host , port ) )

threads = []

playerW = 28
playerH = 28

WIDTH = 720 #1080 / 2
HEIGTH = 480 #720 / 2
SCREEN_X = 0
SCREEN_Y = 0

playerPosX = WIDTH / 2
playerPosY = HEIGTH / 2
playerVelX = 0.0
playerVelY = 0.0

CollisionLeft = False
CollisionRight = False
CollisionTop = False
CollisionBottom = False

speed = 0.5
maxSpeed = 2.5

old_recv = ""

screen_flags = DOUBLEBUF | OPENGL# | RESIZABLE# | FULLSCREEN
#ast.literal_eval()
running = True

users = 0

entities = {}

MAP = {
#"0":[100,250,40,100,"white"],
# "1":[0,0,10,800,"white"],
# "2":[0,800,800,10],
# "3":[800,0,10,800]
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
	print("delete: "+str(ID))
	ID = ID.replace("/del","")
	if "/del" not in ID:
		try:
			del entities[ID]
		except:
			KeyError


def render():
	try:
		for i in entities:
			rect( entities[i][0] , entities[i][1] , entities[i][2] , entities[i][3] , COLORS[entities[i][4]])
	except:
		KeyError

def player(x,y):
	rect(x - 15 , y - 15 , 30 , 30 , COLORS["white"])   #border
	rect(x - playerW / 2 , y - playerH / 2 , playerW , playerH , COLORS[playerColor]) #main player

def render_map():
	for i in MAP:
		rect(MAP[i][0] , MAP[i][1] , MAP[i][2] , MAP[i][3], COLORS["white"])

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
		

def render_text(message,color):
	font = pygame.font.Font(None,24)
	label = font.render("text!", 1, (255,255,0))
	#screen.blit(label, (100,100))
# def CLeft(x,y,w,h):
# 	for i in MAP:
# 		if x - w / 2 < MAP[i][0] + MAP[i][2] and x > MAP[i][0] + MAP[i][2] and y + h / 2 > MAP[i][1] and y < MAP[i][1] + MAP[i][3]:
# 			return True
# 	else:
# 		return False

# def CRight(x,y,w,h):
# 	for i in MAP:
# 		if x + w / 2 > MAP[i][0] and x < MAP[i][0] + MAP[i][2] and y + h / 2 > MAP[i][1] and y < MAP[i][1] + MAP[i][3]:
# 			return True
# 	else:
# 		return False

# def CTop(x,y,w,h):
# 	for i in MAP:
# 		if y + h / 2 > MAP[i][1] and y < MAP[i][1] + MAP[i][3] and x + w / 2 > MAP[i][0] and x < MAP[i][0] + MAP[i][2]:
# 			return True
# 	else:
# 		return False

# def CBottom(x,y,w,h):
# 	for i in MAP:
# 		if y + h / 2 < MAP[i][1] and y > MAP[i][1] + MAP[i][3] and x + w / 2 > MAP[i][0] and x < MAP[i][0] + MAP[i][2]:
# 			return True
# 	else:
# 		return False
def main():
	global users , playerPosX , playerPosY , playerVelX , playerVelY , s , threads , running
	global WIDTH,HEIGTH,SCREEN_X,SCREEN_Y , CollisionLeft , CollisionRight , CollisionTop , CollisionBottom
	
	pygame.init()
	display = (WIDTH,HEIGTH)
	screen = pygame.display.set_mode(display, screen_flags)
	pygame.display.set_caption("Game")

	glViewport(0, 0, WIDTH, HEIGTH)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0.0, WIDTH, 0.0, HEIGTH, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()

	pygame.mouse.set_visible(True)
	pygame.key.set_repeat(1, 0)

	t = threading.Thread(target=recv_data, args=(s , host , port))
	t.start()
	threads.append(t)
	#text_bg = pygame.Surface(screen.get_size())

	while True:
		# font = pygame.font.Font(None,24)
		# label = font.render("text!", 1, (255,255,0))
		# screen.blit(label, (100,100))
		# CollisionLeft = CLeft(playerPosX , playerPosY , 30 , 30)
		# CollisionRight = CRight(playerPosX , playerPosY , 30 ,30)
		# CollisionTop = CTop(playerPosX , playerPosY , 30 , 30)
		# CollisionBottom = CBottom(playerPosX , playerPosY , 30 , 30)
		# if CollisionLeft == True and playerVelX < 0:
		# 	playerVelX = 0

		# if CollisionRight == True and playerVelX > 0:
		# 	playerVelX = 0

		# if CollisionTop == True and playerVelY > 0:
		# 	playerVelY = 0
		
		# if CollisionBottom == True and playerVelY < 0:
		# 	playerVelY = 0
		
		playerPosX += playerVelX
		playerPosY += playerVelY

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
	
		send_data(playerPosX , playerPosY, playerColor)
		clearScreen()
		render()
		render_map()
		player(playerPosX,playerPosY)
		#render_text("asdf",(255,255,255))
		pygame.display.flip()

		pygame.time.wait(2)



main()