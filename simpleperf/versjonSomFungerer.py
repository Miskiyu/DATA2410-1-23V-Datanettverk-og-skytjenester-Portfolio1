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
        msg = connection.recv(1000).decode()   #Decoding received message
        if not msg:
             break
        total_bytes_received +=len(msg)
        print(total_bytes_received)
        print ("received  message = ", msg)   #Printing the received message on the server side
        if msg == DISCONNECT:  
            message = "Are you sure you want to disconnect? (yes/no):"
            connection.send(message.encode())
            response = connection.recv(1000).decode().strip().lower()
            if response == "yes":
                message = DISCONNECT.encode()
                connection.send(message)
                duration = time.monotonic() - start_time
                if(args.format == "B"):
                     total_bytes = f"{total_bytes_received} B"
                elif (args.format == "KB"):
                     total_bytes = f"{total_bytes_received/1000} KB "
                elif (args.format == "MB"):
                     total_bytes = f"{total_bytes_received/1000000.0} MB"
                transfer_rate = (total_bytes_received*8)/(duration*1000000)
                rate = round(transfer_rate,2)
                #Denne koden lager en string "interval" som inneholder en tidsperiode fra 0.0 til varigheten av dataoverføringen (i sekunder). "round(duration, 1)" runder av "duration" variabelen til en desimal.
                interval = f"0.0 - {round(duration, 1)}"

                #result = f"Result: ID={addr[0]}:{addr[1]} Interval={duration:.2f} Transfer={total_bytes_received/(1024*1024):.0f} Rate={transfer_rate:.2f} Mbps"
                #result = f"Result: ID={addr[0]}:{addr[1]} Interval:{duration:.2f} recived {total_bytes} Rate {rate} "
                output_format = "{:<10} {:<15} {:<10} {:<10}"
                output = output_format.format("ID", "Interval", "Received", "Rate") 
                output += "\n{:<10} {:<15} {:<10} {:<10} Mbps".format(  
                     f"{addr[0]}:{addr[1]}",  f"{interval}", 
                       f"{total_bytes}",  f"{rate:.2f}")
                connection.send(output.encode())
                print(output)
                break  #Exiting the loop
            else:
                print("Client will not disconnect.")
                connection.send(message.encode())
 
    connection.close() #closing the socket



"""
def handleClient(connection, addr, interval):
    print(f"A simpleperf client with {addr[0]}:{addr[1]} is connected with ")
    total_bytes_received = 0
    start_time = time.monotonic()
    duration = 25  # Change this to the desired test duration
    for t in range(0, duration, interval):
        interval_start_time = time.monotonic()
        interval_bytes_received = 0
        while time.monotonic() - interval_start_time < interval:
            msg = connection.recv(1000).decode()   #Decoding received message
            if not msg:
                break
            total_bytes_received += len(msg)
            interval_bytes_received += len(msg)
            print(total_bytes_received)
            print ("received  message = ", msg)   #Printing the received message on the server side
            if msg == DISCONNECT:
                message = "Are you sure you want to disconnect? (yes/no):"
                connection.send(message.encode())
                response = connection.recv(1000).decode().strip().lower()
                if response == "yes":
                    message = DISCONNECT.encode()
                    connection.send(message)
                    if(args.format == "B"):
                        total_bytes = f"{interval_bytes_received} B"
                    elif (args.format == "KB"):
                        total_bytes = f"{interval_bytes_received/1000} KB "
                    elif (args.format == "MB"):
                        total_bytes = f"{interval_bytes_received/1000000.0} MB"
                    transfer_rate = (interval_bytes_received*8)/(interval*1000000)
                    rate = round(transfer_rate, 2)
                    interval_str = f"{t:.1f} - {t+interval:.1f}"
                    output_format = "{:<10} {:<15} {:<10} {:<10} Mbps"
                    output = output_format.format(
                        f"{addr[0]}:{addr[1]}", interval_str, f"{total_bytes}", f"{rate:.2f}")
                    connection.send(output.encode())
    connection.close()
"""
"""
def handleClient(connection, addr,intervall):
    print(f"A simpleperf client with {addr[0]}:{addr[1]} is connected with ")
    start_time = 0
    total_bytes_received = 0
    timeStart = time.time()
    duration= 4  # Change this to the desired test duration
    for i in range(0, duration, intervall):
        while True:
            interval_bytes_received = 0
            if time.time() - timeStart > intervall:
                msg = connection.recv(1000).decode()   #Decoding received message
                endtime = "%.2f" % ( start_time + (time.time()- timeStart))
                start_time = "%.2f" % start_time
                print(f"{start_time} - {endtime}")
                start_time= float(start_time) + (time.time()-timeStart)
                timeStart = time.time()
                if not msg:
                    break
                total_bytes_received += len(msg)
                interval_bytes_received += len(msg)
                print(total_bytes_received)
                if(args.format == "B"):
                     total_bytes = f"{interval_bytes_received} B"
                elif (args.format == "KB"):
                      total_bytes = f"{interval_bytes_received/1000} KB "
                elif (args.format == "MB"):                        
                      total_bytes = f"{interval_bytes_received/1000000.0} MB"
                transfer_rate = (interval_bytes_received*8)/(intervall*1000000)
                rate = round(transfer_rate, 2)
                interval_str = f"{start_time} - {endtime}"
                output_format = "{:<10} {:<15} {:<10} {:<10} Mbps"
                output = output_format.format(
                f"{addr[0]}:{addr[1]}", f"{interval_str:.2f}", f"{total_bytes}", f"{rate:.2f}")
                connection.send(output.encode())
                
              
    if(args.format == "B"):
        total_bytes = f"{total_bytes_received} B"
    elif (args.format == "KB"):
        total_bytes = f"{total_bytes_received/1000} KB "
    elif (args.format == "MB"):
        total_bytes = f"{total_bytes_received/1000000.0} MB"
    transfer_rate = (total_bytes_received*8)/(intervall*1000000)
    rate = round(transfer_rate, 2)
    start_time= 0
    interval =f"{start_time} - {endtime}"
    output_format = "{:<10} {:<15} {:<10} {:<10} Mbps"
    output = output_format.format(
    f"{addr[0]}:{addr[1]}", interval, f"{total_bytes}", f"{rate:.2f}")
    connection.send(output.encode())
    connection.close()

"""
def server(host, port): #main method
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host,port))	
	sock.listen()
	print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connectionSocket, addr = sock.accept() #Accepting a new connection
		thread= threading.Thread(target=handleClient, args =(connectionSocket,addr,interval))
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
parser.add_argument('-i', "--interval", type=int,
                        help='Interval for statistics output in seconds', default=25)
args = parser.parse_args()
host = args.bind
port = args.port

def send_thread():
    while True: 
        sentence = input("Enter message (type 'bye' to disconnect): ") #asks for client input
        data =  '0'*1000 
        sock.send(sentence.encode()) #sending the input to the server
        if(sentence == DISCONNECT):
             if(sentence == "yes"):
                  break
        
        # receive and print the result message sent by the server
        

    sock.close()

        
def receive_thread(sock):
    while True:
        received_line = sock.recv(1000).decode()
        if not received_line:
            break
        print('\nFrom Server:', received_line)
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
	    
	    