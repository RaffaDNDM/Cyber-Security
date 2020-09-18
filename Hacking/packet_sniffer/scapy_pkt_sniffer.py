from termcolor import cprint
import subprocess
from scapy.layers.l2 import sniff, ARP
from scapy.layers.inet import IP, TCP, UDP, ICMP
import argparse
import os

VERBOSE = False
INTERFACE = ''
eth_num=0
ip_num=0
arp_num=0
unkown_net_num=0
tcp_num=0
udp_num=0
icmp_num=0
unkown_transport_num=0

LINE = '____________________________________________'
COLOR_L2 = 'red'
COLOR_L3 = 'green'
COLOR_L4 = 'blue'


'''
Parser of command line arguments
'''
def args_parser():
    global INTERFACE, VERBOSE

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-interface", "-if", dest="interface", help="Interface on which we apply packet sniffing")
    parser.add_argument("-verbose", "-v", dest="verbose", help="Specification of packets content", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.interface:
        parser.print_help()
        exit(0)
    
    VERBOSE = args.verbose
    INTERFACE = args.interface


'''
Print number of sniffed packets for each type of protocol
'''
def print_state_pkt(interface, eth_num, ip_num, arp_num, unkown_net_num, tcp_num, udp_num, icmp_num, unkown_transport_num):
            
    subprocess.call('cls' if os.name=='nt' else 'clear')
    cprint('\n\nInterface:   ', 'yellow', attrs=['bold',], end='')
    print(f'{interface}')
    
    cprint(LINE+'\nDLL LAYER PACKETS (layer 2)\n'+LINE, COLOR_L2, attrs=['bold',])
    cprint('Ethernet: ', COLOR_L2)
    print(f'{eth_num}')
    cprint(LINE, COLOR_L2, attrs=['bold',], end='\n\n')
    cprint(LINE+'\nNETWORK PACKETS (layer 3)\n'+LINE, COLOR_L3, attrs=['bold',])
    cprint('IP:  ', COLOR_L3)
    print(f'{ip_num}')
    cprint('ARP: ', COLOR_L3)
    print(f'{arp_num}')
    cprint('Other: ', COLOR_L3)
    print(f'{unkown_net_num}')
    cprint(LINE, COLOR_L3, attrs=['bold',], end='\n\n')
    cprint(LINE+'\nTRANSPORT/CONTROL PACKETS (layer 4)\n'+LINE, COLOR_L4, attrs=['bold',])
    cprint('ICMP:  ', COLOR_L4)
    print(f'{icmp_num}')
    cprint('TCP: ', COLOR_L4)
    print(f'{tcp_num}')
    cprint('UDP: ', COLOR_L4)
    print(f'{udp_num}')
    cprint('Other: ', COLOR_L4)
    print(f'{unkown_transport_num}')
    cprint(LINE, COLOR_L4, attrs=['bold',], end='\n\n')


'''
Process each packet sniffed
'''
def analyse_pkt(packet):
    global eth_num, arp_num, ip_num, tcp_num, udp_num, icmp_num, unkown_transport_num, unkown_net_num

    #Laayer 2 packet
    eth_num+=1

    if VERBOSE:
        print(packet.show())
    else:
        #Layer 3 packet
        if packet.haslayer(ARP):
            arp_num+=1
        elif packet.haslayer(IP):
            ip_num+=1
            #Layer 4 packet
            if packet.haslayer(TCP):
                tcp_num+=1
            elif packet.haslayer(UDP):
                udp_num+=1
            elif packet.haslayer(ICMP):
                icmp_num+=1
            else:
                unkown_transport_num+=1
        else:
            unkown_net_num+=1

        #Print number of sniffed packets
        print_state_pkt(INTERFACE, eth_num, ip_num, arp_num, unkown_net_num, tcp_num, udp_num, icmp_num, unkown_transport_num)


'''
Main function
'''
def main():
    args_parser()

    try:
        #No store of the packet but analyzing on fly
        sniff(iface=INTERFACE, store=False, prn=analyse_pkt)
    except KeyboardInterrupt:
        print('', end='\n\n')


if __name__=='__main__':
    main()
