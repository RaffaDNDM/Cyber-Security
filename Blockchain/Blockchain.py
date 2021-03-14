import random
from termcolor import cprint, colored
import colorama
from hashlib import sha256
import json

class Transaction:
    '''
    Digital transaction.

    Args:
        src (str): Name of the sender of money

        dst (str): Name of the receiver of money

        amount (float): Amount of money exchanged

    Attributes:
        src (str): Name of the sender of money

        dst (str): Name of the receiver of money

        amount (float): Amount of money exchanged
    '''

    def __init__(self, src: str, dst: str, amount: float):
        self.src = src
        self.dst = dst
        self.amount = amount


    def __repr__(self):
        '''
        Serialize the instance

        Returns:
            result (str): Serialization string.
        '''

        return json.dumps(self.__dict__)


class Block:
    '''
    Block of the blockchain.

    Args:
        prev_hash (str): Hash of the previous block in the blockchain

        transactions (list): List of Transaction objects to be encapsulated
                             in the current block

    Attributes:
        prev_hash (str): Hash of the previous block in the blockchain

        transactions (list): List of Transaction objects to be encapsulated
                             in the current block
    '''
    
    def __init__(self, prev_hash: str, transactions: list):
        self.prev_hash = prev_hash
        self.transactions = transactions


    def encode_b(self,obj):
        '''
        Obtain object from the object to be serialized.

        Args:
            obj (obj): Object to be serialized.

        Returns:
            result (obj): Object to be serialized by json.dumps
        '''

        if isinstance(obj, Transaction):
            return obj.__dict__
        return obj


    def compute_hash(self):
        '''
        Compute hash of a block.

        Returns:
            block_hash (str): Hexadecimal hash string, computed using SHA256
        '''

        #Serialize the block content
        block_string = json.dumps(self.__dict__, sort_keys=True, default=self.encode_b)

        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    '''
    Blockchain.

    Attributes:
        BLOCKCHAIN_LIST (list): List of all the blocks in the Blockchain.
    '''

    BLOCKCHAIN_LIST = []

    def __init__(self):
        self.first_block()

    def first_block(self):
        '''
        Create the first genesis block and add it to the blockchain.
        '''

        #Create prev_hash of the first block as a random 64 hexadecimal characters
        hex_chars = '0123456789abcdef'
        prev_hash = ''.join([random.choice(hex_chars) for _ in range(64)])
        #No transactions
        transactions = None
        #Append the first block to the blockchain
        self.BLOCKCHAIN_LIST.append(Block(prev_hash, transactions))

    def add_block(self, transactions: list):
        '''
        Create the block with specified transactions 
        and add it to the blockchain.

        Args:
            transactions (list): List of Transaction objects
        '''

        prev_hash = self.BLOCKCHAIN_LIST[-1].compute_hash()
        b = Block(prev_hash, transactions)
        self.BLOCKCHAIN_LIST.append(b)

    def info(self):
        '''
        Print the content of the blockchain.
        '''

        cprint('\nBlockchain information', 'blue')
        cprint('___________________________________________________________', 'blue')
        
        if len(self.BLOCKCHAIN_LIST) - 1 == 0:
            cprint('[Empty Blockchain]', 'red', end='\n\n')
        else:
            count_block = 1

            for block in self.BLOCKCHAIN_LIST[1:]:
                cprint(f'[{count_block} BLOCK]', 'red', end=' ')
                cprint('-> Hash:', 'yellow', end=' ')
                print(block.compute_hash())
                cprint(f'> Prev block Hash:', 'blue', end=' ')
                print(block.prev_hash)
                
                cprint('> Transactions', 'green')
                count_transaction = 1
                
                for t in block.transactions:
                    print(colored(f'  {count_transaction}) ', 'green'),f'{t.src} -> {t.dst}: {t.amount}')
                    count_transaction += 1

                if count_block != len(self.BLOCKCHAIN_LIST)-1:
                    print('')
                    
                count_block += 1

        cprint('___________________________________________________________', 'blue', end='\n\n')


def main():
    #Colored text
    colorama.init()
    #Create the blockchain
    chain = Blockchain()
    run_check = True

    #Read input transactions of the user
    while run_check:
        cprint('Insert the transaction you want to register', 'blue')
        cprint('(Q to exit and END to submit the transactions in a block):', 'blue')
        cprint('___________________________________________________________', 'blue')
        cprint('Example format: Alice -> Bob : 10.0', 'blue', end='\n\n')

        #Transactions to be inserted in a block
        transactions = []
        submit_check = True

        while submit_check:
            #Read the transaction from the user
            t = input()

            if t.lower() == 'end':
                #Upload all the last input transictions into a block
                submit_check = False
            elif t.lower() == 'q':
                #Upload all the last input transictions into a block
                #and terminate the program
                submit_check = False
                run_check = False
            else:
                #Sender of the money
                src, t2 = t.split(' -> ')
                #Receiver of the specified amount of money
                dst, amount = t2.split(' : ')
                #Add the transaction to the list of transactions
                #that will be uploaded into the block
                transactions.append(Transaction(src, dst, float(amount)))

        cprint('___________________________________________________________', 'blue')

        if transactions:
            #Create a new block and add it to the blockchain
            chain.add_block(transactions)
    
    #Display the content of the blockchain
    chain.info()
    print('Exit from the program...', end='\n\n')


if __name__=='__main__':
    main()