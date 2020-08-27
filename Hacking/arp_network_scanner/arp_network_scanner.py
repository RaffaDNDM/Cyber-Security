'''
08-27-2020
Because of how pylint works, you cannot type directly
import scapy.all as scapy
you need to import each module separately
'''
from scapy.layers.l2 import arping, ARP, Ether, srp
from scapy.layers.inet import IP, UDP, TCP, ICMP
from termcolor import cprint

BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'

def network_scan(network):
    #Create ARP request
    arp_head = ARP(pdst=network)
    ether_head = Ether(dst=BROADCAST_MAC)
    request = ether_head/arp_head
    
    #Send request and wait for response
    responses_list = srp(request, timeout=1)[0]

    cprint(' ______________________________________', 'red')
    cprint("|", 'red', end='')
    cprint(" {:^15} ".format('IP address'), 'blue', 'on_green', end='')
    cprint("|", 'red', end='')
    cprint(" {:^18} ".format('MAC address'), 'blue', 'on_yellow', end='')
    cprint("|", 'red')

    for response in responses_list:
        #response[0]= packet sent
        #response[1]= response
        #print(response.show()) to see all fields of the response packet
        cprint("|", 'red', end='')
        cprint(" {:^15} ".format(response[1].psrc), 'green', end='')
        cprint("|", 'red',end='')
        cprint(" {:^18} ".format(response[1].hwsrc), 'yellow', end='')
        cprint("|", 'red')
    
    cprint(' ______________________________________', 'red', end='\n\n')

def main():
    #Simplest way to implement ARP network scanner 
    #arping("192.168.1.1/24")
    #Implementation of ARP network scanner from zero
    network_scan("192.168.1.1/24")

if __name__=="__main__":
    main()
