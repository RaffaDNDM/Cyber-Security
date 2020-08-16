from termcolor import colored
from struct import pack
from struct import unpack
import sys
import socket
import os

#! Network Byte Order = Big Endian Order
ETH_FORMAT = '! 6s 6s H'
ARP_FORMAT = '! H H B B H 6s 4s 6s 4s'
IP_FORMAT = '! x B H H H B B H 4s 4s'
TCP_FORMAT = '! H H L L H'
UDP_FORMAT = '! H H H H'

ICMP_NUM = 1
TCP_NUM = 6
UDP_NUM = 17

ICMP_TYPE_FILE = "icmp-parameters-types.csv"

network_types = {ICMP_NUM:'ICMP header', TCP_NUM:'TCP header', UDP_NUM:'UDP header'}

def get_MAC(addr):
    '''
    IP address with dot format from array of char numbers
    Convert each char number of addr into string
    and then separate them with :
    '''
    return ':'.join(map(str, addr))

def get_IP(addr):
    '''
    IP address with dot format from array of char numbers
    Convert each char number of addr into string
    and then separate them with :
    '''
    return '.'.join(map(str, addr))

def eth_pkt(raw_data):
    dst, src, protocol_type = unpack(ETH_FORMAT, raw_data[:14])
    src_MAC = get_MAC(src)
    dst_MAC = get_MAC(dst)
    data = raw_data[14:]
    
    return src_MAC, dst_MAC, protocol_type, data


def arp_pkt(raw_data):
    hw_protocol, lv3_protocol, hw_len, lv3_len, op_code, src_hw_addr, src_lv3_addr, dst_hw_addr, dst_lv3_addr = unpack('! H H B B H 6s L 6s L', raw_data[:28])
    
    #Source address
    src_MAC = get_MAC(src_hw_addr)
    #Destination address
    dst_MAC = get_MAC(dst_hw_addr)
    #Source address
    src_IP = get_IP(src_lv3_addr)
    #Destination address
    dst_IP = get_IP(dst_lv3_addr)
    #Type of operation performed by packet
    op = 'Request' if op_code==1 else 'Reply'
    
    return op, src_MAC, dst_MAC, src_IP, dst_IP


def ipv4_pkt(raw_data):
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
    src_IP = get_MAC(src)
    #Destination address
    dst_IP = get_MAC(dst)
    #Payload of IP packet
    data = raw_data[header_len:]
    
    return version, header_len, ttl, protocol, src_IP, dst_IP, data


def icmp_pkt(raw_data):
    with open(ICMP_TYPE_FILE, 'r') as f:
        lines = f.readLines()

    code_type = lines[raw_data[0]]
    type_list = code_type.split(',',1)

    return type_list[1]


def tcp_pkt(raw_data):
    src_port, dst_port, seq, ack, off_res_flags = unpack(TCP_FORMAT, raw_data[:14])
    
    #Offset = number of words of 4 bytes
    offset = (off_res_flags >> 12) * 4
    urg = (off_res_flags & 32) >> 5
    ack = (off_res_flags & 16) >> 4
    psh = (off_res_flags & 8) >> 3
    rst = (off_res_flags & 4) >> 2
    syn = (off_res_flags & 2) >> 1
    fin = off_res_flags & 1
    data = raw_data[offset:]

    return src_port, dst_port, seq, ack, urg, ack, psh, rst, syn, fin, data

def udp_pkt(raw_data):
    src_port, dst_port, udp_len, checksum = unpack(UDP_FORMAT, raw_data[:8])
    return src_port, dst_port, udp_len, checksum

def main():
    sd = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    print(sys.argv)
    sd.bind((sys.argv[1], 0))
    
    if os.name == 'nt':
        sd.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        raw_data, addr = sd.recv(65535)

        src_MAC, dst_MAC, network_protocol, payload_DLL = eth_pkt(raw_data)
        print(colored('Ethernet header', 'red'))

        if(network_protocol==0x0800):
            print(colored('IP header', 'green'))
            version, header_len, ttl, protocol, src_IP, dst_IP, payload_IP = ipv4_pkt(payload_DLL)

            if(protocol==ICMP_NUM): #ICMP
                icmp_type = icmp_pkt(payload_IP)
                print(colored(network_types[protocol]), 'blue')
            elif(protocol==TCP_NUM): #TCP
                src_port, dst_port, seq, ack, urg, ack, psh, rst, syn, fin, data = tcp_pkt(payload_IP)
                print(colored(network_types[protocol]), 'blue')
            elif(protocol==UDP_NUM): #UDP
                src_port, dst_port, udp_len, checksum = udp_pkt(payload_IP)
                print(colored(network_types[protocol]), 'blue')
            else:
                print('Network protocol unknown', 'blue')

        elif(network_protocol==0x0806):
            print(colored('ARP header', 'green'))
            op, src_MAC, dst_MAC, src_IP, dst_IP = arp_pkt(payload_DLL)


if __name__=='__main__':
    main()
