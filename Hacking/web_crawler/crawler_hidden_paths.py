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


def crawler_hidden_paths(url):
    '''
    Display the discovered hidden paths on screen.

    Args:
        url (str): URL of the domain in which you want 
                   to discover the hidden paths
    '''

    cprint('Discovered paths','blue')
    cprint('_____________________','blue')

    with open('files_dirs.txt', 'r') as sub_list:
        for line in sub_list:
            #Appeng to the url of the site that you 
            #want to attck a known hidden path
            hidden_path = line.strip()
            new_url = url+'/'+hidden_path
            #Check if the hidden path exists
            response = url_exist(new_url)

            #If I have a response, the hidden path exists
            #and it will be displayed on screen
            if response:
                print(colored('> ', 'green')+new_url)

    cprint('_____________________','blue')


def main():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Existing url (e.g. www.google.com)")
    args = parser.parse_args()

    #Checks if the URL specified exists
    if url_exist(args.url):
        crawler_hidden_paths(args.url)
    else:
        print('Write an existing domain')

if __name__=='__main__':
    main()
