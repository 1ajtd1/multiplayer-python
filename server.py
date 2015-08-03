import socket

host = raw_input("host: ")
port = int(raw_input("port: "))

s = socket.socket()

s.bind( ( host , port ) )

s.listen(5)

connections = {"asdf":[123,321,30,30]}
users = 0

def load(data):
	connections[data] = [0,0]

def send(c,addr):
	global users
	c.send('/add_entity ' + str(connections["asdf"]))
	users += 1
	load(addr)

def main():
	global users
	while True:
		c , addr = s.accept()
		send(c , addr)
		
		
main()