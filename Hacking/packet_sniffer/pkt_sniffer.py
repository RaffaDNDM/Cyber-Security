from struct import pack
from struct import unpack
import sys
import socket
import os
import argparse
from termcolor import cprint
import subprocess
import csv 

#Format of the main packets
#! Network Byte Order = Big Endian Order
ETH_FORMAT = '! 6s 6s H'
ARP_FORMAT = '! H H B B H 6s 4s 6s 4s'
IP_FORMAT = '! x B H H H B B H 4s 4s'
TCP_FORMAT = '! H H L L H'
UDP_FORMAT = '! H H H H'

#IP type
ICMP_NUM = 1
TCP_NUM = 6
UDP_NUM = 17

#File with ICMP types
ICMP_TYPE_FILE = "icmp-parameters-types.csv"

#Color on display for info on Layer 2, 3, 4 packets
COLOR_L2 = 'red'
COLOR_L3 = 'green'
COLOR_L4 = 'blue'
#String to be print for IP packets on display
network_types = {ICMP_NUM:'ICMP header', TCP_NUM:'TCP header', UDP_NUM:'UDP header'}
LINE = '____________________________________________'


def get_MAC(addr):
    '''
    Obtain MAC address string from the number specified
    '''

    #MAC address with dot format from array of char numbers
    #Convert each char number of addr into string
    #and then separate them with :
    return ':'.join(map(str, addr))

def get_IP(addr):
    '''
    Obtain MAC address string from the number specified
    '''

    #IP address with dot format from array of char numbers
    #Convert each char number of addr into string
    #and then separate them with :
    return '.'.join(map(str, addr))

def eth_pkt(raw_data, verbose):
    '''
    Ethernet decapsulation
    '''

    dst, src, protocol_type = unpack(ETH_FORMAT, raw_data[:14])
    
    #Source MAC address
    src_MAC = get_MAC(src)
    #Destination MAC address
    dst_MAC = get_MAC(dst)
    #Payload of Ethernet packet
    data = raw_data[14:]
            
    if verbose:
        cprint('\n\nEthernet header\n'+LINE, COLOR_L2, attrs=['bold',])
        cprint('Src MAC:   ', COLOR_L2, end='')
        print(src_MAC)
        cprint('Dst MAC:   ', COLOR_L2, end='')
        print(dst_MAC)
        cprint('Protocol:  ', COLOR_L2, end='')
        print(hex(protocol_type))

    return src_MAC, dst_MAC, protocol_type, data

def arp_pkt(raw_data, verbose):
    '''
    ARP decapsulation
    '''

    hw_protocol, lv3_protocol, hw_len, lv3_len, op_code, src_hw_addr, src_lv3_addr, dst_hw_addr, dst_lv3_addr = unpack('! H H B B H 6s 4s 6s 4s', raw_data[:28])
    
    #Source address
    src_MAC = get_MAC(src_hw_addr)
    #Destination address
    dst_MAC = get_MAC(dst_hw_addr)
    #Source address
    src_IP = get_IP(src_lv3_addr)
    #Destination address
    dst_IP = get_IP(dst_lv3_addr)
    #Type of operation performed by packet (Useless for only reception)
    op = 'Request' if op_code==1 else 'Reply'


    if verbose:
        cprint('\nARP header\n'+LINE, COLOR_L3, attrs=['bold',])
        cprint('HW Protocol:   ', COLOR_L3, end='')
        print(hw_protocol)
        cprint('L3 Protocol:   ', COLOR_L3, end='')
        print(lv3_protocol)
        cprint('HW Length:   ', COLOR_L3, end='')
        print(hw_len)
        cprint('L3 Length:   ', COLOR_L3, end='')
        print(lv3_len)
        cprint('OP code:   ', COLOR_L3, end='')
        print(op + ' ('+str(op_code)+')')
        cprint('Src MAC:   ', COLOR_L3, end='')
        print(src_MAC)
        cprint('Src IP:  ', COLOR_L3, end='')
        print(src_IP)
        cprint('Dst MAC:   ', COLOR_L3, end='')
        print(dst_MAC)
        cprint('Dst IP:  ', COLOR_L3, end='')
        print(dst_IP, end='\n\n')

    return op, src_MAC, dst_MAC, src_IP, dst_IP

def ipv4_pkt(raw_data, verbose):
    '''
    IPv4 decapsulation
    '''

    #! Network Byte Order = Big Endian Order
    vhl = raw_data[0]
    #Version of IP protocol
    version = vhl >> 4
    #Length of IP Header in words of 4 bytes
    header_len = (vhl & 0xF) * 4
    
    #x = padding Byte
    # ttl, proto, src, dst = struct.unpack('! 6s 6s H', raw_data[1:header_len])
    tos, total_length, id_pkt, flag_frag, ttl, protocol, checksum, src, dst = unpack('! x B H H H B B H 4s 4s', raw_data[:header_len])
    
    #Source address
    src_IP = get_IP(src)
    #Destination address
    dst_IP = get_IP(dst)
    #Payload of IP packet
    data = raw_data[header_len:]
    
    if verbose:
        cprint('\nIP header\n'+LINE, COLOR_L3, attrs=['bold',])
        cprint('Version:   ', COLOR_L3, end='')
        print(version)
        cprint('Header length:   ', COLOR_L3, end='')
        print(header_len)
        cprint('Type of service:   ', COLOR_L3, end='')
        print(tos)
        cprint('Total Length:   ', COLOR_L3, end='')
        print(total_length)
        cprint('ID:   ', COLOR_L3, end='')
        print(id_pkt)
        cprint('Flags Fragment:   ', COLOR_L3, end='')
        print(flag_frag)
        cprint('Upper Layer Protocol:   ', COLOR_L3, end='')
        print(protocol)
        cprint('Checksum:  ', COLOR_L3, end='')
        print(checksum)
        cprint('Src IP:   ', COLOR_L3, end='')
        print(src_IP)
        cprint('Dst IP:  ', COLOR_L3, end='')
        print(dst_IP)
    
    return version, header_len, ttl, protocol, src_IP, dst_IP, data

def icmp_pkt(raw_data, verbose):
    '''
    ICMP decapsulation
    '''

    type_list = ''
    
    #Open ICMP types packet
    with open(ICMP_TYPE_FILE, 'r') as f:
        rows = csv.reader(f, delimiter=',')
        
        #Search for correct ICMP type in the list
        for row in rows:
            if(int(row[0])==int(raw_data[0])):
                type_list = row[1]

    if verbose:
        cprint('\nICMP header\n'+LINE, COLOR_L4, attrs=['bold',])
        cprint('Type:   ', COLOR_L4, end='')
        print(str(raw_data[0])+' ('+type_list+')', end='\n\n')
    
    return type_list[1]

def tcp_pkt(raw_data, verbose):
    '''
    TCP decapsulation
    '''

    src_port, dst_port, seq, ack, off_res_flags = unpack(TCP_FORMAT, raw_data[:14])
    
    #Offset = number of words of 4 bytes
    offset = (off_res_flags >> 12) * 4
    #Value of flag bits
    urg = (off_res_flags & 32) >> 5
    ack = (off_res_flags & 16) >> 4
    psh = (off_res_flags & 8) >> 3
    rst = (off_res_flags & 4) >> 2
    syn = (off_res_flags & 2) >> 1
    fin = off_res_flags & 1
    data = raw_data[offset:]

    if verbose:
        cprint('\nTCP header\n'+LINE, COLOR_L4, attrs=['bold',])
        cprint('Src Port:   ', COLOR_L4, end='')
        print(src_port)
        cprint('Dst Port:   ', COLOR_L4, end='')
        print(dst_port)
        cprint('Sequence Number:   ', COLOR_L4, end='')
        print(seq)
        cprint('ACK Number:   ', COLOR_L4, end='')
        print(ack)
        cprint('Offset Reserved Flags:   ', COLOR_L4, end='')
        print(off_res_flags, end='\n\n')
    
    return src_port, dst_port, seq, ack, urg, ack, psh, rst, syn, fin, data

def udp_pkt(raw_data, verbose):
    '''
    UDP decapsulation
    '''

    src_port, dst_port, udp_len, checksum = unpack(UDP_FORMAT, raw_data[:8])
    
    if verbose:
        cprint('\nUDP header\n'+LINE, COLOR_L4, attrs=['bold',])
        cprint('Src Port:   ', COLOR_L4, end='')
        print(src_port)
        cprint('Dst Port:   ', COLOR_L4, end='')
        print(dst_port)
        cprint('Length:   ', COLOR_L4, end='')
        print(udp_len)
        cprint('Checksum:   ', COLOR_L4, end='')
        print(checksum, end='\n\n')
    
    return src_port, dst_port, udp_len, checksum

def print_state_pkt(interface, eth_num, ip_num, arp_num, unkown_net_num, tcp_num, udp_num, icmp_num, unkown_transport_num):
    '''
    Print number of sniffed packets for each type of protocol
    '''
            
    subprocess.call('cls' if os.name=='nt' else 'clear')
    cprint('\n\nInterface:   ', 'yellow', attrs=['bold',], end='')
    print(f'{interface}')
    
    cprint(LINE+'\nDLL LAYER PACKETS (layer 2)\n'+LINE, COLOR_L2, attrs=['bold',])
    cprint('Ethernet: ', COLOR_L2)
    print(f'{eth_num}')
    cprint(LINE, COLOR_L2, attrs=['bold',], end='\n\n')
    cprint(LINE+'\nNETWORK PACKETS (layer 3)\n'+LINE, COLOR_L3, attrs=['bold',])
    cprint('IP:  ', COLOR_L3)
    print(f'{ip_num}')
    cprint('ARP: ', COLOR_L3)
    print(f'{arp_num}')
    cprint('Other: ', COLOR_L3)
    print(f'{unkown_net_num}')
    cprint(LINE, COLOR_L3, attrs=['bold',], end='\n\n')
    cprint(LINE+'\nTRANSPORT/CONTROL PACKETS (layer 4)\n'+LINE, COLOR_L4, attrs=['bold',])
    cprint('ICMP:  ', COLOR_L4)
    print(f'{icmp_num}')
    cprint('TCP: ', COLOR_L4)
    print(f'{tcp_num}')
    cprint('UDP: ', COLOR_L4)
    print(f'{udp_num}')
    cprint('Other: ', COLOR_L4)
    print(f'{unkown_transport_num}')
    cprint(LINE, COLOR_L4, attrs=['bold',], end='\n\n')

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-interface", "-if", dest="interface", help="Interface on which we apply packet sniffing")
    parser.add_argument("-verbose", "-v", dest="verbose", help="Specification of packets content", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.interface:
        parser.print_help()
        exit(0)
    
    return args.interface, args.verbose


def main():
    ETH_P_ALL = 3
    sd = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
    interface, verbose = args_parser()
    sd.bind((interface, 0))
    eth_num = 0
    arp_num = 0
    ip_num = 0
    unkown_net_num = 0
    udp_num = 0
    tcp_num = 0
    icmp_num = 0
    unkown_transport_num = 0

    if os.name == 'nt':
        sd.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True: 
            raw_data = sd.recv(1518)
            src_MAC, dst_MAC, network_protocol, payload_DLL = eth_pkt(raw_data, verbose)
            eth_num+=1

            if(network_protocol==0x0800): #IP packets
                ip_num+=1
                version, header_len, ttl, protocol, src_IP, dst_IP, payload_IP = ipv4_pkt(payload_DLL, verbose)
                unkown_protocol = False

                if(protocol==ICMP_NUM): #ICMP packets
                    icmp_num+=1
                    icmp_type = icmp_pkt(payload_IP, verbose)
                elif(protocol==TCP_NUM): #TCP packets
                    tcp_num+=1
                    src_port, dst_port, seq, ack, urg, ack, psh, rst, syn, fin, data = tcp_pkt(payload_IP, verbose)
                elif(protocol==UDP_NUM): #UDP packets
                    udp_num+=1
                    src_port, dst_port, udp_len, checksum = udp_pkt(payload_IP, verbose)
                else:
                    unkown_transport_num+=1
                    unkown_protocol = True

                if verbose:
                    if unkown_protocol:
                        cprint('Unkown Transport Protocol', COLOR_L4)

            elif(network_protocol==0x0806):
                arp_num+=1
                op, src_MAC, dst_MAC, src_IP, dst_IP = arp_pkt(payload_DLL, verbose)
            else:
                unkown_net_num+=1
                if verbose:
                    cprint('Unkown Network Protocol', COLOR_L3)


            if not verbose:
                print_state_pkt(interface, eth_num, ip_num, arp_num, unkown_net_num, tcp_num, udp_num, icmp_num, unkown_transport_num) 
    
    except KeyboardInterrupt:
        sd.close()
    

if __name__=='__main__':
    main()
