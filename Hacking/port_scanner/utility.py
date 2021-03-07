import socket
from termcolor import cprint

def IP_from_host(remote_host):
    try:
        ip_addr = socket.gethostbyname(remote_host)
    except socket.gaierror:
        cprint('Error in the remote address specified.', 'red')
        exit()

    return ip_addr