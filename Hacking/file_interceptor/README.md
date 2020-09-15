# File Interceptor
This program is going to detect the IP packets interecepted by program. Looking at all the HTTP requests, the program analyses them by looking for requests of a specified type of file. If an HTTP request contains desired file specification, the program save the ACK of this TCP packet and looks for a TCP packet with SEQ number equal to that value and, if found, it creates a new HTTP response thats specifies the redirection to a desired URL.   
To use this Sniffer, you need to install the following modules for python3, through this command:
<pre lang="bash"><code>apt install build-essential python3 libnetfilter-queue-dev</code></pre>
<pre lang="bash"><code>pip3 install termcolor argparse</code></pre>
To run the program, you need to type for example this command on bash:
<pre lang="bash"><code>python3 file_interceptor.py -t pdf -local -url https://www.youtube.com</code></pre>
This command will display only the TCP packets intercepted, highligthing packets that contains an HTTP <b>GET</b> request of a file with extension <i>.pdf</i> and creating an HTTP response with redirection to <i>www.youtube.com</i>. An example of output of the command is shown in the following image:<br>
<img src="output.png" width="500" alt="output"><br>
To check which parameters you can insert, you can type the command:
<pre lang="bash"><code>python3 file_interceptor.py --help </code></pre>
Remember to clean the cache, if you apply changes to program or URL and want to test them. For example, if you redirect the requests of <b>pdf</b> files to <i>www.google.com</i> and then you want to redirect the same requests to <i>www.youtube.com</i>, the traffic will be redirect also to <i>www.google.com</i>.
The program must run with superuser privileges and can work only on HTTP web pages.
