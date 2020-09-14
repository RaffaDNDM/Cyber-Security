# DNS Spoofing
This program is going to analyse DNS packets, that work over UDP protocol. The packet is a DNS response if it has at least one <i>DNSRR (DNS Record Route)</i> in which there is one of the IP addresses of requested domain. If a packet is a DNS response, the program looks at the domain specified in the relative <i>DNSQR (DNS Question Record)</i> and if it's the same specified as <i>target domain</i>, it changes the IP address in the first DNSRR with a specified IP address. The program is going to change the number of DNSRRs, specified in DNS packet, to guarantee that the victim will receive only one possible resolution. The goal of the program is to change the sending of packets for the target machine.<br> 
To use this Spoofer, you need to install the following modules for python3, through this command:
<pre lang="bash"><code>apt install build-essential libnetfilter-queue-dev</code></pre>
<pre lang="bash"><code>pip3 install termcolor argparse</code></pre>
To run the program, you need to type for example this command on bash:
<pre lang="bash"><code>python3 dns_spoofing.py -i eth0 -d www.google.com</code></pre>
With this command the packets that the victim would have sent to <i>www.google.com</i> will be sent to the machine in the middle, with IP address relative to network interface <i>eth0</i>.<br>
Another possible example, that is more useful, is the following one:
<pre lang="bash"><code>python3 dns_spoofing.py -t 104.16.91.52 -d www.google.com</code></pre>
With this command all the packets, that victim would have sent to <i>www.google.com</i>, will be sent to IP address <i>104.16.91.52</i> (www.udemy.com).<br> 
The goal of this program is that we can use these program to redirect the traffic of the victim to a fake website and the victim doesn't know it. This happens because the victim, connecting to a remote domain, is asking through a <b>Domain Resoluton Request</b> to obtain an IP address and if the website is uploaded, he thinks that all went in the right way. In reality, through this program, the packets are directed to another website because of modification of only one <b>DNS response</b>.
The program will display <code><pre>"Spoofing target"</pre></code> on command line, during its execution, if DNS spoofing is applied modyfing a DNS packet. 
To check which parameters you can insert, you can type the command:
<pre lang="bash"><code>python3 dns_spoofing.py --help </code></pre>
The program must run with superuser privileges.
