#!/usr/bin/env python

import subprocess
import argparse
import re
from termcolor import cprint

class NoMACSpecified(Exception):
    pass

class NoInterfaceSpecified(Exception):
    pass

def MAC_change(interface, new_MAC):
    #Disable the specified interface
    subprocess.call(["ifconfig", interface, "down"])
    #Setting new MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_MAC])
    #Enable the spesified interface
    subprocess.call(["ifconfig", interface, "up"])

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

def current_MAC(interface):
    #Save current output of the program called
    output = subprocess.check_output(["ifconfig", interface])
    MAC = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(output))
    #Check if MAC exists for this interface
    if not MAC:
        raise NoMACSpecified

    return MAC.group(0)

def main():
    #Command Line Parsing
    try:
       interface, mac = args_parser()
    except NoMACSpecified:
        print("You need to specify a MAC address")
    except NoInterfaceSpecified:
        print("You need to specify an interface name")
    
    #Old MAC address
    try:
        cprint("Old MAC address:", "blue", "on_green", end='')
        cprint(" {}".format(current_MAC(interface)), "cyan", attrs=["bold",])
    except NoMACSpecified:
        print("No OLD MAC address found")

    #Changing MAC address
    MAC_change(interface, mac)

    #New MAC address
    try:
        cprint("New MAC address:", "blue", "on_red", end='')
        cprint(f" {current_MAC(interface)}", "yellow", attrs=["bold",])
    except NoMACSpecified:
        print("No OLD MAC address found")

if __name__=='__main__':
    main()
