# Enumeration with nmap
Nmap (Network Mapper) is a free and open-source network scanner created by Gordon Lyon. Nmap is used to discover hosts and services on a computer network by sending packets and analyzing the responses.<br>
To select a target, you can type one of the following commands:

| Command | Description |
| --- | --- |
| nmap 192.168.1.1 | Scan a single IP address |
| nmap www.example.com | Scan a host |
| nmap 192.168.1.1-20 | Scan a range of IP addresses |
| nmap 192.168.1.0/24 | Scan a sub-network |
| nmap -iL file.txt | Scan targets specified in a file |

You can also add other options, that are described in the following sections sections.

<details><summary>Port selection</summary>
<table>
  <tr>
    <td>-p 22</td>
    <td>Scan a single port</td>
  </tr>
  <tr>
    <td>-p 1-100</td>
    <td>Scan a range of ports</td>
  </tr>
  <tr>
    <td>-F</td>
    <td>Scan 100 most common ports (FAST)</td>
  </tr>
  <tr>
    <td>-p-</td>
    <td>Scan all 65535 ports.</td>
  </tr>
</table>
</details>

<details><summary>Port scan types</summary>
<table>
  <tr>
    <td>-sT</td>
    <td>Scan using TCP CONNECT</td>
  </tr>
  <tr>
    <td>-sS</td>
    <td>Scan using TCP SYN SCAN (by default)</td>
  </tr>
  <tr>
    <td>-sU -p 123,161,162</td>
    <td>Scan UDP ports</td>
  </tr>
  <tr>
    <td>-Pn</td>
    <td>Scan selected ports ignoring discovery</td>
  </tr>
</table>
</details>

<details><summary>Service and OS detection</summary>
<table>
  <tr>
    <td>-A</td>
    <td>Detect OS and services</td>
  </tr>
  <tr>
    <td>-sV</td>
    <td>Standard Service detection</td>
  </tr>
  <tr>
    <td>-sV --version-intensity 5</td>
    <td>More aggressive Service Detection</td>
  </tr>
  <tr>
    <td>-sV --version-intensity 0</td>
    <td>Lighter banner grabbing Detection</td>
  </tr>
</table>
</details>

<details><summary>Output formats</summary>
<table>
  <tr>
    <td>-oN file.txt</td>
    <td>Save <i>stdout</i> of the command to <i>file.txt</i>.</td>
  </tr>
  <tr>
    <td>-oX file.xml</td>
    <td>Save results as XML.</td>
  </tr>
  <tr>
    <td>-oG file.txt</td>
    <td>Save results with format useful for <i>grep</i>.</td>
  </tr>
  <tr>
    <td>-oA file</td>
    <td>Save results in all the formats.</td>
  </tr>  
</table>
</details>

<details><summary>NSE scripts</summary>
<table>
  <tr>
    <td>-sC</td>
    <td>Scan using DEFAULT SAFE scripts.</td>
  </tr>
  <tr>
    <td>--script-help=name-script</td>
    <td>Get help for a script.</td>
  </tr> 
  <tr>
    <td>--script=name-script.nse</td>
    <td>Scan using a specified NSE script.</td>
  </tr>
  <tr>
    <td>--script=smb*</td>
    <td>Scan using a set of scripts by using regular expressions. (e.g. scripts with name=smb..)</td>
  </tr>
</table>
To know which are the all the available NSE scripts, you can type the following command:
locate nse | grep script
</details>

<details><summary>Scan to search for DDoS reflection UDP services</summary>
To make a scan for UDP DDoS reflectors (reflection attacks), you can type the following commands for example:
<pre lang="bash"><code>nmap -sU -A -PN -n -pU:19,53,123,161 -script:ì=ntp-monlist, dns=recursion, snmp-sysdescr 192.168.1.0/24</code></pre>
</details>

<details><summary>HTTP Service Information</summary>
<table>
  <tr>
    <td>--script=http-title</td>
    <td>Gather page titles from HTTP services.</td>
  </tr>
  <tr>
    <td>--script=http-headers</td>
    <td>Gather page headers of web services.</td>
  </tr>
  <tr>
    <td>--script=http-enum</td>
    <td>Gather web applications from known paths.</td>
  </tr>
</table>
</details>

<details><summary>Detect Heartbleed SSL Vulnerability</summary>
For heartbleed testing, you can use the following nmap option:
<pre lang="bash"><code>--script=ssl-heartbleed</code></pre>
</details>

<details><summary>IP address Information</summary>
To find information about an IP address, you can use the following command:
<pre lang="bash"><code>--script=ssl-asn-query, whois, ip-geolocation-maxind</code></pre>
</details>
