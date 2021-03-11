'''
Because of how pylint works, you cannot type directly
import scapy.all as scapy
you need to import each module separately
'''
from scapy.layers.l2 import arping, ARP, Ether, srp
from scapy.layers.inet import IP, UDP, TCP, ICMP
from termcolor import cprint
import argparse
from sys import exit, getsizeof
import struct
import socket

BROADCAST_MAC = 'ff:ff:ff:ff:ff:ff'
IP_MASK = 0x80000000

class NoNetworkSpecified(Exception):
    '''
    Error raised if the user doesn't specify a valid network IP address
    '''

    pass

def check_format_IP(network):
    '''
    Evaluate if network IP address is valid (x.x.x.x/n_netmask)

    Args:
        network (str): Network IP address to be evaluated

    Returns:
        network (str): Network IP address
    '''

    #params[0]=IP 
    #params[1]=number of bits of netmask
    params = network.split('/')
   
    #Error if the number of bits of the netmask is not specified
    if not len(params)==2 or int(params[1])>32 or int(params[1])<=0:
        raise NoNetworkSpecified

    #Split IP address in its fields
    IP_numbers = params[0].split('.')
    
    #Error if the number of fields is not equal to 4
    if not len(IP_numbers)==4:
        raise NoNetworkSpecified
    else:
        #Check if each field has valid value (>=0 and <256)
        for num in IP_numbers:
            if(int(num)>255 or int(num)<0):
                raise NoNetworkSpecified

    #Print Netmask and IP address specified 
    cprint('\n   Netmask:  ', 'blue', attrs=['bold',], end='')
    print(socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - int(params[1]))) & 0xffffffff)))
    cprint('IP address:  ', 'yellow', attrs=['bold',], end='')
    print(f'{params[0]}', end='\n\n')

    return network

def network_scan(network):
    '''
    Detect the MAC addresses of all the devices connected in 
    the local network, using ARP protocol, and display them.

    Args:
        network (str): Network IP address to be evaluated
    '''

    #Create ARP request
    arp_head = ARP(pdst=network)
    ether_head = Ether(dst=BROADCAST_MAC)
    request = ether_head/arp_head
    
    #Send ARP request and wait for response
    responses_list = srp(request, timeout=1)[0]

    cprint(' ______________________________________', 'red')
    cprint("|", 'red', end='')
    cprint(" {:^15} ".format('IP address'), 'blue', 'on_green', end='')
    cprint("|", 'red', end='')
    cprint(" {:^18} ".format('MAC address'), 'blue', 'on_yellow', end='')
    cprint("|", 'red')

    #Check all the responses for sent packets
    for response in responses_list:
        #response[0]= packet sent
        #response[1]= response
        #print(response.show()) to see all fields of the response packet
        cprint("|", 'red', end='')
        cprint(" {:^15} ".format(response[1].psrc), 'green', end='')
        cprint("|", 'red',end='')
        cprint(" {:^18} ".format(response[1].hwsrc), 'yellow', end='')
        cprint("|", 'red')
    
    cprint('|_________________|____________________|', 'red', end='\n\n')


def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-ip", "-net", dest="net", help="IP address of the network in format: x.x.x.x/netmask")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    try:
        if not args.net:
            raise NoNetworkSpecified
        
        network=check_format_IP(args.net)
    except NoNetworkSpecified:
        parser.print_help()
        exit(0)

    return network

def main():
    #Parser of command line arguments
    network = args_parser()    
    #Simplest way to implement ARP network scanner 
    #arping("192.168.1.1/24")
    #Implementation of ARP network scanner from zero
    network_scan(network)


if __name__=="__main__":
    main()
