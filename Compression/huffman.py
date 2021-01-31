import operator
import bitarray
import os
import sys
import argparse

class TreeNode:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

def insertion(list_freq, new_label, new_freq):

    for index in range(0, len(list_freq)):
        (label, freq) = list_freq[index]

        if freq < new_freq:
            list_freq.insert(index, (new_label, new_freq))        
            return

    #New frequency in the last element
    list_freq.append((new_label, new_freq))

class HuffmanTree:
    def __init__(self, freq_dict):
        self.freq_dict = dict(sorted(freq_dict.items(),
                                  key=operator.itemgetter(1),
                                  reverse=True))
        
        self.huffman_code = {k:'' for k in list(self.freq_dict.keys())}
        self.nodes = {}
        self.root_label = ''
        self.create_tree(self.freq_dict.copy())

    def create_tree(self, freq_dict):
        list_freq = list(freq_dict.items())
        
        while len(list_freq) > 1:
            (label_L, freq_L) = list_freq[-2]
            (label_R, freq_R) = list_freq[-1]
            self.update_huffman(label_L, label_R)
            
            left = label_L
      
            if label_L in list(self.nodes.keys()):
                left = self.nodes[label_L]

            right = label_R
      
            if label_R in list(self.nodes.keys()):
                right = self.nodes[label_R]
            
            list_freq = list_freq[:-2]
            new_freq = freq_L + freq_R
            new_label = label_L + label_R
            self.nodes[new_label]=TreeNode(left, right)
            self.root_label = new_label
            insertion(list_freq, new_label, new_freq)

    def update_huffman(self, label_L, label_R):
        for x in label_L:
            self.huffman_code[x] = '0'+ self.huffman_code[x]

        for x in label_R:
            self.huffman_code[x] = '1'+ self.huffman_code[x]

    def table(self):
        return {k:bitarray.bitarray(v) for (k, v) in list(self.huffman_code.items())}

    def encode(self, text):
        encoded_str = ''
        
        for x in text:
            encoded_str += self.huffman_code[x]

        return encoded_str

    def decode(self, text):
        decoded_str = ''

        node = self.nodes[self.root_label]
        
        for x in text:
            
            if x=='0':
                node = node.left
            elif x=='1':
                node = node.right
            else:
                print('Not Huffman encoded')

            if type(node)==str:
                decoded_str += node
                node = self.nodes[self.root_label]

        return decoded_str

def create_dict(text):
    freq_dict = {}
    
    for x in text:
        if x in list(freq_dict.keys()):
            freq_dict[x] += 1
        else:
            freq_dict[x] = 1

    return freq_dict

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    #Initialization of needed arguments
    parser.add_argument("-file", "-f", dest="file", help="Path of the file to be encrypted")
    #Parse command line arguments
    args = parser.parse_args()
    
    return args.file

def main():
    file_path = args_parser()
    text = ''

    if file_path:
        if not(os.path.exists(file_path) and os.path.isfile(file_path)):
            print('[ERROR] File not found')

        with open(file_path, 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    tree = HuffmanTree(create_dict(text))
    encoded_str = tree.encode(text)
    print(encoded_str)
    decoded_str = tree.decode(encoded_str)
    print(decoded_str)

main()