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
