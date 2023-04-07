"""
DATA 2410EKSAMEN: 
"""


#Different module import used 
import socket
import sys
import threading #importing needed packets
import argparse
import re
import time
import ipaddress  # Import the 'ipaddress' module
from tabulate import tabulate


#Functions to check input values

#Here I create a function that checks whether the port is valid
def check_port(val):
    try:
        value = int(val)
        if not (1024 <= value <= 65535): #if the port is not between 1024 and 65535
             print("Error: Port must be between 1024 and 65535")  #print error message
             sys.exit()
        return value                     #if the port is valid return the value 
    except ValueError:
        raise argparse.ArgumentTypeError("Expected an integer but you entred a string")

#This function takes in a single argument ip. The purpose of the function is to check wheter the value provieded is a valid IP address 
def check_ip(ip):
    try:
        val= ipaddress.ip_address(ip) # use the ipaddress module to create an ip_address object with the given IP address
    except ValueError:  # If a ValueError is raised (the IP address is not valid)
        print(f'The IP address is not valid') #print a message indicating that the IP address is not valid
    else: #If no exception is raised (the IP address is valid)
        return ip   #Return the ip address


#A function that takes a string as input and formats it to a number in bytes
def formater_num(val):
    val = val.upper() # convert the input string to uppercase
    if not re.match(r"\d+(B|KB|MB)", val): # check if the input matches B, KB or MB in uppercase
        raise Exception("The format of bytes that can be sent is a number followed by either B, KB, or MB.") # if it does not match, an error message is printed
    a = int(re.findall(r"\d+", val)[0]) # extract the numerical value from the string using re.findall(). [0] is used to extract the first match since there could be multiple matches.
    if re.findall(r'(KB)', val): # if it is KB, then the value is multiplied by 1000
        return a * 1000
    elif re.findall(r'(MB)', val): # if it is MB, then the value is multiplied by 1000000
        return 1000000 * a
    return a         # if the input is B, then the value of a is returned





#Defines and parses command line arguments using the argparse library in Python. 
parser = argparse.ArgumentParser(description="Simpleperf is a simple program for measuring netwrok thrugput.", epilog="End of help")

parser.add_argument('-s','--server', action='store_true', help='enble the server mode')
parser.add_argument('-p','--port', type=check_port, default=8088)
parser.add_argument('-b', '--bind', default='127.0.0.1' , type=check_ip, help='The IP address to bind to (default: 127.0.0.1)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true', help='enable the client mode')
parser.add_argument("-I", "--serverip", type=check_ip, default='127.0.0.1' ,help="server IP address for client mode (default: 127.0.0.1)")

parser.add_argument("-t", "--time", type=int, help="Duration in seconds, Must be > 0. Default: 25 sec", default=25)
parser.add_argument('-i', "--intervall", type=int,
                        help='Interval for statistics output in seconds')
parser.add_argument('-P', '--parallel', default=1, type=int, choices=range(1,6), help='The number of parallel connections to establish with the server (default: 1)')
parser.add_argument('-n','--num',  type=formater_num, help='transfer number of bytes, it shoud be either in B,KB or MB')
args = parser.parse_args()


#Fuction that takes in sock,elapsed_time and how much data send, and prints result
def print_result(mode, addr, elapsed_time,byte_send):
   port = addr [1]
   ip=addr[0]
 
   bandwith = (byte_send/1000000*8)/(elapsed_time) #This line calculates the bandwidth/rate in Mbps
   if(args.format =="B"):
         total_data = byte_send
   elif (args.format == "KB"):
         total_data = byte_send/1000
   else:
         total_data = byte_send/1000000.0 

   if mode == "C":
        headers = ['ID', 'Interval', 'Transfer', 'Bandwith']
   elif mode == "S":
        headers=  ["ID", "Interval", "Recieved", "Rate"]
    
   result = [[f"{ip}:{port}", f"0.0-{elapsed_time:.1f}", f" {total_data:.0f} {args.format}", f"{bandwith:.2f} Mbps"]]
       
   print(tabulate(result, headers=headers))
   print(" ")




"""SERVER"""
#this function creates a socket that listens on a specified host and port for incoming
#  connections from clients. Once a client connects, a new thread is created to handle the
# client's requests, and the server continues to listen for new connections. 
# The function also prints out a message indicating that the server is listening on the specified port.
def server(host, port): #main method
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket object
        sock.bind((host,port))	# binds the socket to the specified ip and port
    except:  # if an error occurs while binding the socket, print an error message and exit the program 
        print("Failed to connect")
        sys.exit()
	
    print('------------------------------------------------')
    print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
    print('-------------------------------------------------')
    sock.listen() # listen for incoming connections
    while True: #always true, this will always loop, and wait for new cleints to connect
        connectionSocket, addr = sock.accept() #Accepting a new connection
        print(f"A simpleperf client with IP {addr[0]}:{str(addr[1])} is connected with {host}:{port} \n")
        thread= threading.Thread(target=handle_client, args =(connectionSocket,addr))
        thread.start()


def handle_client(connection,addr):#A client handler function, this function get's called once a new client joins, and a thread gets created (see main)
    data_lengt=0
    start_time = time.time() # Start time for data transfer
    while True: # Loop forever until a break statement is encountered
        data = connection.recv(1000).decode()  # Receive data from the client and decode it 
        data_lengt += len(data)  # Update the total length of data received from the client
        if "BYE" in data:   # If the client sends a "BYE" message, send an acknowledgement and break out of the loop
            connection.send("ACK:BYE".encode())
            break 
    end_time = time.time()   # Record the end time 
  
    duration = end_time-start_time  #sets how long the data was sent 
    print_result('S',addr,duration,data_lengt)

    connection.close()#then close the connections 



#This function takes a socket, ip and port as input, based on the user-provided arguments,
 #calls the appropriate function to send data over the socket.
 #The three possible functions that can be called are number_of_bytes, send_for_duration, and send_at_intervals
def client_send(sock, serverip,port):
    print(f'A simpleperf client is connecting with {serverip}, port {port} \n') 

    clientip = sock.getsockname()[0]
    clientport = sock.getsockname()[1]
    addr= (clientip,clientport)

    data = b'0'*1000 # Set the data to be sent as 1000 bytes of 0  
    byte_send = 0    # Initialize a variable to keep track of the total number of bytes sent
    start = time.time() # Get the start time of the function
        
    if args.num:
        size = args.num   # sets a variable 'size' to the value of args.num, which is passed as an argument to the function and specifies the total number of bytes to send
         
         # Send data in chunks of 1000 bytes until size is reached
        for i in range(999, size, 1000):   # loops from 999 to size (excluding size) in steps of 1000 bytes
            sock.send(data)   # sends a chunk of 1000 bytes to the connected socket
            byte_send += 1000   # adds 1000 to the total number of bytes sent

    # Send remaining data
        remaining_data = size % 1000   # calculates the remaining data after sending all 1000-byte chunks
        if remaining_data != 0:   # if there is remaining data
            sock.send(b'0' * remaining_data)   # sends the remaining data (less than 1000 bytes)
            byte_send += remaining_data   # adds the number of remaining bytes to the total number of bytes sent
   
   
    # If the user provided the "time" argument
    elif args.time:
        end_time= start + int(args.time)  # Set the end time to be the start time plus the duration specified in the arguments 
        while time.time() < end_time:    # Loop until the current time is greater than the end time
            sock.send(data)    # Send the data over the socket
            byte_send +=len(data)        # Add the number of bytes sent to the total number of bytes sent  
   
    
    elif args.interval:
         data_sent = 0
         byte_send = 0
         data = b'0'*1000
             # Calculate the end time for sending data
         end_time = time.time() + args.time
         start_time = time.time()
        # Set the interval for sending data
         interval = args.intervall
         interval_start = 0
         # Keep sending data until the end time is reached
         while time.time() < end_time:
            # Send data
             sock.send(data)
             data_sent += len(data)
             # Check if an interval has passed
             if time.time() > interval + start_time:
                 # Calculate and print the results for the interval
                 byte_send += data_sent
                 elapsed_time = time.time() - start_time
                 interval_end = elapsed_time
                 bandwidth = (data_sent / 1000000 * 8) / args.intervall
                 if args.format == "B":
                    total_data = data_sent
                 elif args.format == "KB":
                     total_data = data_sent / 1000
                 else:
                    total_data = data_sent / 1000000.0 
                 result = [[f"{args.serverip}:{args.port}", f"{interval_start:.1f} - {interval_end:.1f}", f" {total_data:.0f} {args.format}", f"{bandwidth:.2f}Mbps\n"]]
                 headers = ['ID', 'Interval', 'Transfer', 'Bandwidth']
                 print(tabulate(result, headers=headers))
                 # Update the interval start and reset the data sent
                 interval += args.intervall
                 interval_start = elapsed_time
                 data_sent = 0
    end_time = time.time()   # records the end time of the data transfer
    duration = end_time - start  # calculates the duration of the data transfer
    sock.send("BYE".encode())        # Send "BYE" to signal the end of the transmission
    print_result('C',addr,  duration,byte_send)  #  Print the result of the transmission
    sock.close()

    



#INNVOKING CLIENT OR SERVER MODE 

if args.server and args.client: #gives error if both of client and client is envoked 
    print("Error: Cannot run both server and client mode")
    sys.exit()

#if server is chosed sends port and ip to server function
elif args.server:
    server(args.bind,args.port)

elif args.client: 
    # Create multiple client threads, each with its own socket
    for i in range(0, int(args.parallel)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a new socket object
        
        try:
            sock.connect((args.serverip,args.port)) #binds the socket to ip and port and prints a message
            # Print a message indicating that a client is connecting to the server
            print('--------------------------------------------------------------------------------')
            print ('A SIMPLEPERF CLIENT IS CONNECTION TO SERVER',args.serverip,',PORT',args.port) 
            print('--------------------------------------------------------------------------------')
                 
        except:#if failet to connect sends a error message 
            print("Error: failed to connect to client")
            sys.exit()
        # Create a new thread for the current client, and start it
        t2 = threading.Thread(target=client_send, args=(sock,args.serverip,args.port))
        t2.start()
  
else:
    # If neither '-s' nor '-c' is specified, print an error message and exit
    print("Error: you must run either in server or client mode")
