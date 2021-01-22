import requests
from termcolor import cprint, colored
import argparse

def url_exist(url):
    try:
        return requests.get('http://'+url)
    except requests.exceptions.ConnectionError:
        pass

def discover_hidden_paths(url):
    cprint('Discovered paths','blue')
    cprint('_____________________','blue')

    with open('files_dirs.txt', 'r') as sub_list:
        for line in sub_list:
            hidden_path = line.strip()
            new_url = url+'/'+hidden_path
            response = url_exist(new_url)

            if response:
                print(colored('> ', 'green')+new_url)

    cprint('_____________________','blue')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Existing url (e.g. www.google.com)")
    args = parser.parse_args()

    if url_exist(args.url):
        discover_hidden_paths(args.url)
    else:
        print('Write an existing domain')

if __name__=='__main__':
    main()
