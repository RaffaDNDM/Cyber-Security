import socket, threading
from termcolor import cprint

def manage_info(client_sd, client_address):
    size = ''
    while True:
        size += client_sd.recv(1).decode()

        if size[-2:] == '\r\n':
            size = size[:-2]
            break

    msg = client_sd.recv(int(size)).decode()
    cwd, subfolders = msg.split('\r\n')
    subfolders_list = subfolders.split(',')

    cprint(f'\n{cwd}', 'yellow')
    for fold in subfolders_list:
        print(f'\t{fold}')

def main():
    try:
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sd.bind(('127.0.0.1',8080))
        sd.listen(10)
    except socket.error:
        print('Something goes wrong')
        exit()

    while True:
        client_sd, client_address = sd.accept()
        t = threading.Thread(target=manage_info, args=(client_sd, client_address))
        t.start()

if __name__=='__main__':
    main()