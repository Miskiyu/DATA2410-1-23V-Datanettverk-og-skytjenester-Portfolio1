import socket
import time
import argparse

parser = argparse.ArgumentParser(description='Simpleperf tool for measuring network throughput in server mode')
parser.add_argument('-s', '--server', action='store_true', help='enable the server mode')
parser.add_argument('-b', '--bind', type=str, default='127.0.0.1', help='IP address of the server interface')
parser.add_argument('-p', '--port', type=int, default=8088, help='port number on which the server should listen')
parser.add_argument('-f', '--format', type=str, default='MB', choices=['B', 'KB', 'MB'], help='choose the format of the summary of results')
parser.add_argument("-I", "--serverip", type=str, help="server IP address for client mode")
parser.add_argument("-t", "--time", type=int, default=50, help="time to run in seconds (default: 50)")
parser.add_argument("-f", "--format", type=str, default="MB", choices=["B", "KB", "MB"], help="format to display results in (default: MB)")
parser.add_argument("-i", "--interval", type=int, default=10, help="interval to print statistics in seconds (default: 10)")
parser.add_argument("-P", "--parallel", type=int, default=1, choices=range(1, 6), help="number of parallel connections (default: 1, max: 5)")
parser.add_argument("-n", "--num", type=str, help="number of bytes to send in client mode (e.g. 1MB)")
args = parser.parse_args()

if args.server:
    BUFFER_SIZE = 1000
    total_bytes = 0
    start_time = None
    end_time = None

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = args.bind
    port = args.port

    # bind the socket to a public host, and a well-known port
    s.bind((host, port))

    # become a server socket
    s.listen(1)

    print(f"A simpleperf server is listening on port {args.port}")

    while True:
        # establish connection with client
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        start_time = time.time()

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            total_bytes += len(data)

        end_time = time.time()
        conn.close()

        duration = end_time - start_time
        throughput = total_bytes / duration
        if args.format == 'B':
            print(f"{total_bytes} Bytes received in {duration:.2f} seconds, {throughput:.2f} Bytes/s")
        elif args.format == 'KB':
            print(f"{total_bytes/1000} KB received in {duration:.2f} seconds, {throughput/1000:.2f} KB/s")
        else:
            print(f"{total_bytes/1000000} MB received in {duration:.2f} seconds, {throughput/1000000:.2f} MB/s")

if args.client:
    def send_melding(host, port, tid_valgt ):
        print("A simpleperf client connection to server {args.bind}, port {args.port}")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host,port))

    #send data
        data =  b'\x00' * 1000
        start_tid = time.time()
        bytes_sendt = 0
        while time.time() - start_tid < tid_valgt:
            client_socket.send(data)
            bytes_sendt += len(data)
    
    #Send hade melding og vent 
        client_socket.send(b'finish')
        melding_tilbake = client_socket.recv(1024)
        if melding_tilbake!= b'ack':
            print('Erro: du har ikke fått tilbake melding fra server ')
        client_socket.close()
        tid = time.time() - start_tid
        bandwidth = bytes_sendt / (tid * 1000000)  # In MB/s
        print(f'Bandwidth: {bandwidth:.2f} MB/s')

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



parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=str, help="server IP address for client mode")
parser.add_argument('-P', '--server_port', type=int, help='The IP address to bind to (default: localhost)')
args = parser.parse_args()
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
	    
	    