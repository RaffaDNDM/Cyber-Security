import netfilterqueue
from scapy.layers.l2 import Raw
from scapy.layers.inet import IP, TCP
import argparse
import os
from termcolor import cprint
import re

LINE = '____________________________________________________________'

#Process each packet
def process_packet(packet):
    IP_pkt = IP(packet.get_payload())
    
    if IP_pkt.haslayer(Raw) and IP_pkt.haslayer(TCP):
        if IP_pkt[TCP].dport == 80:
            cprint('Request', 'red', attrs=['bold',], end='')
            #Search for Accept-Encoding Header (?\\r\\n = stop at first occurrence of \\r\\n)
            #Remove Accept-Encoding header from request(we don't understand any encoding)
            new_load = re.sub('Accept-Encoding:.*?\r\n', '', IP_pkt[Raw].load)
           
            print(new_load)
            IP_pkt[Raw].load = new_load
                
            #Scapy recomputes them
            del IP_pkt[IP].len
            del IP_pkt[IP].chksum
            del IP_pkt[TCP].chksum

            packet.set_payload(bytes(IP_pkt))

        elif IP_pkt[TCP].sport == 80:
            cprint('Response', 'blue', attrs=['bold',])
            print(IP_pkt.show())

    packet.accept()



#Parser of command line argument
def args_parser():
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-local", "-l", dest="local", help="If specified, IPTABLES updated to run program on local. Otherwise it works on forward machine (e.g. with arp spoofing).", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()

    return args.local


def main():
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
        cprint(f'\nTCP packets\n{LINE}','green', attrs=['bold',])
        queue.run()
    except KeyboardInterrupt:
        queue.unbind()
        cprint(f'\n{LINE}','green', attrs=['bold',])
        print('Flushing ip table.', end='\n')
        cprint(f'{LINE}','green', attrs=['bold',], end='\n\n')
        os.system('iptables -F')

if __name__=='__main__':
	main()
