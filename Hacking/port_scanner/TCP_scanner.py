import csv
from termcolor import cprint, colored
import pyfiglet
import socket
import utility

class TCPScanner:
    OPEN_PORTS = {}

    def __init__(self, remote_host):
        self.ip_address = utility.IP_from_host(remote_host)
        cprint(colored('Target IP address: ', 'red')+self.ip_address, end='\n\n')

        with open('dat/TCP_ports.csv', mode='r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.TCP_ports = {int(row[0]):row[1] for row in csv_reader}

    def scan(self):        
        count = 0
        count_open = 0

        try:
            for port in self.TCP_ports:
                count += 1

                if self.is_open(port):
                    count_open += 1
                    self.OPEN_PORTS[port] = self.TCP_ports[port]

        except KeyboardInterrupt:
            pass  

        print('Number of scanned ports: '+colored(f'{count}','yellow'))
        print('Number of open ports: '+colored(f'{count_open}','yellow'))
        cprint('_________________________________________________', 'blue')
        
        for port in self.OPEN_PORTS:
            print(colored(f'{port}', 'green')+\
                          f' {self.OPEN_PORTS[port]} '+\
                          colored('---> ', 'green') +\
                          colored('OPEN', 'yellow'))

        cprint('_________________________________________________\n', 'blue')

    def is_open(self, port):
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sd.settimeout(1.0)
        state = sd.connect_ex((self.ip_address, port))
        sd.close()
        return state==0

def main():
    title = pyfiglet.figlet_format("TCP Port Scanner") 
    cprint(title, 'blue')
    cprint('_________________________________________________', 'blue')
    remote_host = input(colored('Insert the IP address or the domain name: \n','blue'))
    
    print('')
    scanner = TCPScanner(remote_host)
    cprint('\nOpen Ports on IP address', 'blue')
    scanner.scan()

if __name__=='__main__':
    main()