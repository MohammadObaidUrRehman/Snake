import socket # communication
import sys
from thread import *# threading concurrency and parallelism 
import random # random number generation 
import curses # game related features e.g rendering
import ast # sting to array conversion

# function to send data across the socket
# sock is the connection
# message is the string we need to send
def send_using_socket(sock,message):
	try:
		# always need to encode before sending
		sock.sendall(message.encode())
	except socket.error:
		print("did not send successfully")
		sys.exit()

# this is where the programs starts from 
# initialisation of socket
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print ("Failed to connect")
	sys.exit()
# define port and host 
ack = "ack"
host = "localhost"
port = 8888
# resolve host "localhost" in our case
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	# print("host name could not be resolved")
	sys.exit();

sock.connect((remote_ip, port))

tempdim = sock.recv(1024) # recieve dimensions of the screen
sock.send(ack.encode())
dim = ast.literal_eval(tempdim.decode())
# decode dimensions of the screen
sh = dim[0][0] # height of the screen (y dimension)
sw = dim[0][1] # width of the screen  (x dimension)
# initialize new window with height and width
stdscr = curses.initscr()
curses.curs_set(0)
w = curses.newwin(int(sh), int(sw), 0, 0)
w.box() # create border around the player screen
w.keypad(1) # intialize to get keyboard input
w.timeout(1000) # set game speed, higher value means slower game
snakeTemp = sock.recv(1024) # recieve snake dimensions
sock.send(ack.encode())

snakeTemp = snakeTemp.decode() # decode string into array
snake = ast.literal_eval(snakeTemp)

myPlayNum = sock.recv(1024)
sock.send(ack.encode())

myPlayNum = ast.literal_eval(myPlayNum.decode())
mySnake = snake[myPlayNum]
food = [sh/2, sw/2]

w.addch(food[0], food[1], curses.ACS_PI)
key = curses.KEY_RIGHT # intially the input is hardcoded to right
# infinite while loop
while 1:
	# function to get keyboard input 
	next_key = w.getch()
	key = key if next_key == -1 else next_key
	# ending conditions
	# if the snak reaches the border then end game
	# if the snake eats himeself them end game
	# print "before ending", mySnake
	if mySnake[0][0] in [0, sh] or mySnake[0][1]  in [0, sw] or mySnake[0] in mySnake[1:]:
		curses.endwin()
		quit()
	# print "2"]
	new_head = [mySnake[0][0], mySnake[0][1]]
# encode the action to be taken in the string, and then send it to socket
# for now the socket just replies back with the same message
# we need to add functionality and in the sockets for this
	if key == curses.KEY_DOWN:
		message="down"
	if key == curses.KEY_UP:
		message="up"
	if key == curses.KEY_LEFT:
		message="left"
	if key == curses.KEY_RIGHT:
		message="right"
	# print "3"
	temp = str([message] + mySnake) 
	# print temp
	sock.recv(1024) #1 wait for ack
	sock.send(temp.encode()) #2 send input
	reply = sock.recv(1024) #3 recv validated input
	resp = ast.literal_eval(reply.decode())
	sock.send(ack.encode()) #4
	tFood = sock.recv(1024) #5
	sock.send(ack.encode()) #6
	# print "4"
	
# move the mySnake according to keyboard input 
	response = str(resp[0])
	# print response
	if response == "down":
		new_head[0] += 1
	if response == "up":
		new_head[0] -= 1
	if response == "left":
		new_head[1] -= 1
	if response == "right":
		new_head[1] += 1
	# print "5"

# we pop from the tail and add to the head to make it seem like the mySnake is moving
# if the mySnake eats food we don't pop from the tails to make it look like the mySnake has grown
	# print new_head
	mySnake.insert(0, new_head)
	# print "6"

	# this code has been commented for now, it refreshes the food whenever the mySnake eats food
	# with this code the mySnake also grows when it eats
	# all this code needs to be added to the server
	""" 
	# if mySnake[0] == food:
	# 	food = None
	# 	while food is None:
	# 		nf = [
	# 			random.randint(1, sh-1),
	# 			random.randint(1, sw-1)
	# 		]
	# 		food = nf if nf not in mySnake else None
	# w.addch(food[0], food[1], curses.ACS_PI)
	# else:
		# tail = mySnake.pop()
	# 	w.addch(tail[0], tail[1], ' ')
"""
	# in the current implemtntaion the mySnake doesn't grow
			# w.addch(food[1], food[0], ' ')
			# food = ast.literal_eval(tFood.decode())
			# w.addch(food[1], food[0], curses.ACS_PI)
# render new food on the screen


	tail = mySnake.pop()
	w.addch(int(tail[0]), int(tail[1]), ' ')
	# print "snake ", snake[0][0]
	w.addch(int(mySnake[0][0]), int(mySnake[0][1]), curses.ACS_CKBOARD)
	# print tail
	# print "7"

	# w.addch(int(tail[1]), int(tail[0]), ' ')

	# w.addch(int(tail[0]), int(tail[1]), ' ')
# pop from the tail
	# print mySnake
	# w.addch(int(mySnake[0][0]), int(mySnake[0][1]), curses.ACS_CKBOARD)
	# print "1"
# add to the head
# sock.close()


# need to deal with tail error maybe array is going our of bounds