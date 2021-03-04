from scipy.io import wavfile as wave
import numpy as np

class AudioStega:
    def __init__(self, path):
        rate, self.audio = wave.read(path)


    def msg_to_byte(self, msg):
        encoded_msg = []
  
        for x in msg:
            encoded_msg.append(format(ord(x), '08b'))

        return encoded_msg

    def byte_to_msg(self, msg):
        decoded_msg = ''
        for x in msg:
            decoded_msg+=chr(int(x, 2))

        return decoded_msg

    def encode(self, msg, output_path):
        self.encode_msg(msg)
        #new_img.save(output_path, 'PNG')

    '''
    def decode(self):
        msg = self.decode_msg()
        print(msg)

    def decode_msg(self):
        data = iter(img.getdata())
        
        msg = []
        while True:
            #Tuple to list of components of the next 3 pixels
            pixels_RGB = [value for value in data.__next__()[:3] + 
                                             data.__next__()[:3] + 
                                             data.__next__()[:3]]

            print(pixels_RGB)
            c = ''
            for x in pixels_RGB[:-1]:
                c += format(x, '08b')[-1]
            
            msg.append(c)

            #Stop reading (1)
            if pixels_RGB[-1]%2 == 1:
                break

        return self.byte_to_msg(msg)
    '''

    def encode_msg(self, msg):
        msg = self.msg_to_byte(msg)
        print(msg)
        new_audio = np.copy(self.audio)

        for sample in new_audio:
            print(type(sample))

def main():
    audio_st = AudioStega('dat/audio.mp3')
    audio_st.encode('Hello', 'dat/encoded_audio.wav')
    #audio_st.decode()

if __name__=='__main__':
    main()