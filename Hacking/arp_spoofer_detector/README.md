# ARP Spoofer Detector
This program is used to understand if the machine is under ARP spoofer attack, by comparing MAC address received by ARP response packet, relative to a specific IP address, and the MAC address obtained by sending a new ARP request for the resolution of the same IP address of ARP response.
To use this ARP spoofer detector, you need to install the following modules for python3, through this command:
```bash
pip3 install scapy termcolor
```
To run the program, you need to type for example this command on bash:
```bash
python3 arp_spoofer_detector.py
```
To check which parameters you can insert, you can type the command:
```bash
python3 arp_spoofer.py --help 
```
The program must run with superuser privileges.
