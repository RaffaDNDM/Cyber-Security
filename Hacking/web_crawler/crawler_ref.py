import requests
import re
import urllib.parse as urlparse
from termcolor import cprint, colored
import argparse

def url_exist(url):
    try:
        return requests.get('http://'+url)
    except requests.exceptions.ConnectionError:
        pass

def references_in_url(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', str(response.content))

URL_LIST = []

def crawler_ref(url):
    global URL_LIST
    references = references_in_url(url)
    
    for ref in references:
        #Join a base URL and a possibly relative URL to
        #form an absolute interpretation of the latter.
        complete_url = urlparse.urljoin(url, ref)

        #Dynamic subsection from # on
        if '#' in complete_url:
            #Take only link before the #
            complete_url = complete_url.split('#')[0]
        
        #The url must be on the site and unique (not already discovered)
        if url in complete_url and complete_url not in URL_LIST:
            print(colored('> ', 'green')+complete_url)
            URL_LIST.append(complete_url)
            #Recursion on url already discoverd
            crawler_ref(complete_url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Existing url (e.g. http://www.google.com)")
    args = parser.parse_args()

    if url_exist(args.url):
        cprint('Discovered URLs','blue')
        cprint('_____________________','blue')
        crawler_ref('http://'+args.url)
        cprint('_____________________','blue')
    else:
        print('Write an existing domain')

if __name__=='__main__':
    main()
