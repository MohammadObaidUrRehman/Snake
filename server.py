from _thread import * # each player will have a seperate thread
import socket # communication between clients via server (sending and recieving data)
import sys
import random # generate random numbers
import time # use the time.sleep function
import ast # convert string to array
# port number and local host can change this aswell
# local host
host = ''
port = 8888

ack = "ack"
play_n = 0 # number of players in the game
ydim = 20 # y dimension of the screen aka height
xdim = 50 # x dimension of the screen aka width
food_pos = [ydim/2,xdim/2,"food"] # initial postiton of the first snake food

# only head coordinates for the first 4 snakes
# at the moment only catering for snakes can expand later 
snakes = [
[[  (ydim/5), xdim/10],[  ((ydim/5)-1), xdim   ],[  ((ydim/5)-2), xdim   ]],
[[(2*ydim/5), xdim/10],[((2*ydim/5)-1), xdim/10],[((2*ydim/5)-2), xdim/10]],
[[(3*ydim/5), xdim/10],[((3*ydim/5)-1), xdim/10],[((3*ydim/5)-2), xdim/10]],
[[(4*ydim/5), xdim/10],[((4*ydim/5)-1), xdim/10],[((4*ydim/5)-2), xdim/10]]
]

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")

# bind socker to host and port
try:
	sock.bind((host, port))
except socket.error:
	print ("binding failed")
	sys.exit()

print("socket has been bounded")

sock.listen(10) # listen for a max of 10 connections

print("socket is ready to listen")

# this function launches whenever a player(client) connect
def clientthread(conn,count):
	# height of the screen
	global ydim
	# widht of the screen
	global xdim
	# position of food
	global food_pos
	# number of players
	global play_n
	# put all the data in a an array
	temp = [[ydim]+[xdim]]
	# temp = [[ydim]+[xdim]+["dim"]]+[food_pos]
	# convert that array data to a string
	message = str(temp)
	print(message)
	print(temp) 
	# send the data using a socket
	conn.send(message.encode())
	conn.recv(1024) # wait for ack

	temp = ""
	temp = str(snakes)
	print(temp)
	conn.send(temp.encode())
	conn.recv(1024) #wait for ack
	
	msg = str(play_n)
	conn.send(msg.encode())
	conn.recv(1024) #wait for ack
	play_n = play_n+1

	while 1:
		# reciece data from the player
		print("sdare ")

		conn.send(ack.encode()) #1 "up down left right"
		print("data ")		
		data = conn.recv(1024) #2
		print("ata ")
		if not data:
			break;
		# error handling
		conn.send(data) #3 send the data that to the clients
		conn.recv(1024) #4
		print("sdre ")

		tempFood=str(food_pos)
		print("food")
		conn.send(tempFood.encode()) #5
		print("tempfood")
		conn.recv(1024) #6
		print("here ")
	conn.close()

# this function runs in parrallel with all the threads and generates foods randomly across the screen
# conn is the socket connection data and food_present is a boolenan variable 
# food present tells us whether the food is present on the grid or not
# for now food_present is not being used in this code
def food_function(dummy_var,food_present):
	global xdim
	global ydim
	global food_pos
	while 1:
		# while food_present==0: do this at a later stage
		time.sleep(3) # sleeps for 3 seconds and then generates a new food item.
		food_pos = [
			random.randint(1, ydim-1),
			random.randint(1, xdim-1),
		]

user_list = [] # to maintain a list of all users
conn_list = [] # to maintain a list of all connections
start_new_thread(food_function,("dummy",0))
print( "the snake is ", snakes)
while 1:
	conn, addr = sock.accept()
	# accept connections when a client tries to connect
	print("connected with " +  addr[0] + ":" + str(addr[1]))
	user_list.append(addr[1])
	conn_list.append(conn)
	start_new_thread(clientthread, (conn,0))
sock.close()
# close socket

# to-do
# food should be same for both 
# generate random variable for snake position?
# loosing condition 
# growing condition
# wait for players before starting

# main condition
# show all snakes on all screen

# how to run between computers?