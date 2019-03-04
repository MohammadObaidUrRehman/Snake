import socket
import sys
from _thread import *
import random
import curses

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print ("Failed to connect")
	sys.exit()

print("socket created")
host = "localhost"
port = 8888

try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print("host name could not be resolved")
	sys.exit();

print("IP addresss: "+ remote_ip)

s.connect((remote_ip,port))

print("socket connected to " + host + " using IP " + remote_ip)

# def listener(socket_var):
# 	while 1:
# 		reply = s.recv(4096)
# 		print(reply.decode())

# def speaker(socket_var):
# 	while 1:	
# 		message = input("enter your message	")
# 		try:
# 			s.sendall(message.encode())
# 		except socket.error:
# 			print("did not send successfully")
# 			sys.exit()
# 		print ("message send successfully ")

# start_new_thread(listener, (s,))
# start_new_thread(speaker,  (s,))
while 1:
	# message = "hello what is your name"
	message = input("enter your message	")
	try:
		s.sendall(message.encode())
	except socket.error:
		print("did not send successfully")
		sys.exit()
	print ("message send successfully ")

	reply = s.recv(4096)
	print(reply.decode())

s.close()