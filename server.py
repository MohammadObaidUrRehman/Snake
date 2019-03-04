import socket
import sys
from _thread import *


host = ''
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")

try:
	s.bind((host, port))
except socket.error:
	print ("binding failed")
	sys.exit()

print("socket has been bounded")

s.listen(10)

print("socket is ready to listen")

# message = input("enter your message	")
def clientthread(conn):
	counter=0
	message = "welcome to the server. type something and hit enter"
	conn.send(message.encode())
	while 1:
		data = conn.recv(1024)
		reply = "OK" + data.decode()
		if not data:
			break;
		print(reply)
		sendData = "message from server number" + str(counter) 
		conn.send(sendData.encode())
		counter=counter+1
	conn.close()

while 1:
	conn, addr = s.accept()
	print("connected with" +  addr[0] + ":" + str(addr[1]))
	start_new_thread(clientthread, (conn,))
s.close()
