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
play_n = 0 # num players in the game
ydim = 20 # y dimension of the screen (height)
xdim = 50 # x dimension of the screen (width)
food_pos = [ydim/2,xdim/2,"food"] # initial positon of the first snake food

# 4 snakes at the moment
snakes = [
[[  (ydim/5), xdim/10],[  (ydim/5), (xdim/10)-1],[  (ydim/5) , (xdim/10)-2]],
[[(2*ydim/5), xdim/10],[(2*ydim/5), (xdim/10)-1],[(2*ydim/5) , (xdim/10)-2]],
[[(3*ydim/5), xdim/10],[(3*ydim/5), (xdim/10)-1],[(3*ydim/5),  (xdim/10)-2]],
[[(4*ydim/5), xdim/10],[(4*ydim/5), (xdim/10)-1],[(4*ydim/5),  (xdim/10)-2]]
]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
print("socket created")

try: 	
	sock.bind((host, port)) # bind socket to host and port
except socket.error:
	print ("binding failed")
	sys.exit()

print("socket has been bounded")

sock.listen(10) # listen for a max of 10 connections

print("socket is ready to listen")

# this function launches whenever a player(client) connects
def clientthread(conn,count):
	global ydim # screen height
	global xdim	# screen width
	global food_pos # position of food
	global play_n # number of players

	temp = [[ydim]+[xdim]]# dimension data in a an array
	message = str(temp) # convert array data to string

	conn.send(message.encode())#1.1 send the data using a socket
	conn.recv(1024) #1.2 wait for ack

	temp = ""
	temp = str(snakes)
	conn.send(temp.encode()) #2.1: send all snakes
	conn.recv(1024) #2.2: recv wait for ack
	
	msg = str(play_n)
	conn.send(msg.encode())#3.1: send player Number
	conn.recv(1024) #3.2: recv wait for ack
	play_n = play_n+1

	while 1:
		conn.send(ack.encode()) #4.1: send ack
		data = conn.recv(1024) #4.2: recv "up down left right"

		if not data: #need to check what this will change
			break;
			
		# winning and loosing conditions info here
		# input validation

		# error handling
		conn.send(data) #5.1: send validated data to clients
		conn.recv(1024) #5.2: recv wait for ack

		tempFood = str(food_pos)
		conn.send(tempFood.encode()) #6.1: send food
		conn.recv(1024) #6.2: recv wait for ack
	conn.close() # close connection

# function runs in parallel with all the threads, generates random food coordinates
# conn: socket connection data 
# food_present: boolean - whether the food is present or not
# for now food_present is not being used in this code
def food_function(dummy_var,food_present):
	global xdim
	global ydim
	global food_pos
	while 1:
		# while food_present==0: do this at a later stage
		time.sleep(3) # sleeps for 3 sec and then generate a new food
		food_pos = [
			random.randint(1, ydim-1),
			random.randint(1, xdim-1),
		]
####################################
# program begins execution from here
####################################
user_list = [] # list of all users
conn_list = [] # list of all connections
start_new_thread(food_function,("dummy",0)) #generate foods
print( "the snake is ", snakes)
while 1:
	# input of the number of players
	conn, addr = sock.accept()# accept connections when client tries to connect
	print("connected with " +  addr[0] + ":" + str(addr[1]))
	user_list.append(addr[1])
	conn_list.append(conn)
	start_new_thread(clientthread, (conn,0))
sock.close() # close socket

# to-do
# food should be same for both 
# generate random variable for snake position?
# loosing condition 
# growing condition
# wait for players before starting

# main condition
# show all snakes on all screen

# how to run between computers?