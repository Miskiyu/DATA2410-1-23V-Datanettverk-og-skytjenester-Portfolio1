import time

total = 4

intervall = 1
start_time=0
timeStart = time.time()
for i in range(0, total,intervall):
     while True:
          if time.time() - timeStart > intervall:
               endtime = "%.2f" % ( start_time + (time.time()- timeStart))
               start_time = "%.2f" % start_time
               print(f"{start_time} - {endtime}")
               start_time= float(start_time) + (time.time()-timeStart)
               timeStart = time.time()
               break
start_time = 0
print (f"{start_time} - {endtime}")

import argparse
import socket
import time
import threading

def transfer_data(host, port, num_bytes):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        for i in range(num_bytes // 1000):
            sock.send(b'0' * 1000)
        remaining_bytes = num_bytes % 1000
        if remaining_bytes:
            sock.send(b'0' * remaining_bytes)

def run_client(args):
    host = args.host
    port = args.port
    total_bytes = args.num_bytes
    num_parallel = args.parallel
    duration = args.duration

    start_time = time.monotonic()

    threads = []
    for i in range(num_parallel):
        t = threading.Thread(target=transfer_data, args=(host, port, total_bytes//num_parallel))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed_time = time.monotonic() - start_time

    total_bytes_str = f"{total_bytes/(1024*1024):.3f} MB"
    bandwidth = (total_bytes/elapsed_time)/1000000
    bandwidth_str = f"{bandwidth:.3f} Mbps"

    print("ID Interval Transfer Bandwidth")
    for i in range(num_parallel):
        output_format = "{:<10} {:<15} {:<10} Mbps"
        output = output_format.format(
            f"{host}:{port}",
            f"{duration:.1f} seconds",
            f"{total_bytes_str}/{num_parallel}",
            f"{bandwidth_str}"
        )
        print(output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default='localhost', type=str, help='The IP address of the server to connect to (default: localhost)')
    parser.add_argument('-p', '--port', default=8080, type=int, help='The port number of the server to connect to (default: 8080)')
    parser.add_argument('-n', '--num-bytes', type=int, help='The number of bytes to transfer to the server')
    parser.add_argument('-P', '--parallel', default=1, type=int, help='The number of parallel connections to establish with the server (default: 1)')
    parser.add_argument('-t', '--duration', default=25.0, type=float, help='The duration of the transfer in seconds (default: 25.0)')

    args = parser.parse_args()

    run_client(args)

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
         connection.sendall(b'ACK:BYE')
    print(total_bytes_received)
    connection.close()
       




def server(host, port): #main method
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host,port))	
	sock.listen()
	print ('A SIMPLEPERF SERVER IS LISTENING ON PORT',port) #Printing this message on the server
	while True: #always true, this will always loop, and wait for new cleints to connect
		connectionSocket, addr = sock.accept() #Accepting a new connection
		thread= threading.Thread(target=handleClient, args =(connectionSocket,addr))
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
             sock.send(data)
             print(data)
        sock.sendall(b'BYE')    
        print("bye")
        # receive and print the result message sent by the server
        
       
def receive_thread(client_sock):
    while True:
        data = client_sock.recv(1000).decode()
        if not data:
            break
        if data == b'ACK:BYE':
             print(data)
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
	    
	    
def send(sock):   
    print("CLIENT CONNECTED WITH SERVER_IP",args.server_ip,', PORT',args.port)
    data_sendt =0

    bandwith = 0
    data =  b"0" * 1000 
    total_data_sent = 0
    start_time = time.time()
    intervall_time =time.time()
    if not args.num: 
        while time.time()- start_time <args.time:
             sock.send(data)
             data_sendt += len(data)
             total_data_sent +=len(data)
             current_time = time.time()
             elapsed_time = current_time - intervall_time
             if args.intervall and elapsed_time >= args.intervall:
                 bandwidth = (total_data_sent/ args.intervall) / 1000000
                 result= [[f"{args.server_ip}:{args.port}",f"{intervall_time:.1f} - {current_time:.1f}",f" {data_sendt}",f"{ bandwidth:.2f}Mbps"]]                    
                 headers = ['ID', 'Interval','Transfer','Bandwith']
                 print(tabulate(result, headers=headers))
                 intervall_time= current_time
                 total_data_sent = 0
             if elapsed_time >= args.time:
                 break
                 
        end_time = time.time()
        duration = end_time-start_time
        if(args.format =="B"):
            total_data = data_sendt
        elif (args.format == "KB"):
            total_data = data_sendt/1000
        elif (args.format == "MB"):
            total_data = data_sendt/1000000.0
        sock.send('BYE'.encode())
        melding =  sock.recv(1024).decode() 
        if melding == "ACK:BYE":
            exit()
        bandwith = (data_sendt*8)/duration

        data = [[f"{args.server_ip}:{args.port}",f"0.0-{duration:.1f}",f" {total_data}",f"{bandwith:.2f}"]]
        headers = ['ID', 'Interval','Transfer','Bandwith']
        print(tabulate(data, headers=headers))
        sock.close()