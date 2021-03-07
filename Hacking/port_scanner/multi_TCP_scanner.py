import csv
from termcolor import cprint, colored
import pyfiglet
import socket
import utility
import os
from multiprocessing.pool import ThreadPool

class TCPScanner:
    OPEN_PORTS = {}

    def __init__(self, remote_host):
        self.ip_address = utility.IP_from_host(remote_host)
        cprint(colored('Target IP address: ', 'red')+self.ip_address, end='\n\n')

        with open('dat/TCP_ports.csv', mode='r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.TCP_ports = {int(row[0]):row[1] for row in csv_reader}

    def scan(self):        
        try:
            workers_num = os.cpu_count()
            
            with ThreadPool(workers_num) as pool:
                for loop_index, _ in enumerate(pool.imap(self.is_open, self.TCP_ports)):
                    print(colored(f'\r{loop_index/len(self.TCP_ports)*100:.2f}%', 'yellow')+' ports scanned.', end='')

        except KeyboardInterrupt:
            pass  

        cprint('\n_________________________________________________', 'blue')
        
        for port in self.OPEN_PORTS:
            print(colored(str(port), 'green')+' '+\
                          str(self.OPEN_PORTS[port])+' '+\
                          colored('---> ', 'green') +\
                          colored('OPEN', 'yellow'))

        cprint('_________________________________________________\n', 'blue')

    def is_open(self, port):
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sd.settimeout(1.0)
        state = sd.connect_ex((self.ip_address, port))
        sd.close()

        if state == 0:
            self.OPEN_PORTS[port] = self.TCP_ports[port]

def main():
    title = pyfiglet.figlet_format("TCP Port Scanner") 
    cprint(title, 'blue')
    cprint('_________________________________________________', 'blue')
    remote_host = input(colored('Insert the IP address or the domain name: \n','blue'))
    
    print('')
    scanner = TCPScanner(remote_host)
    cprint('Open Ports on IP address', 'blue')
    scanner.scan()

if __name__=='__main__':
    main()