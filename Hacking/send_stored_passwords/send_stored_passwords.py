import subprocess
import smtplib

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


def main():
    mail, password = credentials()
    send_mail(mail, password, 'ciao')

if __name__=='__main__':
    main()