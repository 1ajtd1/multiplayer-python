import socket

host = raw_input("host: ")
port = int(raw_input("port: "))

s = socket.socket()

s.bind( ( host , port ) )

s.listen(5)

connections = {}
users = 0

def load(data):
	connections[data] = [0,0]


def main():
	global users
	while True:
		c , addr = s.accept()
		c.send('/add_entity {"user['+str(users)+']":[50,50,30,30]}')
		users += 1
		load(addr)

		
		
main()