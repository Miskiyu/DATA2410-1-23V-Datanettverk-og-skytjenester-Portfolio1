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


def handle_client(client_socket, address):
    print(f"A simpleperf client with {address[0]}:{address[1]} is connected with IP:{address[1]}")

    while True:
        message = input("Enter message (type 'bye' to disconnect): ")
        client_socket.send(message.encode())

        if message == DISCONNECT:
            client_socket.close()
            break

        data = client_socket.recv(1024).decode()
        print(f"Received message from server: {data}")

        if data == DISCONNECT:
            client_socket.close()
            break


def server(host, port): #main method
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host,port))	
	sock.listen()
	print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connectionSocket, addr = sock.accept() #Accepting a new connection
		thread= threading.Thread(target=handle_client, args =(connectionSocket,addr))
		thread.start()
		

#lager server 
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=str, help="server IP address for client mode")
parser.add_argument('-P', '--server_port', default='localhost', type=int, help='The IP address to bind to (default: localhost)')

args = parser.parse_args()
host = args.bind
port = args.port

"""	
def send_thread(sock):
	while True: 
		sentence = input("Enter message (type 'bye' to disconnect): ") #asks for client input
		sock.send(sentence.encode()) #sending the input to the server
		if (sentence == DISCONNECT): #if the inpout is exit, the client stops
			msg = sentence.encode()
			sock.send(msg)
			break #stops the loop
		else:
			msg = sentence.encode()
			sock.send(msg)

def receive_thread(): #another function/thread to listen for messages
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
"""	

if args.server:
    server(host,port)

if args.client:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    address = (args.server_ip, args.server_port)

    try:
        client_socket.connect(address)
        t = threading.Thread(target=handle_client, args=(client_socket, address))
        t.start()
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running on the specified host and port.")

else:
     print("Error: you must run either in server or client mode")
"""    
elif args.client:        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = args.bind
    port = args.port
    try:
        sock.connect((host,port))
	
        print(f"A simpleperf client with IP {args.server_ip}:{args.server_port} is connected with <server IP:port>")
        t1 = threading.Thread(target=send_thread, args=(sock,))
        t2 = threading.Thread(target=receive_thread, args=(sock,))
        t1.start()
        t2.start()
        
	    
	    
	
    except ConnectionRefusedError:
	    print("Could not connect to server.")
"""

import _thread as thread
import socket
import sys
import threading
import argparse
import re
import time

DISCONNECT = "bye"
parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")
message_length = '0'*1000

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
        print("This is not a valid IP address")
        sys.exit()  

def handleClient(connection, addr ):
    print(f"A simpleperf client with {addr[0]}:{addr[1]} is connected with ")

    while True:
        msg = connection.recv(1000).decode()
        print ("Received message = ", msg)
        if (msg== DISCONNECT):
            message_send = DISCONNECT.encode()
            connection.send(message_send)
            break
        else:
            message_send = "Do you want to quit this session?".encode()
            connection.send(message_send)

    connection.close()

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen()
    print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port)
    while True:
        connectionSocket, addr = sock.accept()
        thread= threading.Thread(target=handleClient, args =(connectionSocket,addr))
        thread.start()

def send_thread(sock, duration):
    start_time = time.monotonic()
    sent_bytes = 0
    while time.monotonic() - start_time < duration:
        sock.send(message_length.encode())
        sent_bytes += 1000
    finish_message = "finish".encode()
    sock.send(finish_message)
    response = sock.recv(



import _thread as thread
import socket
import sys
import threading
import argparse

DISCONNECT = "bye"

parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")
parser.add_argument('-s', '--server', action='store_true')
parser.add_argument('-p', '--port', type=int, default=12345)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-c', '--client', action='store_true')
parser.add_argument('-I', '--server-ip', type=str, help='The IP address of the server for client mode')
parser.add_argument('-P', '--server-port', type=int, help='The port number of the server for client mode')
parser.add_argument('-t', '--time', type=int, help='The duration in seconds for which the client should send data')
parser.add_argument('-z', '--zero', action='store_true', help='Send all zero data instead of same data')
parser.add_argument('-d', '--data', type=int, default=0, help='The value to send for same data mode (default: 0)')
args = parser.parse_args()

def check_port(val):
    try:
        value = int(val)
        if not (1024 <= value <= 65535):
            raise argparse.ArgumentTypeError("Port must be between 1024 and 65535")
        return value
    except ValueError:
        raise argparse.ArgumentTypeError("Expected an integer but got a string")

def check_ip(val):
    ip = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", val)
    if(ip):
        return True
    else:
        raise argparse.ArgumentTypeError("Invalid IP address")

def handle_client(connection, addr):
    print(f"A simpleperf client with {addr[0]}:{addr[1]} is connected")

    if args.time:
        if args.zero:
            data = '0' * 1000
        else:
            data = str(args.data) * 1000

        bytes_sent = 0
        start_time = time.monotonic()
        while time.monotonic() - start_time < args.time:
            connection.send(data.encode())
            bytes_sent += len(data)

        print(f"Sent {bytes_sent} bytes in {args.time} seconds")

    while True:
        msg = connection.recv(1000).decode()
        print("Received message:", msg)
        if msg == DISCONNECT:
            connection.send(DISCONNECT.encode())
            break
        else:
            connection.send("Do you want to quit this session?".encode())

    connection.close()

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    print(f"A SIMPLEPERF SERVER IS LISTENING ON PORT {port}")

    while True:
        connection_socket, addr = sock.accept()
        thread = threading.Thread(target=handle_client, args=(connection_socket, addr))
        thread.start()

def send_thread(sock):
    while True:
        sentence = input("Enter message (type 'bye' to disconnect): ")
        sock.send(sentence.encode())
        if sentence == DISCONNECT:
            sock.send(DISCONNECT.encode())
            break

    print("Waiting for acknowledgement...")
    response = sock.recv(1024).decode()
    print("Received acknowledgement:", response)
    sock.close()

def receive_thread(sock):
    msg = ''
    while True:
        received
