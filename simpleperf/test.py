"""
DATA 2410EKSAMEN: 
"""
import _thread as thread #importing needed packets
import socket
import sys
import threading #importing needed packets
import argparse
import re
import time
from tabulate import tabulate


parser = argparse.ArgumentParser(description="optional arguments", epilog="End of help")



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

#This function takes in a single argument val. The purpose of the function is to check wheter the value provieded is a valid IP address 
def check_ip(val):
    ip = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",val)
    if not ip: 
        raise ValueError("This is not a valid IP address")
    return val 
       
    


def format_bytes(val):
    match = re.match(r"^(\d+)(B|KB|MB)$", val)
    if not match:
        raise ValueError("Expected a number followed by B, KB or MB")
    size, unit = match.groups()
    size = int(size)
    if unit == "KB":
        size *= 1000
    elif unit == "MB":
        size *= 1000000
    return size

def send_for_duration(sock,duration):
        data = b'0'*1000
        start = time.time()
        end = start + duration
        byte_send = 0
        while time.time() < end:
            sock.send(data)
            byte_send += 1000
          
        sock.send("BYE".encode())
        skrivut(sock,byte_send)

def send_at_intervals(sock,intervall0, tid):
     data_sendt = 0
     total_data_sent = 0
     data = b'0'*1000
     end_time=time.time()+tid
     start_time = time.time()
     intervall =intervall0
     interval_start =  0
     while time.time() <end_time:
        sock.send(data)
        data_sendt += 1000
        if time.time() > intervall + start_time:
            total_data_sent += data_sendt
            elapsed_time = time.time() - start_time
            total_data_sent += data_sendt
            interval_end = elapsed_time
            bandwidth = (data_sendt/1000000*8) / intervall0
            if(args.format =="B"):
                total_data = data_sendt
            elif (args.format == "KB"):
                total_data = data_sendt/1000
            else:
                total_data = data_sendt/1000000.0 
                result= [[f"{args.server_ip}:{args.port}",f"{interval_start:.1f} - {interval_end:.1f}",f" {total_data:.0f} {args.format}",f"{ bandwidth:.2f}Mbps"]]
                headers = ['ID', 'Interval','Transfer','Bandwith']
                print(tabulate(result, headers=headers))
                intervall+= intervall0
                interval_start = elapsed_time
                data_sendt = 0
        sock.send("BYE".encode())
        skrivut(sock, total_data_sent)


def send_num(sock,num):
    data_sendt =0
    bandwidth = 0
    data =  b"0" * 1000 
    size = num
    start_time = time.time()
    remaining_data = 0
    for i in range(999, size,1000):
        sock.send(data)
        data_sendt += 1000
    remaining_data = size%1000
    if remaining_data !=0:
        sock.send(b'0'*remaining_data)
        data_sendt +=remaining_data
    sock.send('BYE'.encode())
    end_time = time.time()
    duration = end_time - start_time
    if duration == 0:
        duration = 1
    melding = sock.recv(1000).decode()
    if "ACK:BYE" in melding:
        bandwith = (data_sendt/1000000*8)/(duration)
        if(args.format =="B"):
            total_data = data_sendt
        elif (args.format == "KB"):
            total_data = data_sendt/1000
        else:
            total_data = data_sendt/1000000.0 
        result = [[f"{args.server_ip}:{args.port}", f"0.0-{duration:.1f}", f" {total_data:.0f} {args.format}", f"{bandwith:.2f} Mbps"]]
        headers = ['ID', 'Interval', 'Transfer', 'Bandwith']
        print(tabulate(result, headers=headers))




def skrivut(sock,byte_send):
    melding = sock.recv(1000).decode()
    if "ACK:BYE" in melding:
        bandwith = (byte_send/1000000*8)/(args.time)
        if(args.format =="B"):
         total_data = byte_send
        elif (args.format == "KB"):
         total_data = byte_send/1000
        else:
         total_data = byte_send/1000000.0 
        result = [[f"{args.server_ip}:{args.port}", f"0.0-{args.time:.1f}", f" {total_data:.0f} {args.format}", f"{bandwith:.2f} Mbps"]]
        headers = ['ID', 'Interval', 'Transfer', 'Bandwith']
        print(tabulate(result, headers=headers))


def handle_client(connection,addr):#A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
    data_lengt=0
    start_time = time.time() # Start time for data transfer
    transfer_rate = 0 # Set transfer_rate to 0 initially
    total_data=0
    while True:
        data = connection.recv(1024).decode() 
        data_lengt += len(data)
        if "BYE" in data:
            connection.send("ACK:BYE".encode())
            break 
    end_time = time.time()
    if(args.format =="B"):
        total_data = data_lengt
    elif (args.format == "KB"):
        total_data = data_lengt/1000
    elif (args.format == "MB"):
        total_data = data_lengt/1000000
   
    duration = end_time-start_time
    transfer_rate =(data_lengt / duration) * 8 / 1000000# Update transfer_rate on each iteration of the loop
  
    #Creates a table to display the results
    data = [[f"{addr[0]}:{args.port}",f"0.0-{duration:.1f}",f" {total_data:.0f} {args.format}",f"{transfer_rate:.2f} Mbps"]]
    headers = ['ID', 'Interval','Transfer','Rate']
    print(tabulate(data, headers=headers))# The table is printed using the tabulate function from the tabulate module.
    connection.close()#then close the connections 

def server(host, port): #main method
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host,port))	
    except:
        print("Feil til å koble seg på")
        sys.exit()
	
    print('------------------------------------------------')
    print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
    print('-------------------------------------------------')
    sock.listen()
    while True: #always true, this will always loop, and wait for new cleints to connect
        connectionSocket, addr = sock.accept() #Accepting a new connection
        print(f"A simpleperf client with IP {args.server_ip}:{str(args.port)} is connected with {args.bind}:{args.port}")
        thread= threading.Thread(target=handle_client, args =(connectionSocket,addr))
        thread.start()
                
#Defines and parses command line arguments using the argparse library in Python. 
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port, default=8088)
parser.add_argument('-b', '--bind', default=socket.gethostbyname(socket.gethostname()) , type=check_ip, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=check_ip, default=socket.gethostbyname(socket.gethostname()) ,help="server IP address for client mode",)
parser.add_argument("-t", "--time", type=int, help="Duration in seconds")

parser.add_argument('-i', "--intervall", type=int,
                        help='Interval for statistics output in seconds')
parser.add_argument('-P', '--parallel', default=1, type=int, help='The number of parallel connections to establish with the server (default: 1)')
parser.add_argument('-n','--num',  type=format_bytes)
args = parser.parse_args()




if args.server and args.client:
        print("Error: Cannot run both server and client mode")
        sys.exit()

elif args.server:
    server(args.bind,args.port)

elif args.client: 

    if(args.parallel >0 and args.parallel <6):       
        for i in range(0, int(args.parallel)):    
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                 sock.connect((args.server_ip,args.port))
                 print('--------------------------------------------------------------------------------')
                 print ('A SIMPLEPERF CLIENT IS CONNECTION TO SERVER IP',args.server_ip,'PORT',args.port) 
                 print('--------------------------------------------------------------------------------')
            except:
                print("Error: failed to connect to client")
                sys.exit()

            try:
                if args.time:
                    send_for_duration(sock, args.time)
                elif args.intervall and args.time:
                    send_at_intervals(sock, args.intervall, args.time)
                elif args.num and not args.time and not args.intervall:
                    send_num(sock, args.num)
            except:
                print('Failed to send data to server.')
    
    else:
        print("-P kan ikke være større enn 5")
        sys.exit()
else:
	print("Error: you must run either in server or client mode")
 
	    