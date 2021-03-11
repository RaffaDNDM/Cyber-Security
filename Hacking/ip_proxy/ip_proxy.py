import netfilterqueue
import os
import argparse
from termcolor import cprint
from scapy.layers.inet import IP

DROP = False
VERBOSE = False
NUM_PKTS = 0


def process_packet(packet):
    '''
    Process each packet in Network Filter queue
    '''

    global DROP, VERBOSE, NUM_PKTS
    
    if VERBOSE:
        IP_pkt = IP(packet.get_payload())
        print(IP_pkt.show())
    else:
        print(packet)

    NUM_PKTS+=1
    if DROP:
        #Block the connection of the victim
        packet.drop()
    else:
        #Analyse packets sent between victim and servers
        packet.accept()


def args_parser():
    '''
    Parser of command line arguments
    '''

    global DROP, VERBOSE

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-drop", "-d", dest="drop", help="If specified, it drops all packets otherwise accept them", action='store_true')
    parser.add_argument("-local", "-l", dest="local", help="If specified, IPTABLES updated to run program on local. Otherwise it works on forward machine (e.g. with arp spoofing).", action='store_true')
    parser.add_argument("-verbose", "-v", dest="verbose", help="If specified, print all the fields of IP packet", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()

    #Check if the arguments have been specified on command line
    DROP = args.drop
    VERBOSE = args.verbose
    
    return args.local

def main():
    #Parser of command line arguments
    local = args_parser()

    #Packets are blocked and not forwarded
    if local:
        os.system('iptables -F')
        os.system('iptables -I INPUT -j NFQUEUE --queue-num 0')
        os.system('iptables -I OUTPUT -j NFQUEUE --queue-num 0')
    else:
        os.system('iptables -F')
        os.system('iptables -I FORWARD -j NFQUEUE --queue-num 0')


    #O = queue num
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)

    try:
        queue.run()
    except KeyboardInterrupt:
        queue.unbind()
        print('Flushing ip table.', end='\n\n')
        os.system('iptables -F')

if __name__=='__main__':
	main()
