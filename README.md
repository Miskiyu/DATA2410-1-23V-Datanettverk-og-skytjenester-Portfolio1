<h1>Simpleperf </h1> 
<p> Simpleperf is a simple program to test network performance between server and client. It can be used to mesaure the maximum bandwidht and how much data transferd between to host and  test the quality of network link. You can run simpleprf in to modes client mode and server mode.</p>


<h2>Dependencies</h2>

<p>Simpleperf uses the Tabulate library as a dependency. To use it, you need to have pip installed.</p>
<p>To install Tabulate, run the following command:</p>
   - sudo apt-get install pip
   - python -m pip install -U tabulate  


<h2> How to use Simpleperf</h2>
<p> Simpleperf can be run in either server mode or client mode. Each mode has different flags that can be used. </p>

<h3>Server mode</h3>
<p>if you want to mesaure the network perfrmance of server start Simpleperf in server mode by running:</p>
    - python simplpeperf.py  -s 

If you don't specify an IP address and port number, Simpleperf will use default values.

<h4>The server has three other options:</h4>

 - f (format): specifies the format for the output (B for bytes, KB for kilobytes, or MB for megabytes)
 - p (port): specifies the port number to use
 - b (IP): specifies the IP address to bind to

<h3>Client mode</h3>
<p>if you want to mesaure the network performance between client adn server, start Simpleperf in client mode by running:</p>
    - python simpleperf.py -c

<h4>The client has five options:</h4>

- f (format): specifies the format for the output (B for bytes, KB for kilobytes, or MB for megabytes)
- i (interval): specifies the time interval (in seconds) between data transmissions
- t (time): specifies the total time (in seconds) to run the test
- n (num): specifies the number of data transmissions to perform
- p (parallel): specifies the number of parallel connections to use









