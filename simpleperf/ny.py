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
import time

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
    total_bytes_received = 0
    start_time = time.monotonic()
    while True:
        data = connection.recv(1000).decode()   #Decoding received message
        if not data:
             break
        total_bytes_received +=len(data)
        if data == "BYE":
             connection.send(b'ACK:BYE')
    print(total_bytes_received)
    connection.close()
       




def server(host, port): #main method
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host,port))	
	sock.listen()
	print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connection, addr = sock.accept() #Accepting a new connection
		thread= threading.Thread(target=handleClient, args =(connection,addr))
		thread.start()
                

parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=str, help="server IP address for client mode")
parser.add_argument('-i', "--interval", type=int,
                        help='Interval for statistics output in seconds', default=25)
args = parser.parse_args()
host = args.bind
port = args.port

def send_thread():
    while True: 
        data =  b"0" * 1000
        duration =1
        start_time = 10
        while time.time()- start_time <duration:
             msg = data.encode()
             sock.send(msg)
        melding ='BYE'.encode()
        sock.send(melding)       
        



        # receive and print the result message sent by the server
        
       
def receive_thread(client_sock):
    msg =""
    while True:
        data = client_sock.recv(1000).decode()
        if not data:
            break
        if data =='ACK:BYE':
             print(data)
             break
        else:
             msg = data
             print(msg)
    sock.close()


if args.server:
    server(host,port)

elif args.client:        
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = args.bind
    port = args.port
    try:
        sock.connect((args.server_ip,args.port))
	
        print(f"A simpleperf client with IP {args.server_ip}:{args.port} is connected with {args.server}:{args.port}")
        t1 = threading.Thread(target=send_thread, args=())
        t2 = threading.Thread(target=receive_thread, args=(sock,))
        t1.start()
        t2.start()
        
    except:
	    print("Error: failed to connect to server")
else:
	print("Error: you must run either in server or client mode")
	    
	    