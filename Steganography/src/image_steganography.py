from PIL import Image
import utility
from termcolor import cprint

class ImageSteganography:
    def __init__(self, path):
        self.IMG = Image.open(path, 'r')

    def encode(self, msg, output_path):
        new_img = self.IMG.copy()
        new_img = self.encode_msg(new_img, msg)
        new_img.save(output_path, 'PNG')

    def encode_msg(self, img, msg):
        msg = utility.msg_to_byte(msg)
        #print(msg)

        data = iter(img.getdata())
        width = img.size[0]
        height = img.size[1]
        
        if height*width*3 < len(msg):
            raise Exception
        
        i=0
        x=0
        y=0

        while i < len(msg):
            #Tuple to list of components of the next 3 pixels
            pixels_RGB = [value for value in data.__next__()[:3] + 
                                                data.__next__()[:3] +
                                                data.__next__()[:3]]
            #print(pixels_RGB, end=' ')
            for j in range(0, 8):
                pixels_RGB[j] = int(format(pixels_RGB[j], '08b')[:-1]+msg[i][j], 2)
            
            #print(pixels_RGB)

            i+=1

            #Stop reading (1)
            if i == len(msg):
                pixels_RGB[-1]= int(format(pixels_RGB[j], '08b')[:-1]+'1', 2)
            #Keep reading (0)
            else:
                pixels_RGB[-1]= int(format(pixels_RGB[j], '08b')[:-1]+'0', 2)

            pixels_RGB = tuple(pixels_RGB)

            for j in range(3):
                img.putpixel((x, y), pixels_RGB[j*3:(j+1)*3])
                x = (x+1) % width

                if x == 0:
                    y += 1

        return img

    def decode(self):
        msg = self.decode_msg(self.IMG)
        cprint(msg,'yellow')

    def decode_msg(self, img):
        data = iter(img.getdata())
        
        msg = []
        while True:
            #Tuple to list of components of the next 3 pixels
            pixels_RGB = [value for value in data.__next__()[:3] + 
                                                data.__next__()[:3] + 
                                                data.__next__()[:3]]

            #print(pixels_RGB)
            c = ''
            for x in pixels_RGB[:-1]:
                c += format(x, '08b')[-1]
            
            msg.append(c)

            #Stop reading (1)
            if pixels_RGB[-1]%2 == 1:
                break

        return utility.byte_to_msg(msg)