import argparse
import socket
import time
import sys

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
    

def run_server(host,port):
    print('A SIMPLEPERF SERVER IS LISTENING ON PORT',port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
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
                duration = time.monotonic() - start_time
                if(args.format == "B"):
                    total_bytes = f"{bytes_received} B"
                elif (args.format == "KB"):
                    total_bytes = f"{bytes_received/1000} KB "
                elif (args.format == "MB"):
                    total_bytes = f"{bytes_received/1000000.0} MB"
                elapsed_time = duration- start_time
                print(f"Received {bytes_received} bytes in {elapsed_time:.2f} seconds  KB/s)")
            #  if data!= 0:
             #        transfer_rate = (bytes_received*8)/(duration*1000000)
              #  else:
               #      transfer_rate = 0.0  
                #rate = round(transfer_rate,2)
                #Denne koden lager en string "interval" som inneholder en tidsperiode fra 0.0 til varigheten av dataoverføringen (i sekunder). "round(duration, 1)" runder av "duration" variabelen til en desimal.
                interval = f"0.0 - {round(duration, 1)}"

                #result = f"Result: ID={addr[0]}:{addr[1]} Interval={duration:.2f} Transfer={total_bytes_received/(1024*1024):.0f} Rate={transfer_rate:.2f} Mbps"
                #result = f"Result: ID={addr[0]}:{addr[1]} Interval:{duration:.2f} recived {total_bytes} Rate {rate} "
                output_format = "{:<10} {:<15} {:<10} "
                output = output_format.format("ID", "Interval", "Received") 
                output += "\n{:<10} {:<15} {:<10}  Mbps".format(  
                  f"{addr[0]}:{addr[1]}",  f"{elapsed_time}", 
                  f"{total_bytes}")
                print(output)
                break

                
def run_client(host, port, duration,interval):
    print(f"A simpleperf client with {host}:{port} is connected with ")
    start_time = time.monotonic()
    bytes_sent = 0
    timeStart = time.time()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
             s.connect((host, port))

             for i in range(0, duration,interval): 
                interval_bytes_received = 0
                while time.monotonic() - timeStart < interval:
                    data = b"x" * 1000
                    s.sendall(data)
                    endtime = "%.2f" % ( start_time + (time.time()- timeStart))
                    start_time = "%.2f" % start_time
                    start_time= float(start_time) + (time.time()-timeStart)
                    timeStart = time.time()
                    if not data:
                        break
                    bytes_sent += len(data)
                    interval_bytes_received +=len(data)
                    if(args.format == "B"):
                         total_bytes = f"{interval_bytes_received} B"
                    elif (args.format == "KB"):
                      total_bytes = f"{interval_bytes_received/1000} KB "
                    elif (args.format == "MB"):                        
                       total_bytes = f"{interval_bytes_received/1000000.0} MB"
                
                    interval_str = f"{i:.1f} - {i+interval:.1f}"
                #f"{('%.2f' % start_time)} - {endtime}"
                    output_format = "{:<10} {:<15} {:<10} Mbps"
                    output = output_format.format("ID", "Interval", "Received") 
                    output += "\n{:<10} {:<15} {:<10}".format(
                    f"{host}:{port}", interval_str, f"{total_bytes}")
                    print(output)
                    break
             if(args.format == "B"): 
                 total_bytes = f"{bytes_sent} B"
             elif (args.format == "KB"):
                 total_bytes = f"{bytes_sent/1000} KB "
             elif (args.format == "MB"):
                total_bytes = f"{bytes_sent/1000000.0} MB"
             end_time = time.monotonic()
             elapsed_time = end_time - start_time
                #Denne koden lager en string "interval" som inneholder en tidsperiode fra 0.0 til varigheten av dataoverføringen (i sekunder). "round(duration, 1)" runder av "duration" variabelen til en desimal.
             interval = f"0.0 - {duration}"

             #result = f"Result: ID={addr[0]}:{addr[1]} Interval={duration:.2f} Transfer={total_bytes_received/(1024*1024):.0f} Rate={transfer_rate:.2f} Mbps"
             #result = f"Result: ID={addr[0]}:{addr[1]} Interval:{duration:.2f} recived {total_bytes} Rate {rate} "
             output_format = "{:<10} {:<15} {:<10} "
             output = output_format.format("ID", "Interval", "Received") 
             output += "\n{:<10} {:<15} {:<10} Mbps".format(  
                  f"{host}:{port}",  f"{interval}", 
                f"{total_bytes}" )
             print(output)
        except:
            print("Error: failed to connect to server")

    
    
parser = argparse.ArgumentParser(description="A simple implementation of iperf")
parser.add_argument('-s','--server', action='store_true')
parser.add_argument('-p','--port', type=check_port)
parser.add_argument('-b', '--bind', default='localhost', type=str, help='The IP address to bind to (default: localhost)')
parser.add_argument('-f', '--format', type=str, default="MB", choices=["B", "KB", "MB"], help='Format of the summary of results')
parser.add_argument('-c','--client', action='store_true')
parser.add_argument("-I", "--server_ip", type=str, help="server IP address for client mode")
parser.add_argument("-t", "--time", type=int, help="Duration in seconds")
parser.add_argument('-i', "--interval", type=int,help='Interval for statistics output in seconds')

args = parser.parse_args()

def main():
    
    if args.server:
        run_server(args.bind,args.port)
    elif args.client:
        run_client(args.server_ip, args.port, args.time,args.interval)
    else:
	    print("Error: you must run either in server or client mode")

if __name__ == "__main__":
    main()
