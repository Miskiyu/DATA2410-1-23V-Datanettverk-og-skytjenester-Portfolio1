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
import re
DISCONNECT = "bye"
message_length = '0'*1000  #hvordan man lager 1000 bytes


"""SEERVER MODE"""



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
    ip = re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",val)
    if(ip):
        return True
    else:
        print("this is not valid ip-adress")
        sys.exit()    

def server(host,port):
    #lager en TCP/IP socket og velger type adresse og strem 
    sock.bind((host,port))
    sock.listen()
    print(f"Hører på on {host}:{port}")
    bytes_recived = b""

    while True:
        connection, addr =sock.accept()
        print(f"Hører på on {addr}")
        while True:
            data = connection.recv(1000)
            if not data:
                break
            bytes_recived+=data
        response = "Thanks for the data!"
        connection.sendall(response)
        connection.close()

parser = argparse.ArgumentParser(description="positional arguments", epilog="End of help")


#lager server 
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b','--bind', type=check_ip)
parser.add_argument('-c','--client', action='store_true')
args = parser.parse_args()


def handle_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host,port))
    message = input("Enter a message to send to the server: ")

# Send the message to the server in chunks of 1000 bytes
    message_bytes = message.encode('utf-8')
    for i in range(0, len(message_bytes), 1000):
        chunk = message_bytes[i:i+1000]
        client_socket.sendall(chunk)

    print("Message sent to server.")

# Receive a response from the server
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Received response: {response}")

# Close the connection with the server
    client_socket.close()




if __name__ =="__main__":
    if args.server:
        print("A simpleperf server is listening on port",args.port)
        host = args.bind
        port = args.port
        server(host,port)
    elif(args.client):
        host = args.bind
        port = args.port
        handle_client(host, port)


"client"
"""
def thread1(sock):  ##hører på 
    while True:
        message = sock.recv(1024).decode 
        print('\nFrom sever:',message)
        if (message == "bye"):
            break

def threda2():
    while True:
        melding = input("input")
        if melding == DISCONNECT:
            melding_ut= melding.encode()
            sock.send(melding_ut)
            break
        else:
            melding_ut = melding.encode()
            sock.send(melding_ut)

x = '0'*1000  #hvordan man lager 1000 bytes
print(x)
"""





