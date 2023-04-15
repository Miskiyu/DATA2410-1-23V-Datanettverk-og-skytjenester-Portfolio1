
Simpleperf 
================================================================

Simpleperf is a simple program to test network performance between server and client. It can be used to mesaure the maximum bandwidht and how much data transferd between two host and  test the quality of network. You can run simpleprf in to modes client mode and server mode



Dependencies
--------------
Simpleperf uses the Tabulate library as a dependency. To use it, you need to have pip and then install tabulate.

To install pip run this command in terminal:

    sudo apt-get install pip

To install tabulate:

    python -m pip install -U tabulate 

How to use Simpleperf
---------------------
Simpleperf can be run in either server mode or client mode. Each mode has different flags that can be used. If you don't specify any flags, Simpleperf will use default values.


### Server mode: ###
If you want to mesaure the network perfrmance of server start Simpleperf in server mode by running:
    
    python simplpeperf.py  -s 


The server has three other command-line options:

    -f, --format           specifies the format for the output (B, KB or MB)
    -b, --bind             specifies the IP address to bind to
    -p, --port             specifies the port number to use

### Client mode: ###
if you want to mesaure the network performance between client and server, start Simpleperf in client mode by running:

    - python simpleperf.py -c
    
    
The client has five other command-line options:

    -f, --format           specifies the format for the output (B, KB or MB)
    -I, --serverip         specifies the ip address of the server
    -p, --port             specifies the port number to use
    -i, --interval         specifies the time interval (in seconds) between data transmissions
    -t, --time             specifies the total time (in seconds) to run the test
    -n, --num              specifies the number of bytes to transfer
    -p,--parallel          specifies the number of parallel connections to use
    








