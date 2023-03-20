import argparse
import socket
import time
import sys
import ipaddress
import threading


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
    
def check_ip(address):
    try:
        val = ipaddress.ip_address(address)
        print(f'The IP adress {val} is valid.')
    except ValueError:
        print("The IP address is not valid ")
        sys.exit()

def run_server(host, port):
    print('A SIMPLEPERF SERVER IS LISTENING ON PORT',port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
           # thread = threading.Thread(target=run_client, args=(conn,addr))
            #thread.start()  
            with conn:
                print(f"Connection from {addr[0]}:{addr[1]}")
                start_time = time.monotonic()
                bytes_received = 0
                total_bytes = 0
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    bytes_received += len(data)
             
                    if data == b"BYE":
                        conn.sendall(b"ACK: BYE")
                        end_time = time.monotonic()
                        duration = end_time-start_time
                        if(args.format == "B"): 
                           total_bytes = f"{bytes_received} B"
                        elif (args.format == "KB"):
                            total_bytes = f"{bytes_received/1000} KB "
                        elif (args.format == "MB"):
                            total_bytes = f"{bytes_received/1000000.0} MB"
                        interval = f"0.0 - {round(duration, 1)}"
                        output_format = "{:<10} {:<15} {:<10} "
                        output = output_format.format("ID", "Interval", "Received") 
                        output += "\n{:<10} {:<15} {:<10}  Mbps".format(  
                                 f"{addr[0]}:{addr[1]}",  f"{interval}", 
                         f"{total_bytes}")
                        print(output)
                        conn.close()
                        break
                end_time = time.monotonic()
                elapsed_time = end_time - start_time
                if(args.format == "B"):
                    total_bytes = f"{bytes_received}"
                elif (args.format == "KB"):
                    total_bytes = f"{bytes_received/1000} "
                elif (args.format == "MB"):
                    total_bytes = f"{bytes_received/1000000.0}"   
                output_format = "{:<10} {:<15} {:<10} "
                output = output_format.format("ID", "Interval", "Received") 
                output += "\n{:<10} {:<15} {:<10}  Mbps".format(  
                             f"{addr[0]}:{addr[1]}",  f"{elapsed_time}", 
                         f"{total_bytes}")
                print(output)
                print(f"Total: {bytes_received/1000000:.2f} MB, {1000000:.2f} Mbps")

def handleparallel(host, port, duration, interval,parallel,num):
    for i in range()


                
def run_client(host, port, duration, interval,parallel,num):
    print(f"A simpleperf client with {host}:{port} is connected with ")
    client = []
    if parallel > 1:
        handleparallel(host, port, duration, interval,parallel,num)
        stop
    start_time = time.monotonic()
    bytes_sent = 0
    if duration is None and interval is None:
        # Run a simple data transfer without intervals
        bytes_sent = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            while True:
                data = b"0" * 1000
                s.sendall(data)
                bytes_sent += len(data)
                if bytes_sent  > 100000:
                    break
            s.sendall(b"BYE")
            response = s.recv(1000)
            print(response)
            if response != b"ACK: BYE":
                  print("Error: Did not receive acknowledgement from server")
            else:
              end_time = time.monotonic()
              elapsed_time = end_time - start_time
            print(f"Sent {bytes_sent} bytes")
    else:
        for i in range(int(duration/interval)):
            interval_start_time = time.monotonic()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                while time.monotonic() - interval_start_time < interval:
                    data = b"0" * 1000
                    s.sendall(data)
                    bytes_sent += len(data)
                interval_end_time = time.monotonic()
                elapsed_time = interval_end_time - interval_start_time
                if(args.format == "B"):
                     total_bytes = f"{bytes_sent}"
                elif (args.format == "KB"):
                     total_bytes = f"{bytes_sent/1000} "
                elif (args.format == "MB"):                        
                    total_bytes = f"{bytes_sent/1000000}"
            total_bytes = float(total_bytes)
            bandwith = (total_bytes/elapsed_time)/1000000
            output_format = "{:<10}       {:<15}      {:<10}    {:<10}"
            output = output_format.format("ID", "Interval", "Transfer ","Bandwith") 
            output += "\n{:<15}        {:<15}      {:<10}     {:<10}".format(
            f"{host}:{port}", f"{interval*i:.1f} - {interval*(i+1):.1f}", f"{total_bytes}", f"{bandwith}")
            print(output)  
            end_time = time.monotonic()
            elapsed_time = end_time - start_time
        speed = (bytes_sent / elapsed_time)
        output_format = "{:<10}      {:<15}   {:<10}  {:<10}"
        output = output_format.format("ID", "Interval", "Transfer ","Bandwith") 
        output += "\n{:<15}          {:<15}  {:<10}   {:<10}".format(
        f"{host}:{port}", f"0 - {interval*(i+1):.1f}", f"{total_bytes}", f"{speed/1000000:.2f}")
        print("------------------------------------------------------------")

        print(output)  
        print(f"Total: {bytes_sent/1000000:.2f} MB, {speed/1000000:.2f} Mbps")



parser = argparse.ArgumentParser(description="A simple implementation of iperf")
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port , default=8088)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", default='localhost', type=str, help="server IP address for client mode")
parser.add_argument("-t", "--time", type=int, help="Duration in seconds")
parser.add_argument('-i', "--interval", type=int,help='Interval for statistics output in seconds')
parser.add_argument('-P', '--parallel', default=1, type=int, help='The number of parallel connections to establish with the server (default: 1)')

parser.add_argument('-n', '--num', type=str, default=1000 )
args = parser.parse_args()
def main():

  
    if args.server:
        run_server(args.bind, args.port)
    elif args.client:
        run_client(args.server_ip, args.port, args.time, args.interval, args.parallel, args.num)
    else:
        print("Error: you must run either in server or client mode")

if __name__ == "__main__":
    main()
