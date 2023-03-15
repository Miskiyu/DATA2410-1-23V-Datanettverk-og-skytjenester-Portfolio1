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
    
    parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")



#lager server 
    parser.add_argument('-s','--server', action='store_true')

#Port
    parser.add_argument('-p','--port', type=check_port)

#IP adresse

    parser.add_argument('-b','--bind', type=str, default='heo')

#Lager format
    parser.add_argument('-f','--format',type=str, default='MB')


#parser args
    args = parser.parse_args()

    
    if args.server:
        print("A simpleperf server is listening on port",args.port)
        host = args.bind
        port = args.port
        server(host,port)

"client"

def send_melding(host, port, tid_valgt ):
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

parser = argparse.ArgumentParser(description='Simpleperf client')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument('-I','--server_ip',  help='IP address of server')
parser.add_argument('-p','--server_port', type=int, help='Port number of server')
parser.add_argument('-t','--time_duration', type=int, help='Duration of data generation in seconds')
args = parser.parse_args()


if args.client:
        print("A simpleperf client connection to server {args.server_ip}, port {args.server_port}")
        send_melding(args.server_ip, args.server_port, args.time_duration)




