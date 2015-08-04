import socket
import time
import threading
import random
import sys
from random import *

host = raw_input("host: ")
port = int(raw_input("port: "))

s = socket.socket()

s.bind( ( host , port ) )

s.listen(5)

connections = {}

conn = []

block = {"block_1":[randint(1,1000),randint(1,700),30,30]}

users = 0

threads = []

def load(data):
	connections[data] = [0,0,30,30]

def send(c,addr):
	global users
	try:
		#c.send("/name"+str(addr))
		c.send('/add_entity' + str(block))
		users += 1
		load(addr)
	
	except socket.error as error:
		print("[ERR] " + str(error))

def recv_all():
	for c in conn:
		recived = c.recv(1024)
		if recived == "/pos":
			data = c.recv(1024)
			if "/pos" in data:
				data = data.replace("/pos" , "")
			
			data = data.split(",")

			POS_X = float(data[0])
			POS_Y = float(data[1])
			
			POS_X = int(POS_X)
			POS_Y = int(POS_Y)
			if POS_X != None and POS_Y != None and POS_X != "" and POS_Y != "":
				connections[str(c)] = [ POS_X - 16 , POS_Y - 16 , 32 , 32]

def send_all():
	global users
	for c in conn:
		try:
			c.send("/add_entity")
			c.send( str( connections ) + "&")

		except socket.error as error:
			print("[ERR] " + str(error))



def new_connection(s , host , port):
	global users
	while True:
		c , addr = s.accept()
		print("[ALERT] New connection: " + str(addr[0])) + " : "+str(addr[1])
		conn.append(c)
		connections[str(c)] = [100,100,32,32]

		main()

def main():
	t = threading.Thread(target=new_connection, args=(s , host , port))
	t.start()
	threads.append(t)
	while True:
		send_all()
		recv_all()
		
		
main()