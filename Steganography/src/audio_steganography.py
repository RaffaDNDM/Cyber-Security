from scipy.io import wavfile as wave
import numpy as np
from termcolor import cprint
import utility

class AudioSteganography:
    ASCII_SIZE = 8 #size of an ASCII char in bits

    def __init__(self, path):
        self.rate, self.audio = wave.read(path)

    def encode(self, msg, output_path):
        msg = utility.msg_to_byte(msg)
        #print(msg)

        new_audio = np.copy(self.audio)
        
        if new_audio.shape[1] == 2:
            new_audio = self.encode_stereo(new_audio, msg)
        else:
            new_audio = self.encode_mono(new_audio, msg)

        wave.write(output_path, self.rate, new_audio)

    def encode_mono(self, audio, msg):
        if (len(msg)+len(msg)//self.ASCII_SIZE) > len(audio):
            print('Audio too small')

        i=0
        j=0
        while i < len(msg):
            if msg[i]=='0' and audio[j] % 2 != 0:
                audio[j] -= 1
            elif msg[i]=='1' and audio[j] % 2 == 0:
                audio[j] += 1

            i += 1
            j += 1
            
            if i<len(msg) and i%8==0 and audio[j]%2 != 0:
                audio[j] -= 1
            elif i==len(msg) and audio[j]%2 == 0:
                audio[j] += 1
            
            j += 1

        return audio

    def encode_stereo(self, audio, msg):
        if (len(msg)+len(msg)//self.ASCII_SIZE) > (2*len(audio)):    
            print('Audio too small')

        i=0
        j=0
        channel=0

        while i < len(msg):
            for x in msg[i]:
                if x=='0' and audio[j][channel] % 2 != 0:
                    audio[j][channel] -= 1    
                elif x=='1' and audio[j][channel] % 2 == 0:
                    audio[j][channel] += 1
                
                channel = (channel + 1) % 2
                    
                if channel==0:
                    j += 1

            i += 1

            if i<len(msg) and audio[j][channel]%2 != 0:
                audio[j][channel] -= 1
                
            elif i==len(msg) and audio[j][channel]%2 == 0:
                audio[j][channel] += 1

            channel = (channel + 1) % 2
            if channel==0:
                j += 1

        return audio

    def decode(self):
        new_audio = np.copy(self.audio)
        
        if len(new_audio.shape) == 2:
            msg = self.decode_stereo(new_audio)
        else:
            msg = self.decode_mono(new_audio)
        
        cprint(msg, 'yellow')
        
    def decode_mono(self, audio):
        msg = []

        i = 0
        while True:
            ascii_9_samples = [x for x in audio[i*9:(i+1)*9,1]]
            
            c = ''
            for sample in ascii_9_samples[:-1]:
                c += str(sample % 2)

            msg.append(c)
            i += 1

            if ascii_9_samples[-1] % 2 == 1:
                break

        #print(msg)
        return utility.byte_to_msg(msg)

    def decode_stereo(self, audio):
        msg = []
        i = 0
        j = 0
        channel = 0

        while True:
            ascii_9_samples = []
            while len(ascii_9_samples) < 9:
                ascii_9_samples.append(audio[j][channel])
                channel = (channel + 1) % 2
                
                if channel == 0:
                    j += 1

            c = ''
            for sample in ascii_9_samples[:-1]:
                c += str(sample % 2)
        
            msg.append(c)
            i += 1
            
            if ascii_9_samples[-1] % 2 == 1:
                break

        #print(msg)
        return utility.byte_to_msg(msg)