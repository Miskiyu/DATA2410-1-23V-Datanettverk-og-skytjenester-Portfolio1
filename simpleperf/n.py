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
