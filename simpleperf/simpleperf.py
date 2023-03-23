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


def mota_melding(sock): #another function/thread to listen for messages
    while True:
         msg = sock.recv(1000).decode()
         if msg == "ACK:BYE":
              print(msg)
              break
         print(msg)
    data_length = sock.recv(1024).decode()
  
    print(data_length)


def send(sock):
    total_data_sendt =0
    intervall_data_sendt = 0
    while True: 
        data =  b"0" * 1000
        antall= args.num
        start_time = time.time()
        while time.time()- start_time <args.time:
              for i in range (antall/1000):
                  sock.send(data)
        
           
        break
    sock.send('BYE'.encode())
    tilbakemelding=sock.recv(1000).decode()   
    #if (tilbakemelding=="ACK:BYE"):

 # for i in range (0, len(data), chunk_size):
             #    sock.send(data[i:i+chunk_size])
              #   data_sendt += len(data)


def handle_client(connection,addr):#A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
    timeStart=time.time()
    data_lengt=0
    start_time = time.time() # Start time for data transfer
    transfer_rate = 0 # Set transfer_rate to 0 initially
    while True:
        data = connection.recv(1024).decode() 
        data_lengt += len(data)
        if(data == "BYE"): 
            connection.send("ACK:BYE".encode())
            break
    end_time = time.time()
    duration = end_time-start_time
    transfer_rate =(data_lengt / duration) * 8 / 1000000# Update transfer_rate on each iteration of the loop
    bandwidth =transfer_rate
    regnut(duration,data_lengt,args)
   
    "for å skrive ut til server "
    """
    output_format = "{:<20} {:<5}     {:<15}{:<5}"
    output = output_format.format("ID", "Interval", "Transfer", "Rate") 
    output += "\n{:<20} {:<5}     {:<15} {:<5} ".format(
    f"{args.bind}:{args.port}", f"0.0-{duration:.1f}",f" {data_lengt}", f"{transfer_rate:.2f}")
    """
    
    "For å skrive ut til klienten "
    output1_format = "{:<20} {:<5}     {:<15}{:<5}"
    output1 = output1_format.format("ID", "Interval", "Transfer", "Bandwidth") 
    output1 += "\n{:<20} {:<5}     {:<15} {:<5} ".format(
    f"{addr[0]}:{addr[1]}", f"0.0-{duration:.1f}",f" {data_lengt}", f"{bandwidth:.2f}")  
    connection.send(output1.encode())
    connection.close()

def regnut(duration,data_length,args):
    total_data= 0
    if(args.format =="B"):
        total_data = data_length
    elif (args.format == "KB"):
        total_data = f"{data_length/1000:.0f}"
    elif (args.format == "MB"):
        total_data = f"{data_length/1000000.0:.0f}"
    transfer_rate =((float(total_data))/ duration) * 8 / 1000000
    output_format = "{:<20} {:<5}     {:<15}{:<5}"
    output = output_format.format("ID", "Interval", "Transfer", "Rate") 
    output += "\n{:<20} {:<5}     {:<15} {:<5} ".format(
    f"{args.bind}:{args.port}", f"0.0-{duration:.1f}",f"{total_data}", f"{transfer_rate}")
    print(output)




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
parser.add_argument("-t", "--time", type=int, help="Duration in seconds", default=25)

parser.add_argument('-i', "--interval", type=int,
                        help='Interval for statistics output in seconds')
parser.add_argument('-P', '--parallel', default=1, type=int, help='The number of parallel connections to establish with the server (default: 1)')
parser.add_argument('-n','--num', default=1000, type=int)
args = parser.parse_args()


if args.server:
    server(args.bind,args.port)

elif args.client: 
    if(args.parallel >0 and args.parallel <6):       
        for i in range(0, int(args.parallel)):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                 sock.connect((args.server_ip,args.port))
            except:
                print("Error: failed to connect to client")
            t1 = threading.Thread(target=mota_melding, args=(sock,))
            t2 = threading.Thread(target=send, args=(sock,))
            t1.start()
            t2.start()
    else:
        print("-P kan ikke være større enn 5")
else:
	print("Error: you must run either in server or client mode")
	    


"""
def send(sock):
    bytes_sent = 0
    while True:
        data = b"0" * 1000
        sock.send(data)
        bytes_sent += len(data)
        if bytes_sent  > 100000:
            break
    sock.send("BYE".encode())


def send():
    while True:
        msg = "BYE".encode()
        sock.send(msg)
        break
"""
""" 
    print(addr)
    connection.send("HEEEEI".encode())
    time.sleep(1)
    connection.close()
 """