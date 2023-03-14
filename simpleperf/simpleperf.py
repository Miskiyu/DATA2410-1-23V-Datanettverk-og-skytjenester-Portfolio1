"""
When you run in server mode, simpleperf will receive TCP packets and track
how much data was received during from the connected clients; it will calculate
and display the bandwidth based on how much data was received and how much
time elapsed during the connection. A server should read data in chunks of 1000
bytes. For the sake of simplcity, assume 1 KB = 1000 Bytes, and 1 MB = 1000
KB.
"""

import sys
import argparse
import socket
import time
"""SEERVER MODE"""



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
    


"""Optional arguments"""
"""må lage en parser"""
parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")

"""Må deretter lage fire argumenter  for server """

#lager server 
parser.add_argument('-s','--server', action='store_true')

#Port
parser.add_argument('-p','--port', type=check_port)

#IP adressec

parser.add_argument('-b','--bind', type=str)

#Lager format
parser.add_argument('-f','--format',type=str, default='MB')


"""Client"""

parser2= argparse.ArgumentParser(description="positional arguments", epilog="End of help")

#client
parser.add_argument('-c','--client', action='store_true')

#ip
parser.add_argument('-I', '--serverip',type=str)

#port
parser.add_argument('-p','--port',type=int)

#time
parser.add_argument('-t','--time', type=int)

#format
parser.add_argument('-f','--format',type=str)

#interval
parser.add_argument('-i','--interval', type=int)

#paralell
parser.add_argument('-P','--parallel',type=int)

#parser args
args = parser.parse_args()

"""Print """
print('your port number is:',args.port)
print('your ip adresse er:', args.bind)

if args.server:
    print("A simpleperf server is listening on port",args.port)

"""for å koble serevr"""
host = args.bind
port = args.port

def server(host,port):
    #lager en TCP/IP socket og velger type adresse og strem 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.bind((host,port))
    sock.listen()
    print(f"Hører på on {host}:{port}")

    while True:
        connection, addr =sock.accept()
        print(f"Hører på on {addr}")
        totalBytes = 0
        startTid = time.time()

        while True:
            data = connection.recv(1000)
            if not data:
                break
            totalBytes += len(data)
        slutt_tid = time.time()
        bruktTid = slutt_tid - startTid
        bandwidth = totalBytes / bruktTid / 1000000  # Calculate bandwidth in MB/s
        print(f"Received {totalBytes} bytes in {bruktTid:.2f} seconds, bandwidth: {bandwidth:.2f} MB/s")
       
        connection.close()




if __name__ =="__main__":
    server(args.bind,args.port)


##client 


if args.client:
    print(f"Simpleperf cliens is connecting to {args.bind} port {args.port}")

