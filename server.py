import socket
import time
import threading
import random
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
		print("[ERR]" + str(error))



def send_all():
	global users
	for c in conn:
		try:
			#c.send("/add_entity" + str(connections))
			#c.send("\n")
			#c.send("/add_entity"+'{box:[25,25,30,30]}')
			users += 1
		
		except socket.error as error:
			print("[ERR]" + str(error))

def new_connection(s , host , port):
	global users
	while True:
		c , addr = s.accept()
		print("[ALERT] New connection: " + str(addr[0])) + " : "+str(addr[1])
		conn.append(c)
		connections[str(addr[1])] = [100,100,30,30]
		send(c , addr)
		main()

def main():
	t = threading.Thread(target=new_connection, args=(s , host , port))
	t.start()
	threads.append(t)
	while True:
		send_all()
		
		
main()