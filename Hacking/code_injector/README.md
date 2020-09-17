# Code Interceptor
This program is going to detect the IP packets interecepted by program. Looking at all the HTTP requests, the program removes HTTP <code>Accept-Encoding</code> header so the response HTML load will not be encrypted. The program inserts the javascript code, taken from a file, in the HTML load of the HTTP response as a script. The addition of the lines of code are performed by replacing <code></body></code> with <code><script>CODE</script></body></code> statement. Then the program modifies the <code>Content-Length</code> value w.r.t. performed HTML changes.
To use this Interceptor, you need to install the following modules for python3, through this command:
<pre lang="bash"><code>apt install build-essential python3 libnetfilter-queue-dev</code></pre>
<pre lang="bash"><code>pip3 install termcolor argparse</code></pre>
To run the program, you need to type for example this command on bash:
<pre lang="bash"><code>python3 code_interceptor.py -local -f code.js</code></pre>
This command will perform the javascript command in <i>code.js</i>, that in the following case, displays a dialogue window with message <i>Message</i>:<br>
<img src="output.png" width="500" alt="output"><br>
To check which parameters you can insert, you can type the command:
<pre lang="bash"><code>python3 code_interceptor.py --help </code></pre>
The program must run with superuser privileges and can work on HTTP web pages. Starting from this program, you can modify or add HTML tags, by changing <code></body></code> with another tag.

### Bypassing HTTPS
After establishing a MITM connection (e.g. using ARP spoofing), we need to use the SSLstrip that permit us to leave HTTP requests of victim, without force it to use HTTPS protocol. All the request and responses, made by victim, belong to HTTP type. Then the MITM machine forwards HTTP packets to <b><i>SSLstrip</i></b>, sending and receiving then HTTPS requests and responses to/from the server. <br>
In this way, the server thinks that is talking with client through a secure connection but the victim is actually talking through an HTTP connection. To perform this behaviour the MITM machine must run in order the following commands:
<pre lang="bash"><code>sslstrip</code></pre>
<pre lang="bash"><code>iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000</code></pre>
The last command is very important because it's going to redirect all HTTP packets to port of SSLstrip program, through a rule applied before any operation would be performed.
If you are the MITM on HTTPS protocol, the program on HTTPS executes these commands, because of empty FORWARD chain:
<pre lang="bash"><code>iptables -I OUTPUT -j NFQUEUE --queue-num 0 </code></pre>
<pre lang="bash"><code>iptables -I INPUT -j NFQUEUE --queue-num 0 </code></pre>
and analyses packets on SSLstrip port (<i>10000</i>) and not on HTTP port (<i>80</i>).
