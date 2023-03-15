import socket
import time
import argparse

parser = argparse.ArgumentParser(description='Simpleperf tool for measuring network throughput in server mode')
parser.add_argument('-s', '--server', action='store_true', help='enable the server mode')
parser.add_argument('-b', '--bind', type=str, default='127.0.0.1', help='IP address of the server interface')
parser.add_argument('-p', '--port', type=int, default=8088, help='port number on which the server should listen')
parser.add_argument('-f', '--format', type=str, default='MB', choices=['B', 'KB', 'MB'], help='choose the format of the summary of results')
parser.add_argument("-I", "--serverip", type=str, help="server IP address for client mode")
parser.add_argument("-t", "--time", type=int, default=50, help="time to run in seconds (default: 50)")
parser.add_argument("-f", "--format", type=str, default="MB", choices=["B", "KB", "MB"], help="format to display results in (default: MB)")
parser.add_argument("-i", "--interval", type=int, default=10, help="interval to print statistics in seconds (default: 10)")
parser.add_argument("-P", "--parallel", type=int, default=1, choices=range(1, 6), help="number of parallel connections (default: 1, max: 5)")
parser.add_argument("-n", "--num", type=str, help="number of bytes to send in client mode (e.g. 1MB)")
args = parser.parse_args()

if args.server:
    BUFFER_SIZE = 1000
    total_bytes = 0
    start_time = None
    end_time = None

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = args.bind
    port = args.port

    # bind the socket to a public host, and a well-known port
    s.bind((host, port))

    # become a server socket
    s.listen(1)

    print(f"A simpleperf server is listening on port {args.port}")

    while True:
        # establish connection with client
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        start_time = time.time()

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data: break
            total_bytes += len(data)

        end_time = time.time()
        conn.close()

        duration = end_time - start_time
        throughput = total_bytes / duration
        if args.format == 'B':
            print(f"{total_bytes} Bytes received in {duration:.2f} seconds, {throughput:.2f} Bytes/s")
        elif args.format == 'KB':
            print(f"{total_bytes/1000} KB received in {duration:.2f} seconds, {throughput/1000:.2f} KB/s")
        else:
            print(f"{total_bytes/1000000} MB received in {duration:.2f} seconds, {throughput/1000000:.2f} MB/s")

if args.client:
    def send_melding(host, port, tid_valgt ):
        print("A simpleperf client connection to server {args.bind}, port {args.port}")

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