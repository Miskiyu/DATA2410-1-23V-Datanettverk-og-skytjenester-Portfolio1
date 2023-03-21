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


def mota_melding(): #A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
    while True:
         msg = sock.recv(1000).decode()
         if msg != "":
              print(msg)


def handle_client(connection,addr):
     print(addr)
     connection.send("HEEEEI".encode())
     time.sleep(1)
     connection.close()


def server(host, port): #main method
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host,port))	
    except:
        print("Feil til å koble seg på")
	
    print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
    sock.listen()
    while True: #always true, this will always loop, and wait for new cleints to connect
        connectionSocket, addr = sock.accept() #Accepting a new connection
        print(f"A simpleperf client with IP {str(args.server_ip)}:{str(args.port)} is connected with {str(args.server)}:{str(args.port)}")
        thread= threading.Thread(target=handle_client, args =(connectionSocket,addr))
        thread.start()
                

parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=str, help="server IP address for client mode")
parser.add_argument('-i', "--interval", type=int,
                        help='Interval for statistics output in seconds', default=25)
parser.add_argument('-P', '--parallel', default=1, type=int, help='The number of parallel connections to establish with the server (default: 1)')

args = parser.parse_args()




        # receive and print the result message sent by the server
        

if args.server:
    server(args.bind,args.port)

elif args.client:        
    for i in range(0, int(args.parallel)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
             sock.connect((args.server_ip,args.port))
        except:
            print("Error: failed to connect to client")
        print("hei")
        t1 = threading.Thread(target=mota_melding)
        t1.start()
else:
	print("Error: you must run either in server or client mode")
	    
	    