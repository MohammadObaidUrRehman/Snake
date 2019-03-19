import sys
import socket # communication
from thread import * # threading concurrency and parallelism 
import random # random number generation 
import curses # game related features e.g rendering
import ast # sting to array conversion
import time # for time.sleep

# function to send data across the socket
# sock is the connection
# message is the string we need to send
def send_using_socket(sock,message):
	try:
		sock.sendall(message.encode())
	except socket.error:
		print("did not send successfully")
		sys.exit()

def render(snake,numberOfPlayers): #function to render snake, need to add for numplayers
	for y in range (0,len(snake)):
		for x in range(0,len(snake[y])):
			w.addch(int(snake[y][x][0]), int(snake[y][x][1]), "o")
			time.sleep(0.01)

####################################
# program begins execution from here
####################################
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print ("Failed to connect")
	sys.exit()
ack  = "ack"
host = "localhost"
port = 8888
try: # resolve host "localhost" in our case
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	# print("host name could not be resolved")
	sys.exit();

sock.connect((remote_ip, port))

tempdim = sock.recv(1024) #1.1: recv dimensions of the screen
sock.send(ack.encode())#1.2: send ack

dim = ast.literal_eval(tempdim.decode()) # decode dimensions of screen
sh = dim[0][0] # screen height (y dimension)
sw = dim[0][1] # screen width  (x dimension)
# initialize new window with height and width
stdscr = curses.initscr()
curses.curs_set(0)
w = curses.newwin(int(sh), int(sw), 0, 0)
w.box() # border around the player screen
w.keypad(1) # intialize to get keyboard input
w.timeout(1000) # set game speed, higher value = slower game

snakeTemp = sock.recv(1024) #2.1: recv snake dimensions
sock.send(ack.encode()) #2.2: send ack

snakeTemp = snakeTemp.decode() # decode string into array
snake = ast.literal_eval(snakeTemp)

myPlayNum = sock.recv(1024) #3.1: recv number of players
sock.send(ack.encode()) #3.2: send number ack

myPlayNum = ast.literal_eval(myPlayNum.decode())
mySnake = snake[myPlayNum] #get mySnake
food = [sh/2, sw/2]

w.addch(food[0], food[1], curses.ACS_PI) #render first food
key = curses.KEY_RIGHT #intially input is hardcoded to right

while 1: #infinite while loop
	next_key = w.getch() # keyboard input 
	key = key if next_key == -1 else next_key
	# ending conditions
	# if snake reaches border or eats himself then end game
	# implement in server
	if mySnake[0][0] in [0, sh] or mySnake[0][1]  in [0, sw] or mySnake[0] in mySnake[1:]:
		curses.endwin()
		quit()
	new_head = [mySnake[0][0], mySnake[0][1]]
# encode next move in the string, and then send it to socket
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

	temp = str([message] + mySnake) 
	sock.recv(1024) #4.1: recv wait for ack
	sock.send(temp.encode()) #4.2: send input

	reply = sock.recv(1024) #5.1: recv validated input
	sock.send(ack.encode()) #5.2: send ack

	tFood = sock.recv(1024) #6.1: recv food
	sock.send(ack.encode()) #6.2: send ack
	
# move mySnake according to keyboard input 
	resp = ast.literal_eval(reply.decode())
	response = str(resp[0])
	if response == "down":
		new_head[0] += 1
	if response == "up":
		new_head[0] -= 1
	if response == "left":
		new_head[1] -= 1
	if response == "right":
		new_head[1] += 1

	mySnake.insert(0, new_head) #edit snake, to this in server
	w.addch(food[0], food[1], ' ') #remove old food
	food = ast.literal_eval(tFood.decode())
	w.addch(food[0], food[1], curses.ACS_PI) # render new food

	w.clear()
	w.box()
	mySnake.pop()# pop from tail
	snake[myPlayNum]=mySnake
	render(snake,2) #render on screen
	w.refresh()
# sock.close()

# need to deal with tail error maybe array is going out of bounds