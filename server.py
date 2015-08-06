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

old_recv = ""
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
	global old_recv
	for c in conn:
		try:
			recived = old_recv +  c.recv(1024)
			
			recived = recived.split("&")

			old_recv = recived[int(len(recived)) - 1]
			
			del recived[int(len(recived)) - 1]

			for i in range(0,int(len(recived))):
				if "/pos" in recived[i]:
					data = recived[i]
					data = data.replace("/pos" , "")
					data = data.split(",")
					
					POS_X = data[0]
					POS_Y = data[1]

					POS_X = float(data[0])
					POS_Y = float(data[1])
					
					POS_X = int(POS_X)
					POS_Y = int(POS_Y)
					

					connections[str(c)] = [ POS_X - 15 , POS_Y - 15 , 30 , 30]
		except:
			socket.error

def send_all():
	global users
	for c in conn:
		try:
			client = str(c)
			c.send("/add" + str( connections ) + "&")

		
		except socket.error:
			try:
				
				if connections[client]:
					del connections[client]

				
					for c in conn:
						c.send("/del")
						c.send(str(data) + "&")
			except:
				KeyError


def new_connection(s , host , port):
	global users
	while True:
		c , addr = s.accept()
		print("[ALERT] New connection from: " + str(addr[0])) + " : "+str(addr[1])
		conn.append(c)
		connections[str(c)] = [100,100,30,30]

		main()

def main():
	t = threading.Thread(target=new_connection, args=(s , host , port))
	t.start()
	threads.append(t)
	while True:
		send_all()
		recv_all()
		
		
main()