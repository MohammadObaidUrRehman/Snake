from _thread import * # each player will have a seperate thread
import socket# communication between clients via server (sending and recieving data)
from socket import gethostbyname
import sys
import random # generate random numbers	
import time # use the time.sleep function
import ast # convert string to array
import os
# port number and local host can change this aswell
# local host
# host = '0.0.0.0'
# hostName = gethostbyname('0.0.0.0')
hostName = gethostbyname( '0.0.0.0' )
port = 8888

ack = "ack"
play_n = 0 # num players in the game
curr_play = 0
ydim = 20 # y dimension of the screen (height)
xdim = 50 # x dimension of the screen (width)
food_pos = [ydim/2,xdim/2,"food"] # initial positon of the first snake food

# 4 snakes at the moment

# snakes = [
# [[  (ydim/5), xdim/10],[  (ydim/5), (xdim/10)-1],[  (ydim/5) , (xdim/10)-2]],
# [[(2*ydim/5), xdim/10],[(2*ydim/5), (xdim/10)-1],[(2*ydim/5) , (xdim/10)-2]],
# [[(3*ydim/5), xdim/10],[(3*ydim/5), (xdim/10)-1],[(3*ydim/5),  (xdim/10)-2]],
# [[(4*ydim/5), xdim/10],[(4*ydim/5), (xdim/10)-1],[(4*ydim/5),  (xdim/10)-2]]
# ]
snakes = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket
print("socket created")

try: 	
	sock.bind((hostName, port)) # bind socket to host and port
except socket.error:
	print ("binding failed")
	sys.exit()

print("socket has been bounded")

sock.listen(10) # listen for a max of 10 connections

print("socket is ready to listen")
def generatesnake(num):
	global ydim
	global xdim
	allsnakes = []
	snake = []
	snakebuilder = []
	for i in range(0,num): 
		snake = []
		heady=random.randint(2, int(ydim)-2)
		headx=random.randint(3, int(xdim-xdim/4))
		for j in range(0,3):
			snakebuilder = []	
			snakebuilder.append(heady)
			snakebuilder.append(headx-j)
			snake.append(snakebuilder)
		allsnakes.append(snake)
	return allsnakes

def collision(snake,my_play):
	snake_head = snake[0]
	allSnakeTemp = snakes[:]
	allSnakeTemp.pop(my_play)

	for i in range(0,len(allSnakeTemp)):
		for j in range(0,len(allSnakeTemp[i])):
			if snake_head == allSnakeTemp[i][j]:
				return 1
	return 0
# this function launches whenever a player(client) connects
def clientthread(conn,my_play,lock):
	global ydim # screen height
	global xdim	# screen width
	global food_pos # position of food
	global play_n # number of players
	global curr_play
	has_lost = 0
	tempPlay = str(tot_Play)
	print(tempPlay)
	conn.send(tempPlay.encode())#0.1 send
	conn.recv(1024)#0.2 recv

	temp = [[ydim]+[xdim]]# dimension data in a an array
	message = str(temp) # convert array data to string

	conn.send(message.encode())#1.1 send the data using a socket
	conn.recv(1024) #1.2 wait for ack
	tempPlay=str(2)
	temp = ""
	temp = str(snakes)
	conn.send(temp.encode()) #2.1: send all snakes
	conn.recv(1024) #2.2: recv wait for ack
	
	# my_play = play_n
	msg = str(my_play)
	conn.send(msg.encode())#3.1: send player Number
	conn.recv(1024) #3.2: recv wait for ack
	
	mySnake = snakes[my_play]
	play_n = play_n+1
	print(my_play)
	lastinput = "right"
	while curr_play>1:
		conn.send(ack.encode()) #4.1: send ack
		data = conn.recv(1024) #4.2: recv "up down left right"

		if not data: #need to check what this will change
			break;

		if has_lost != 1:
			new_head = [mySnake[0][0], mySnake[0][1]]
			reply = data.decode()
			response = str(reply)


			if (lastinput == "right" and response =="left") or (lastinput == "left" and response == "right") or (lastinput == "up" and response == "down") or (lastinput == "down" and response == "up"):
				response = lastinput

			if response == "down":
				new_head[0] += 1
			if response == "up":
				new_head[0] -= 1
			if response == "left":
				new_head[1] -= 1
			if response == "right":
				new_head[1] += 1
			lastinput = response
			mySnake.insert(0, new_head) #edit snake, to this in server
			mySnake.pop()# pop from tail

			if mySnake[0][0] in [0, ydim] or mySnake[0][1] in [0, xdim] or mySnake[0] in mySnake[1:]:
				has_lost = 1
				curr_play = curr_play - 1
				mySnake = []
				# break;
			elif collision(mySnake,my_play):
				has_lost = 1
				curr_play = curr_play - 1
				mySnake = []
				# break;
		if (curr_play<2):
			print("curr play")
			break
		snakes[my_play]=mySnake # might need to use locks

		# winning and loosing conditions info here
		# input validation

		message = str(snakes)
		conn.send(message.encode()) #5.1: send validated data to clients
		conn.recv(1024) #5.2: recv wait for ack

		tempFood = str(food_pos)
		conn.send(tempFood.encode()) #6.1: send food
		conn.recv(1024) #6.2: recv wait for ack
	print("has lost")
	if has_lost==0:
		winmsg = "win"
		conn.send(winmsg.encode())
		conn.recv(1024)
	elif has_lost==1:
		winmsg = "loss"
		conn.send(winmsg.encode())
		conn.recv(1024)
	print("clsong")
	# conn.close() # close connection
	print("closed connection")
	lock.release()
	# return

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
thread_list = []
locks = []
global tot_Play
tot_Play = input("Number of Players: ")
tot_Play = int(tot_Play)
curr_play = tot_Play
snakes = []
snakes = generatesnake(tot_Play)
start_new_thread(food_function,("dummy",0)) #generate foods
print( "the snake is ", snakes)
while 1:
	print( "here")
	conn, addr = sock.accept()# accept connections when client tries to connect
	print("connected with " +  addr[0] + ":" + str(addr[1]))
	user_list.append(addr[1])
	conn_list.append(conn)
	# start_new_thread(clientthread, (conn,0))
	has_completed = 0
	if(len(conn_list)==tot_Play):
		for co in range(0,tot_Play):
			_lock = allocate_lock()
			_lock.acquire()
			locks.append(_lock)
			to = start_new_thread(clientthread, (conn_list[co],co,_lock))
		for _lock in locks:
			_lock.acquire()
		break;
			# thread_list.append(to)
		# for k in thread_list:
		# 	k.join()
			# print("here")
sock.shutdown(socket.SHUT_RDWR)
sock.close() # close socket #need to this in thread
print("the game has ended")
os.system("reset")
# to-do
# food should be same for both 
# generate random variable for snake position?
# loosing condition 
# growing condition
# wait for players before starting

# main condition
# show all snakes on all screen

# how to run between computers?

# connected with 127.0.0.1:51662
# connected with 127.0.0.1:51664
# <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8888), raddr=('127.0.0.1', 51662)>
# <socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8888), raddr=('127.0.0.1', 51664)>
