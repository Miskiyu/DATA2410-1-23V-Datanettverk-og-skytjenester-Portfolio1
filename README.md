# Simpleperf 

Simpleperf is a simple program to test network performance between server and client. It can be used to mesaure the maximum bandwidht and how much data transferd between to host and  test the quality of network link. You can run simpleprf in to modes client mode and server mode.


# Dependencies 

- this program uses Tabulate as depenedency, you have to first download pip to use pip. 
    - sudo apt-get install pip
    - python -m pip install -U tabulate  


# How to use Simpleperf
simpleperf runs in server mode and client mode. Each mode has different flags you can invoke. 

# Server mode:
- if you want to mesaure the network perfrmance of server start Simpleperf in server mode by running:
    - python simplpeperf.py  -s 

port and ip has default if you dont want to write ip and port

-  server has three other options:
    - -f (format)
    - -p (port)
    - -b (ip)

# Client 
- if you want to mesaure the network performance between client adn server, start Simpleperf in client mode by running:
    - python simpleperf.py -c
    
    client have 5 options
    - -f (format)
    - -i (intervall)
    - -t (time)
    - -n (num)
    - -p (parallel )










