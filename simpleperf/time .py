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