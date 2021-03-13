# Wi-Fi password detection
<details><summary>Linux</summary>
There is an <b><i>nmconnection</i></b> in the folder <b><i>/etc/NetworkManager/system-connections/</i></b> for each Wi-Fi network registered on the machine:
<pre lang="bash"><code>
ls /etc/NetworkManager/system-connections/*.nmconnection</code></pre>
To read the key of a Wi-Fi network, you need to read the content of the related <b><i>nmconnection</i></b> file:
<pre lang="bash"><code>
sudo cat /etc/NetworkManager/system-connections/<WiFi_Network_Name>.nmconnection</code></pre>
The key can be read in clear in the <i>[wi-fi security]</i> as the value of the <i>psk</i> entry.<br><br>
You can also obtain the list of the passwords of all the registered Wi-Fi networks easily using the following command:
<pre lang="bash"><code>sudo grep psk= /etc/NetworkManager/system-connections/*.nmconnection</code></pre>
</details>
<details><summary>Windows</summary>
Executing the following command, there is an entry of the table for each registered Wi-Fi network on the machine:
<pre lang="bash"><code>netsh wlan show profiles</code></pre>
To read the key of a Wi-Fi network, you need to type the following command:
<pre lang="bash"><code>
netsh wlan show profile <WiFi_Network_Name> key=clear</code></pre>
The key can be read in clear in the <i>Security settings</i> as the value of the <i>Key Content</i> entry.
</details>
