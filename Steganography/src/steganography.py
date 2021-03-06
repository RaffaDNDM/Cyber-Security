import argparse
import os
from image_steganography import ImageSteganography
from audio_steganography import AudioSteganography
from termcolor import cprint 

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-encode", "-e", dest="encode_check", help="Encode the message in the file", action='store_true')
    parser.add_argument("-input", "-i", dest="input", help="Input file path of the image (PNG) or the audio (WAV) to be encrypted or decrypted")
    parser.add_argument("-output", "-o", dest="output", help="Output file path of the image (PNG) or the audio (WAV) with secret message")
    parser.add_argument("-message", "-msg", dest="msg", help="Message to be encrypted")

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if (not args.input) or (not os.path.exists(args.input)) or \
        (args.encode_check and not args.output):
        parser.print_help()
        exit(0)
    
    return args.encode_check, args.input, args.output, args.msg

def main():
    is_encode, input_path, output_path, secret_msg = args_parser()
    st = None

    if input_path[-4:] == '.png':
        st = ImageSteganography(input_path)
    elif input_path[-4:] == '.wav':
        st = AudioSteganography(input_path)
    else:
        cprint('\nFile type not supported', 'red', end='\n\n')
        exit(0)

    if is_encode:
        if not secret_msg:
            cprint('\nWrite the message to be hidden:', 'blue')
            cprint('_________________________________', 'blue')
            secret_msg = input()
            cprint('_________________________________', 'blue', end='\n\n')
        
        st.encode(secret_msg, output_path)
    else:
        cprint('\nHidden message:', 'blue')
        cprint('_________________________________', 'blue')
        st.decode()
        cprint('_________________________________', 'blue', end='\n\n')

if __name__=='__main__':
    main()