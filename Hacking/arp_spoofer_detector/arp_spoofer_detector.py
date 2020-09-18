from scapy.layers.l2 import ARP, Ether, sniff
from termcolor import cprint
from scapy.config import conf

'''
Evaluate MAC address of a specific IP
'''
def get_MAC(ip):
    #ARP request of resolution of IP address ip
    arp_header = ARP(pdst=ip) 
    
    #ARP request sent in broadcast to all hosts connected in the network
    eth_header = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    #Creation of packet by appending ARP packet to Ethernet header
    packet = eth_header/arp_header
    
    #Send packet of layer 2 to each user in the network
    #and wait for timeout seconds for the response
    #response_list = srp()[0]= answers
    #response_list[1]=unanswered
    response_list = srp(packet, timeout=1, verbose=False)[0]
    
    #response_list[0] correspond to first response 
    #(we want to obtain MAC of a specific IP address)
    #first_element[0] = request done for which I obtain a respons
    #first_element[1] = response to request
    return response_list[0][1].hwsrc


'''
Detect ARP spoofing
'''
def detect_spoofer(interface):
    sniff(iface=interface, store=False, prn=check_pkt)


'''
Check if an ARP packet has correct MAC address
'''
def check_pkt(packet):
    #ARP Response
    if packet.haslayer(ARP) and packet[ARP].op == 2:
        
        try:
            real_mac = get_mac(packet[ARP].psrc)
            response_mac = packet[ARP].hwsrc

            #Check if the real MAC is equal to the MAC 
            #in the ARP response
            if real_mac != response_mac:
                cprint('[WARNING] ', 'red', attrs=['bold',], end='')
                print('Under ARP Spoofing attack')
        
        except IndexError:
            #It's my MAC address and get_mac raised exception
            pass


'''
Main function
'''
def main():
    detect_spoofer(conf.iface)


if __name__=='__main__':
    main()
