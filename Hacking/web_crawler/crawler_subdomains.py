import requests
from termcolor import cprint, colored
import argparse

def url_exist(url):
    '''
    Check if an URL exists by returning the 
    resource obtain through the HTTP GET request.

    Args:
        url (str): URL to be checked.
    
    Returns:
        result (str): Resource obtained at the 
                      specified URL
    '''

    try:
        return requests.get('http://'+url)
    except requests.exceptions.ConnectionError:
        pass

def crawler_subdomains(url):
    '''
    Display the discovered hidden subdomains of a domain.

    Args:
        url (str): URL of the domain in which you want 
                   to discover the hidden subdomains
    '''
    
    cprint('Discovered subdomains','blue')
    cprint('_____________________','blue')

    with open('subdomains.txt', 'r') as sub_list:
        for line in sub_list:
            subdomain = line.strip()
            new_url = subdomain+'.'+url
            response = url_exist(new_url)

            if response:
                print(colored('> ', 'green')+new_url)

    cprint('_____________________','blue')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="existing domain (e.g. google.com)")
    args = parser.parse_args()

    if url_exist(args.domain):
        crawler_subdomains(args.domain)
    else:
        print('Write an existing domain')

if __name__=='__main__':
    main()