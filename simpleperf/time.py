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


def handleClient(connection, addr):
    print(f"A simpleperf client with {addr[0]}:{addr[1]} is connected with ")
    intervall =1
    total_bytes_received = 0
    timeStart = time.time()
    duration= 4  # Change this to the desired test duration
    for t in range(0, duration, intervall):
        while True:
            interval_bytes_received = 0
            if time.time() - timeStart > intervall:
                msg = connection.recv(1000).decode()   #Decoding received message
                endtime = "%.2f" % ( start_time + (time.time()- timeStart))
                start_time = "%.2f" % start_time
                print(f"{start_time} - {endtime}")
                start_time= float(start_time) + (time.time()-timeStart)
                timeStart = time.time()
                if not msg:
                    break
                total_bytes_received += len(msg)
                interval_bytes_received += len(msg)
                print(total_bytes_received)
                print ("received  message = ", msg)   #Printing the received message on the server side
                if msg == DISCONNECT:
                    message = "Are you sure you want to disconnect? (yes/no):"
                    connection.send(message.encode())
                    response = connection.recv(1000).decode().strip().lower()
                    if response == "yes":
                        message = DISCONNECT.encode()
                        connection.send(message)
                        if(args.format == "B"):
                            total_bytes = f"{interval_bytes_received} B"
                        elif (args.format == "KB"):
                            total_bytes = f"{interval_bytes_received/1000} KB "
                        elif (args.format == "MB"):
                            total_bytes = f"{interval_bytes_received/1000000.0} MB"
                        transfer_rate = (interval_bytes_received*8)/(intervall*1000000)
                        rate = round(transfer_rate, 2)
                        interval_str = f"{t:.1f} - {t+intervall:.1f}"
                        output_format = "{:<10} {:<15} {:<10} {:<10} Mbps"
                        output = output_format.format(
                            f"{addr[0]}:{addr[1]}", interval_str, f"{total_bytes}", f"{rate:.2f}")
                        connection.send(output.encode())
    connection.close()
