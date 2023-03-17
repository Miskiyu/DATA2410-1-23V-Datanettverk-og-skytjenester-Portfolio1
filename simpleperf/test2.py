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
parser = argparse.ArgumentParser(description="optional arguments", epilog="End of help")
message_length = '0'*1000  


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
    ip = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",val)
    if(ip):
        return True
    else:
        print("this is not valid ip-adress")
        sys.exit()  


def handleClient(connection, addr ): #A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
	print(f"A simpleperf client with {addr[0]}:{addr[1]} is connected with ")
	totea_bytes = 0
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
	print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connectionSocket, addr = sock.accept() #Accepting a new connection
		thread= threading.Thread(target=handleClient, args =(connectionSocket,addr))
		thread.start()

def calculate_result(format, value):
    if format == "B":
        result = value
    elif format == "KB":
        result = value / 1024
    elif format == "MB":
        result = value / 1024 / 1024
    else:
        raise ValueError(f"Invalid format specified: {format}")
    return result


def main():
    parser.add_argument('-s','--server', action='store_true')
    parser.add_argument('-p','--port', type=check_port)
    parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
    parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
    parser.add_argument('-c','--client', action='store_true')
    parser.add_argument("-I", "--server_ip", type=str, help="server IP address for client mode")
    parser.add_argument('-P', '--server_port', type=int, help='The IP address to bind to (default: localhost)')
    args = parser.parse_args()
    print(args)
host = args.bind
port = args.port


def send_thread():
	while True: 
		sentence = input("Enter message (type 'bye' to disconnect): ") #asks for client input
		sock.send(sentence.encode()) #sending the input to the server
		if (sentence == DISCONNECT): #if the inpout is exit, the client stops
			message = "Vil du avslutte?(ja/nei):"
			sock.send(message.encode())
			response = sock.recv(100).decode().strip().lower()
			if response == "ja":
				print("serveren avsluttes")
				sock.close
			else:
				print("Klienten ønsker ikke å avslutte.")


def receive_thread(sock): #another function/thread to listen for messages
	msg =""
	while True: 
		received_line = sock.recv(1000).decode() #When a message is recieved from the client, it is decoded. The message has 1024 bytes.
		print ('\nFrom Server:', received_line) #prints the menssage recieved from the server
		if (received_line == DISCONNECT): #if the message is "bye", the thread stops. This is done to prevent infinate looping
			break
		else:
			print(msg)
			pass
	sock.close()


if args.server:
    server(host,port)

elif args.client:        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = args.bind
    port = args.port
    try:
        sock.connect((args.server_ip,args.server_port))
	
        print(f"A simpleperf client with IP {args.server_ip}:{args.server_port} is connected with <server IP:port>")
        t1 = threading.Thread(target=send_thread, args=())
        t2 = threading.Thread(target=receive_thread, args=(sock,))
        t1.start()
        t2.start()
        
    except:
	    print("Error: failed to connect to server")
else:
	print("Error: you must run either in server or client mode")
	    
	    