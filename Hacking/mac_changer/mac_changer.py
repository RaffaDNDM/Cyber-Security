#!/usr/bin/env python

import subprocess
import argparse
import re
from termcolor import cprint

'''
No MAC address specified as command line argument
'''
class NoMACSpecified(Exception):
    pass


'''
No network interface specified as command line argument
'''
class NoInterfaceSpecified(Exception):
    pass


'''
Change current MAC address of network interface with a new one
'''
def MAC_change(interface, new_MAC):
    #Disable the specified interface
    subprocess.call(["ifconfig", interface, "down"])
    
    #Setting new MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_MAC])
    
    #Enable the spesified interface
    subprocess.call(["ifconfig", interface, "up"])


'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-i", "-interface", dest="interface", help="Name of the interface for which you want to change the MAC address")
    parser.add_argument("-hw", "-mac", dest="mac", help="New MAC address")
    
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.interface:
        raise NoInterfaceSpecified
    if not args.mac:
        raise NoMACSpecified
    
    return args.interface, args.mac


'''
Obtain current MAC address of interface
'''
def current_MAC(interface):
    #Save current output of the program called
    output = subprocess.check_output(["ifconfig", interface])
    MAC = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(output))
    
    #Check if MAC exists for this interface
    if not MAC:
        raise NoMACSpecified

    return MAC.group(0)


'''
Main function
'''
def main():
    try:
        #Parser of command line arguments
        interface, mac = args_parser()
    except NoMACSpecified:
        print("You need to specify a MAC address")
        exit(0)
    except NoInterfaceSpecified:
        print("You need to specify an interface name")
        exit(0)

    #Old MAC address
    try:
        cprint("Old MAC address:", "blue", "on_green", end='')
        cprint(" {}".format(current_MAC(interface)), "cyan", attrs=["bold",])
    except NoMACSpecified:
        print("No OLD MAC address found")
        exit(0)

    #Changing MAC address
    MAC_change(interface, mac)

    #New MAC address
    try:
        cprint("New MAC address:", "blue", "on_red", end='')
        cprint(f" {current_MAC(interface)}", "yellow", attrs=["bold",])
    except NoMACSpecified:
        print("No OLD MAC address found")
        exit(0)


if __name__=='__main__':
    main()
