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
    ip = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",val)#function is using re to mathc the input val, withc a pattern that defines the format of an IP address
    if(ip):  #if ip is valid return ip
        return val
    else:#if the string does not match the patter, the code prinst an error message andexit the progamr 
        print("This is not valid ip-adress")
        sys.exit()  


#A function that takes a string as input and formats it to a number in bytes
def formater_num(val):
    if not re.match(r"\d+(B|KB|MB)",val):  #checks if the input matches B,KB or MB
        raise Exception("Formate av bytes du kan sende er et tall og enten B,KB eller MB") #if it does not mathc errror message is printed
    a = int(re.findall(r"\d+",val)[0]) # the function extracts the numerical value from the string using re.findall(). [0] is used to extract the first match since there could be multiple matches.
    if re.findall(r'(KB)',val): #If it is KB then the value is multiplied bye 1000
        return a*1000
    elif re.findall(f'(MB)',val): #it it is MB then the value is multiplied bt 1000000
        return 1000000*a
    return a         #if the input is B then the value of a returns


#Fuction that takes in sock, and how much data send, and prints result
def print_result(sock,byte_send):
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

                
#Defines and parses command line arguments using the argparse library in Python. 
parser = argparse.ArgumentParser(description="optional arguments", epilog="End of help")

parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port, default=8088)
parser.add_argument('-b', '--bind', default=socket.gethostbyname(socket.gethostname()) , type=check_ip, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=check_ip, default=socket.gethostbyname(socket.gethostname()) ,help="server IP address for client mode",)
parser.add_argument("-t", "--time", type=int, help="Duration in seconds", default=25)

parser.add_argument('-i', "--intervall", type=int,
                        help='Interval for statistics output in seconds')
parser.add_argument('-P', '--parallel', default=1, type=int, help='The number of parallel connections to establish with the server (default: 1)')
parser.add_argument('-n','--num',  type=formater_num)
args = parser.parse_args()







"""SERVER"""
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
        print(f"A simpleperf client with IP {addr[0]}:{str(addr[1])} is connected with {args.bind}:{args.port}")
        thread= threading.Thread(target=handle_client, args =(connectionSocket,addr))
        thread.start()


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




def client_send(sock,tid):
    if args.time:
        send_for_duration(sock,tid)

    #ip = sock.getsockname()[0]
    #port = sock.getsockname()[1]

    
def send_for_duration(sock,duration):
        data = b'0'*1000
        start = time.time()
        end = start + duration
        byte_send = 0
        while time.time() < end:
            sock.send(data)
            byte_send += 1000
          
        sock.send("BYE".encode())
        print_result(sock,byte_send)




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
                 
            except:
                print("Error: failed to connect to client")
                sys.exit()
            t2 = threading.Thread(target=client_send, args=(sock,args.time))
            t2.start()
            print('--------------------------------------------------------------------------------')
            print ('A SIMPLEPERF CLIENT IS CONNECTION TO SERVER IP',args.server_ip,'PORT',args.port) 
            print('--------------------------------------------------------------------------------')
    else:
        print("-P kan ikke være større enn 5")
        sys.exit()
else:
	print("Error: you must run either in server or client mode")
 
	    