# Steganography
A secret message can be hidden in a file using one of the following steganography methods:
<details><summary><b><i>Image Steganography</i></b></summary>
LSB approach by mapping each ASCII character (1 byte) into 3 pixels. Each bit of the ASCII character will modify the LSB bit of each RGB component value of the 3 pixels. The LSB of the 3rd component value of the last pixel will be <i>1</i> (odd number) if the message to be hidden is over, <i>0</i> otherwise (even number).
</details>
<details><summary><b><i>Audio Steganography</i></b></summary>
LSB approach by mapping each ASCII character (1 byte) into 9 samples of the audio file. Each bit of the ASCII character will modify the LSB bit of each sample. The LSB of the 9th sample will be <i>1</i> (odd number) if the message to be hidden is over, <i>0</i> otherwise (even number).
</details>
To run the program, you need to install the following dependencies:
```
pip3 install argparse termcolor numpy scipy pillow
```
