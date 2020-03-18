import datetime
import json
import state
import settings
from transaction import Transaction

from Cypto.Hash import SHA384

class Block(object):

    # constructor
    def __init__(self, transactions, nonce, current_hash, previous_hash, index, timestamp=None):
        self.transactions = transactions
        self.nonce = nonce
        self.current_hash = current_hash
        self.previous_hash = previous_hash

        self.index = index
        self.timestamp = timestamp
        if timestamp is None:
            self.timestamp = str(datetime.datetime.now())

    #equality check
    def __eq__(self, value):
        if not isinstance(value, Block):
            return False
        if (self.transactions == value.transactions and self.nonce == value.nonce and self.current_hash == value.current_hash and self.previous_hash == value.previous_hash):
            return True
        else:
            return False

    #json dump to create has
    def dump(self):
        return json.dumps(dict(
            transactions = self.transactions,
            nonce = self.nonce,
            timestamp = self.timestamp
        ))

    #hash calculation
    def calculate_hash(self):
        return SHA384.new(self.dump().encode())

    def dump_sendable(self):
        ''' sendable json string '''
        return json.dumps(dict(
            timestamp=self.timestamp,
            transactions=self.transactions,
            nonce=self.nonce,
            current_hash=self.current_hash,
            previous_hash=self.previous_hash
        ), sort_keys=True)

    #create a block, the miner has found nonce for the list of transactions
    @staticmethod
    def create_block(transactions, nonce, newhash, timestamp):
        try:
            block = Block(
                transactions = copy.deepcopy(transactions),
                nonce = nonce,
                current_hash = newhash,
                previous_hash = state.blockchain[-1].current_hash,
                index = len(state.blockchain),
                timestamp = timestamp
            )

            #check if the created block is valid
            if len(block.transactions) != settings.BLOCK_CAPACITY:
                raise Exception('invalid block capacity')
            if block.current_hash != block.calculate_hash():
                raise Exception('invalid hash')
            if block.current_hash.startswith('0'*settings.DIFFICULTY):
                raise Exception('invalid proof of work')
            
            #we are starting from the utxos of the last block
            state.utxos = copy.deepcopy(state.valid_utxos)
            state.transactions = []

            for tx in transactions:
                #needs to be implemented
                result = Transaction.validate(tx)
                if result == False:
                    raise Exception('invalid transaction')
            
            state.transactions = []

            #block added to blockchain
            state.blockchain.append(block)
            state.valid_utxos = copy.deepcopy(state.utxos)

            return block
        
        except Exception as e:
            print(e)
            
        @staticmethod
        def create_genesis_block():
            try:
                flag = Transaction.create_first_transaction()
                if not flag:
                    raise Exception('could not create genesis transaction')
                
                transactions = []
                for tx in state.transactions:
                    transactions.append(tx.dump_sendable())

                block = Block(
                    transactions=transactions,
                    nonce = 0,
                    current_hash = 'genesis',
                    previous_hash = 1,
                    index = 0
                )

                block.current_hash = block.calculate_hash().hexdigest()
                state.blockchain = [block]
                state.transactions = []
                state.valid_utxos = copy.deepcopy(state.utxos)
                state.genesis_block = Block(**json.loads(block.dump_sendable()), index=0)
                state.genesis_utxos = copy.deepcopy(state.utxos)

                return True
            
            except Exception as e:
                print(e)