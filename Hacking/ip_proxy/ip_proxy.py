import netfilterqueue
import os
import argparse
from termcolor import cprint

DROP = False
NUM_PKTS = 0

def process_packet(packet):
    global DROP, NUM_PKTS
    print(packet)
    NUM_PKTS+=1
    if DROP:
        packet.drop()
    else:
        packet.accept()

def args_parser():
    global DROP
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-drop", "-d", dest="drop", help="If specified, it drops all packets otherwise accept them", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    DROP = args.drop

def main():
    args_parser()

    #Packets are blocked and not forwarded
    os.system('iptables -F')
    os.system('iptables -I FORWARD -j NFQUEUE --queue-num 0')

    #O = queue num
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)

    try:
        queue.run()
    except KeyboardInterrupt:
        queue.unbind()
        cprint('\nPackets detected: ','yellow', attrs=['bold',], end='')
        print(f'{NUM_PKTS}\nFlushing ip table.', end='\n\n')
        os.system('iptables -F')

if __name__=='__main__':
	main()
