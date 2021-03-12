from Crypto.Cipher import AES
from Crypto import Random
import argparse
import glob
import os
from termcolor import cprint, colored
import shutil
import tkinter
from tkinter import simpledialog, messagebox
import hashlib

class CipherData:
    '''
    AES cipher/decipher of files inside a folder.

    Args:
        path (str): Path of the folder in which you want to encrypt 
                    all the files (found recursively also in subfolders)

    Attributes:
        KEY (bytes): Key used in AES to encrypt the messages

        PATH (str): Path of the folder in which you want to encrypt 
                    all the files (found recursively also in subfolders)
        
        DEFAULT_PATH: Default path of the folder in which you want to encrypt 
                      all the files (found recursively also in subfolders)

        FILE_LIST (list): List with the paths of all the files found
                          recursively in PATH

        DIR_LIST (list):  List with the paths of all the folder/subfolders
                          analysed to find the files

    '''

    DEFAULT_PATH = 'dat/'
    FILE_LIST = []
    DIR_LIST = []
    CHECK_ENCRYPTED = b'ENCRYPTED'

    def __init__(self, path=DEFAULT_PATH):
        #e.g. INPUT_PATH = .../complete/path/dat/
        if path.endswith('\\') or path.endswith('/'):
            self.INPUT_PATH = path
        else:
            self.INPUT_PATH = path+'/'

        self.OUTPUT_PATH = path.rstrip('\\')
        self.OUTPUT_PATH = path.rstrip('/')
        self.LAST_FOLDER = os.path.os.path.basename(os.path.normpath(self.OUTPUT_PATH))
        self.DIR_LIST.append(self.INPUT_PATH)

        #Read password from the user
        password = ''

        while len(password) < 6:
            pwd_win = tkinter.Tk()
            pwd_win.withdraw()

            #Ask the password to the user
            password = simpledialog.askstring('Password', 'Insert password', parent=pwd_win)

            if len(password) < 6:
                #Password too short to be used
                messagebox.showwarning('Too short password', 'Use a password of at least 6 characters')

        #Create AES key by hashing the password with SHA256
        self.KEY = hashlib.sha256(password.encode()).digest()  


    def encrypt(self):
        '''
        Encrypt all the files found ricursively in PATH.
        '''

        #Find all the files contained recursively in the specified path
        self.find_files_recursive()
        #e.g. OUTPUT PATH = .../complete/path/encoded_dat/
        self.OUTPUT_PATH = self.INPUT_PATH[:-len(self.LAST_FOLDER)-1] + 'encoded_' + self.LAST_FOLDER + '/'
        #Copy the content of INPUT_PATH resursively in OUTPUT_PATH
        shutil.copytree(self.INPUT_PATH, self.OUTPUT_PATH)

        #Encrypt each file
        for x in self.FILE_LIST:
            print('Encoding '+colored(x, 'yellow')+' ...', end= '    ')

            #Read the binary content of a file
            with open(x, 'rb') as f:
                msg = f.read()    
            
            #Encrypt the content
            check, encrypted_msg = self.encrypt_msg(msg)

            if check:
                #Replace the content of the file with its encryption
                print(self.OUTPUT_PATH + x[len(self.INPUT_PATH):])
                
                with open(self.OUTPUT_PATH + x[len(self.INPUT_PATH):], 'wb') as f:
                    f.write(encrypted_msg)

                print(f'completed')
            else:
                print("it was already encrypted")                

    def decrypt(self):
        '''
        Decrypt all the files found ricursively in PATH.
        '''
        
        #Find all the files contained recursively in the specified path
        self.find_files_recursive()
        #e.g. OUTPUT PATH = .../complete/path/decoded_dat/
        self.OUTPUT_PATH = self.INPUT_PATH[:-len(self.LAST_FOLDER)-1] + 'decoded_' + self.LAST_FOLDER + '/'
        #Copy the content of INPUT_PATH resursively in OUTPUT_PATH
        shutil.copytree(self.INPUT_PATH, self.OUTPUT_PATH)

        #Decrypt each file
        for x in self.FILE_LIST:
            print('Decoding '+colored(x, 'yellow')+' ...', end= '    ')

            #Read the binary content of a file
            with open(x, 'rb') as f:
                msg = f.read()    
            
            #Decrypt the content
            check, decrypted_msg = self.decrypt_msg(msg)

            if check:
                print(self.OUTPUT_PATH)
                print(x[len(self.INPUT_PATH):])
                #Replace the content of the file with its decryption
                with open(self.OUTPUT_PATH + x[len(self.INPUT_PATH):], 'wb') as f:
                    f.write(decrypted_msg)

                print('completed')
            else:
                print("it wasn't already encrypted")


    def encrypt_msg(self, msg):
        '''
        Encrypt a bytes message with AES.

        Args:
            msg (bytes): Message to be encrypted

        Returns:
            check (bool): True if the file msg wasn't already encrypted
                          False otherwise

            encoded_msg (bytes): Encrypted message
        '''

        if self.CHECK_ENCRYPTED == msg[:len(self.CHECK_ENCRYPTED)]:
            #The message was already encrypted
            return False, None
        else:
            #Padding msg
            msg = self.pad_msg(msg)
            #Initialization vector
            IV = Random.new().read(AES.block_size)
            #AES cipher with Cipher Block Chaining (CBC) techinque
            cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
            #Message encrypted
            return True, self.CHECK_ENCRYPTED + IV + cipher.encrypt(msg)

    def decrypt_msg(self, msg):
        '''
        Decrypt a bytes message with AES.

        Args:
            msg (bytes): Message to be decrypted

        Returns:
            check (bool): True if the file msg was already encrypted
                          False otherwise
                          
            encoded_msg (bytes): Decrypted message
        '''
        
        if self.CHECK_ENCRYPTED == msg[:len(self.CHECK_ENCRYPTED)]:
            msg = msg[len(self.CHECK_ENCRYPTED):]
            #Initialization vector (beginning of the encoded text)
            IV = msg[:AES.block_size]
            #AES cipher with Cipher Block Chaining (CBC) techinque
            cipher = AES.new(self.KEY, AES.MODE_CBC, IV)
            #Message decrypted (from IV on)
            decoded_msg = cipher.decrypt(msg[AES.block_size:])
            #Message decrypted without last padding bytes
            return True, decoded_msg.rstrip(b"\0")
        else:
            #The message wasn't already encrypted
            return False, None


    def pad_msg(self, msg):
        '''
        Pad a bytes message by appending 0's to reach a size multiple
        of the block size used by AES.
        '''
        return msg + b'\0' * (AES.block_size - len(msg) % AES.block_size)

    def find_files_recursive(self):
        '''
        Find the files contained in the path specified in the
        constructor of the Ransomware, by looking for them 
        recursively in all the found subfolders.
        '''

        #Analyse all the directories in DIR_LIST
        for x in self.DIR_LIST:
            #List all the content of the folder analysed
            content_list = os.listdir(x)
            
            #Analyse the content of the folder
            for f in content_list:

                if os.path.isdir(x+f):
                    #If the content is a directory, the path of the
                    #subfolder is inserted in the directory list, so 
                    #it will be analysed in the next iteration of the
                    #loop
                    self.DIR_LIST.append(x+f+'/')
                else:
                    #If the content is a file, the file path is 
                    #added to FILE_LIST
                    self.FILE_LIST.append(x+f)

            #Show directory analysed during the current iteration
            cprint(x, 'red')

        #Print the list of all the files found recursively
        cprint(self.FILE_LIST, 'yellow')

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-decode", "-d", dest="decode", help="Decode option (by default, encode)", action='store_true')
    parser.add_argument("-path", "-p", dest="path", help="Path with files to be encrypted")
    
    #Parse command line arguments
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print('You need to specify an existing folder')
        exit()

    return args.decode, args.path

def main():
    decode_option, path = args_parser()

    #Creation of the cypher
    cypher = None   

    if path:
        cypher = CipherData(path)
    else:
        cypher = CipherData()

    if decode_option:
        cypher.decrypt()
    else:
        cypher.encrypt()

if __name__=='__main__':
    main()
