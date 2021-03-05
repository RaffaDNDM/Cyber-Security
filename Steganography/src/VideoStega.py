from cv2 import cv2 as cv
from ImageStega import encode_msg, decode_msg
import utility
from PIL import Image
import numpy as np

class VideoStega:
    CHARS_IN_FRAME = 3
    END_SEQUENCE = 'ENDING'

    def __init__(self, path):
        self.video = cv.VideoCapture(path)
        self.fps = int(self.video.get(cv.CAP_PROP_FPS))
        self.width  = int(self.video.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.count = int(self.video.get(cv.CAP_PROP_FRAME_COUNT))

    def encode(self, msg, output_path):
        if (self.count-1)*4 >= len(msg):
            print('Video too short for encoding')

        success = True
        encode_check = True
        start = 0
        end = 0
        frames = []

        fourcc = cv.VideoWriter_fourcc(*'mp4v')        
        out = cv.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        while success:
            success, frame = self.video.read()
            
            if not success:
                continue

            if encode_check:
                end = start+self.CHARS_IN_FRAME if (start+self.CHARS_IN_FRAME)<=len(msg) else len(msg)
                print(frame.shape)
                frame = encode_msg(Image.fromarray(frame), msg[start:end])
                out.write(np.array(frame))
                start += (self.CHARS_IN_FRAME)

                if (end-start) != 1 and end == len(msg):
                    encode_check = False
                    success, frame = self.video.read()
                    if not success:
                        continue
    
                    frame = encode_msg(Image.fromarray(frame), self.END_SEQUENCE)
                    out.write(np.array(frame))

            else:
                out.write(frame)

    def decode(self):
        success = True
        msg = ''
        while success:
            success, frame = self.video.read()
            if not success:
                continue
            
            msg_frame = decode_msg(Image.fromarray(frame))

            if msg_frame == self.END_SEQUENCE:
                success = False
            else:
                msg += msg_frame

        print(msg)
                           
            
def main():
    #video_st = VideoStega('../dat/video.mp4')
    #video_st.encode('Hello RaffaDNDM!', '../dat/encoded_video.mp4')
    video_st = VideoStega('../dat/encoded_video.mp4')
    video_st.decode()

if __name__=='__main__':
    main()