"""
Server side: open a socket on a port, listen for a message 
from a client, and send an echo reply; 
echoes lines until eof when client closes socket; spawns a 
thread to handle each client connection; threads share global 
memory space with main thread.
"""
from socket import *
import _thread as thread #importing needed packets
import socket
import sys
import threading #importing needed packets
import argparse
import re

liste = [] #List with all clients, needed for the broadcast function

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

def broadcast(client, message): #Broadcast function to broadcast a given message to defined clients
	client.send((message.encode())) #send the specified client the given message
	return

def handleClient(connection): #A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
	
	while True:
		data = connection.recv(1024).decode()   #Decoding recieved message
		print ("received  message = ", data)   #Printing the recieved message on the server side
		if (data == "exit"):  #If a cleint sends Exit, the connection is removed from the server
			liste.remove(connection)  #Removing the connection from the list
			broadcast(connection, "bye")   #Sending a goodbye message. This is also used to prevent infinite looping in the message recieving thread of the client
			break  #Exiting the loop
	connection.close() #closing the socket

def server(host, port): #main method
	serverPort = 12000 #Defining the server port 
	serverSocket = socket(AF_INET,SOCK_STREAM)  
	try:
		serverSocket.bind((host,port)) #binding this socket to this adress
	except: 
		print("Bind failed. Error : ") #error message in case something fails
	serverSocket.listen(1) #Setting up the socket for listening for messages
	print ('The server is ready to receive') #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connectionSocket, addr = serverSocket.accept() #Accepting a new connection
		thread.start_new_thread(handleClient, (connectionSocket,)) #Creating a new thread for the new connection
		connectionSocket.send("Welcome to the server. Type Broadcast: followed by your message to broadcast something".encode()) #This message get's sent when a new connection
		# joins the server
		for i in liste: #This loops though all existing clients that are connected to the server, and broadcasts the given message to them
			broadcast(i, "\n En ny klient har koblet seg til")

parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")


#lager server 
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b','--bind', type=check_ip)
parser.add_argument('-c','--client', action='store_true')
args = parser.parse_args()

if __name__ =="__main__":
    if args.server:
        print("A simpleperf server is listening on port",args.port)
        host = args.bind
        port = args.port
        server(host,port)
	

	

def thread1(): #making one function (/thread) for sending messages to the server
	while True: #this is always true, it always listens for input
		sentence = input('') #asks for client input
		clientSocket.send(sentence.encode()) #sending the input to the server
		if (sentence == "exit"): #if the inpout is exit, the client stops
			break #stops the loop
def thread2(): #another function/thread to listen for messages
	while True: #always true, always lsitening for messages
		received_line = clientSocket.recv(1024).decode() #When a message is recieved from the client, it is decoded. The message has 1024 bytes.
		print ('\nFrom Server:', received_line) #prints the menssage recieved from the server
		if (received_line == "bye"): #if the message is "bye", the thread stops. This is done to prevent infinate looping
			break #break as before

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