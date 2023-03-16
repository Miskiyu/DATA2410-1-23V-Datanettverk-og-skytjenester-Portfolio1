"""
Server side: open a socket on a port, listen for a message 
from a client, and send an echo reply; 
echoes lines until eof when client closes socket; spawns a 
thread to handle each client connection; threads share global 
memory space with main thread.
"""

import _thread as thread #importing needed packets
import socket
import sys
import threading #importing needed packets
import argparse
import re

DISCONNECT = "bye"
parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")



"""Her lager jeg en funksjon som sjekker om porten er valid"""
def check_port(val):
    try:
        value = int(val)
        if not (1024 <= value <= 65535):
             print("Error: Port must be between 1024 and 65535")
             sys.exit()
        return value
    except ValueError:
        raise argparse.ArgumentTypeError("Expected an integer but you entred a string")
    
def check_ip(val):
    ip = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",val)
    if(ip):
        return True
    else:
        print("this is not valid ip-adress")
        sys.exit()  


def handleClient(connection): #A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
	while True:
		msg = connection.recv(1000).decode()   #Decoding recieved message
		print ("received  message = ", msg)   #Printing the recieved message on the server side
		if (msg== DISCONNECT):  
			melding_send = DISCONNECT.encode()
			connection.send((melding_send))
			break  #Exiting the loop
		else:
			melding_send = "Do you want to quit this session?".encode()
	connection.close() #closing the socket

def server(host, port): #main method
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host,port))	
	sock.listen()
	print ('A SIMPLEPERF SERVER IS LISTENING ON PORT 1025',port) #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connectionSocket, addr = sock.accept() #Accepting a new connection
		
		

def client(host, port):
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((host, port))
	print("Connected to the server.")
	while True:
		msg = input("Enter message (type 'bye' to disconnect): ")
		clientSocket.send(msg.encode())
		if msg == DISCONNECT:
			break
		data = clientSocket.recv(1000).decode()
		print("Server response: ", data)
	clientSocket.close()

#lager server 
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-c','--client', action='store_true')
args = parser.parse_args()
host = args.bind
port = args.port

if __name__ =="__main__":
    if args.server:
        server(host,port)
    elif args.client:
          if check_port(port):
                client(host,port)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Socket settings. THe first says what kind of adress we are looking for,


def sendthread():
	while True: 
		sentence = input("Enter message (type 'bye' to disconnect): ") #asks for client input
		clientSocket.send(sentence.encode()) #sending the input to the server
		if (sentence == DISCONNECT): #if the inpout is exit, the client stops
			msg = sentence.encod()
			clientSocket.send(msg)
			break #stops the loop
		else:
			msg = sentence.encode()
			clientSocket.send(msg)
def thread2(): #another function/thread to listen for messages
	msg =""
	while True: 
		received_line = clientSocket.recv(1024).decode() #When a message is recieved from the client, it is decoded. The message has 1024 bytes.
		print ('\nFrom Server:', received_line) #prints the menssage recieved from the server
		if (received_line == DISCONNECT): #if the message is "bye", the thread stops. This is done to prevent infinate looping
			break #break as before
		else:
			print(msg)
	clientSocket.close()

t1 = threading.Thread(target=thread1) #making a thread

host = socket.gethostbyname(socket.gethostname()) #getting the ip name of the server using this function. That makes this code usable for not only one machine

serverPort = 12000 #defining the server port (which is the same as in the server part of the code)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Socket settings. THe first says what kind of adress we are looking for,
#and the second is the standard option for what we will use the socket for.
try:
	clientSocket.connect((host,serverPort)) #trying to connect
except:
	print("ConnectionError") #if we can't conenct, an error message is created
	sys.exit() #and afterwards we exit the system

t1.start() #starting thread 1
thread2() #and thread 2 (the ) is already running, so we just use a normal function.

