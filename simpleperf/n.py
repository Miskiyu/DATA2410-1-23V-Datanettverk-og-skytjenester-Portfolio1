import argparse
import socket
import sys
import time

def run_server():
    parser = argparse.ArgumentParser(description='Simple TCP Bandwidth Test Server')
    parser.add_argument('-p', '--port', type=int, default=5001,
                        help='TCP port number (default 5001)')
    args = parser.parse_args()

    print('Server listening on TCP port', args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', args.port))
        s.listen(1)
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, args.window)
            while True:
                data = conn.recv(1024)
                if not data:
                    break

def run_client():
    parser = argparse.ArgumentParser(description='Simple TCP Bandwidth Test Client')
    parser.add_argument('host', help='Server hostname or IP address')
    parser.add_argument('-p', '--port', type=int, default=5001,
                        help='TCP port number (default 5001)')
    parser.add_argument('-f', '--format', choices=['b', 'B', 'k', 'K', 'm', 'M', 'g', 'G'], default='M',
                        help='Output format (bits or bytes, default M)')
    args = parser.parse_args()

    print('Client connecting to', args.host, 'TCP port', args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.host, args.port))
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, args.window)
        start_time = time.monotonic()
        data_size = 0
        while True:
            s.sendall(b'\0' * 1024)
            data_size += 1024
            elapsed_time = time.monotonic() - start_time
            if elapsed_time >= 10:
                break

    bandwidth = data_size * 8 / elapsed_time
    if args.format in ['b', 'k', 'm', 'g']:
        bandwidth /= 1024
    if args.format in ['b', 'k', 'm']:
        bandwidth /= 1000
    if args.format == 'b':
        unit = 'bits/sec'
    elif args.format == 'B':
        unit = 'Bytes/sec'
    elif args.format == 'k':
        unit = 'Kbits/sec'
    elif args.format == 'K':
        unit = 'KBytes/sec'
    elif args.format == 'm':
        unit = 'Mbits/sec'
    elif args.format == 'M':
        unit = 'MBytes/sec'
    elif args.format == 'g':
        unit = 'Gbits/sec'
    else:
        unit = 'GBytes/sec'
    print('%.2f %s' % (bandwidth, unit))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-s':
        run_server()
    else:
        run_client()

import argparse
import socket
import time

def run_server(port):
    print(f"Starting server on port {port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr[0]}:{addr[1]}")
                start_time = time.monotonic()
                bytes_received = 0
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    bytes_received += len(data)
                end_time = time.monotonic()
                elapsed_time = end_time - start_time
                speed = bytes_received / elapsed_time
                print(f"Received {bytes_received} bytes in {elapsed_time:.2f} seconds ({speed/1000:.2f} KB/s)")
                
def run_client(host, port, duration):
    print(f"Connecting to {host}:{port}")
    start_time = time.monotonic()
    bytes_sent = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while time.monotonic() - start_time < duration:
            data = b"x" * 1024
            s.sendall(data)
            bytes_sent += len(data)
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    speed = bytes_sent / elapsed_time
    print(f"Sent {bytes_sent} bytes in {elapsed_time:.2f} seconds ({speed/1000:.2f} KB/s)")
    
def main():
    parser = argparse.ArgumentParser(description="A simple implementation of iperf")
    subparsers = parser.add_subparsers(dest="mode", required=True, help="Mode of operation")

    server_parser = subparsers.add_parser("server", help="Run as server")
    server_parser.add_argument("port", type=int, help="Port number to listen on")

    client_parser = subparsers.add_parser("client", help="Run as client")
    client_parser.add_argument("host", type=str, help="Host name to connect to")
    client_parser.add_argument("port", type=int, help="Port number to connect to")
    client_parser.add_argument("duration", type=int, help="Duration of test in seconds")
    
    args = parser.parse_args()

    if args.mode == "server":
        run_server(args.port)
    elif args.mode == "client":
        run_client(args.host, args.port, args.duration)

if __name__ == "__main__":
    main()
