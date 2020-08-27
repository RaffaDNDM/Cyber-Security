'''
08-27-2020
Because of how pylint works, you cannot type directly
import scapy.all as scapy
you need to import each module separately
'''
from scapy.layers.l2 import arping
from scapy.layers.inet import IP, UDP, TCP, ICMP

#Simplest way to implement ARP network scanner 
arping("192.168.1.1/24")

#Implementation of ARP network scanner from zero
