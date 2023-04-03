# Simpleperf 

Simpleperf is a simple program to test network performance between server and client. It can be used to mesaure the maximum bandwidht and how much data transferd between to host and  test the quality of network link. You can run simpleprf in to modues, client or server.

# How to use Simpleperf

Dependecies you need to download before using Simpleperf
- pip 
- tabulate, you can download with pip install tabulate

choose the mode of operation

-Server mode:
    - if you want to mesaure the network perfrmance of server start Simpleperf in server mode by running:
    python -s 
port and ip has default if you dont want to write ip and port

    -server has three other options:
        - -f (format)
        - -p (port)
        - -b (ip)

Client 
    - if you want to mesaure the network performance between client adn server, start Simpleperf in client mode by running:
        - simpleperf -c
    
    client have 5 options
    - 










