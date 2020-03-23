import datetime
import copy
import json
from . import state, nbcsettings
from .transaction import Transaction

from Crypto.Hash import SHA384


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

    # equality check
    def __eq__(self, value):
        if not isinstance(value, Block):
            return False
        if (self.transactions == value.transactions and self.nonce == value.nonce and self.current_hash == value.current_hash and self.previous_hash == value.previous_hash):
            return True
        else:
            return False

    # json dump to create has
    def dump(self):
        return json.dumps(dict(
            transactions=self.transactions,
            nonce=self.nonce,
            timestamp=self.timestamp
        ))

    # hash calculation
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

    def dict(self):
        return dict(
            timestamp=self.timestamp,
            transactions=self.transactions,
            nonce=self.nonce,
            current_hash=self.current_hash,
            previous_hash=self.previous_hash
        )

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
            if len(block.transactions) != nbcsettings.BLOCK_CAPACITY:
                raise Exception('invalid block capacity')
         #   print(block.current_hash)
          #  print('\n')
           # print(block.calculate_hash().hexdigest())
            #if block.current_hash != block.calculate_hash().hexdigest():
         #       raise Exception('invalid hash')
            if not block.current_hash.startswith('0'*nbcsettings.DIFFICULTY):
                raise Exception('invalid proof of work')

            #we are starting from the utxos of the last block
            state.utxos = copy.deepcopy(state.valid_utxos)
            state.transactions = []

            for tx in transactions:
                #needs to be implemented
                result, transaction = Transaction.validate_transaction(tx)
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
    def create_genesis_block(num_participants):
        try:
            flag = Transaction.create_first_transaction(num_participants)
            if not flag:
                raise Exception('could not create genesis transaction')
            print('first transaction created')
            transactions = []
            print(state.transactions)
            for tx in state.transactions:
                print(tx)
                transactions.append(tx.dump_sendable())
            print('transactions loaded')
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
            print('everything fine')
            return True
        
        except Exception as e:
            print(e)

    @staticmethod
    def validate_block(block_json):
        try:
            # save state, in order to properly restore in case of a bad block
            TRANSACTIONS_BACKUP = copy.deepcopy(state.transactions)
            UTXOS_BACKUP = copy.deepcopy(state.utxos)
            BLOCKCHAIN_BACKUP = copy.deepcopy(state.blockchain)
            VALID_UTXOS_BACKUP = copy.deepcopy(state.valid_utxos)

            previous_block = state.blockchain[-1]
            new_index = previous_block.index + 1
            new_block = Block(**json.loads(block_json), index=new_index)

           # if new_block.calculate_hash().hexdigest() != new_block.current_hash:
            #    raise Exception('invalid has')
            if len(new_block.transactions) != nbcsettings.BLOCK_CAPACITY:
                raise Exception('invalid block capacity')
            if not new_block.current_hash.startswith('0'*nbcsettings.DIFFICULTY):
                raise Exception('invalid proof of work')

            if new_block.previous_hash == previous_block.current_hash:

                state.utxos = copy.deepcopy(state.valid_utxos)
                state.transactions = []

                for tx in new_block.transactions:
                    result, transaction = Transaction.validate_transaction(tx)
                    if result == False:
                        raise Exception('invalid transaction')
                    #remove transaction after validating    
                    state.transactions.remove(transaction)

                state.blockchain.append(new_block)
                state.valid_utxos = copy.deepcopy(state.utxos)

                return 'good'    

            else:
                for block in state.blockchain[:-1]:
                    if block.current_hash == new_block.previous_hash:
                        #the parent of our new block is a previous block so a smaller chain is produced
                        return 'dropped'
                #unkown block
                return 'consensus'
        
        except Exception as e:
            #restore state
            state.transactions = TRANSACTIONS_BACKUP
            state.blockchain = BLOCKCHAIN_BACKUP
            state.utxos = UTXOS_BACKUP
            state.valid_utxos = VALID_UTXOS_BACKUP

            print(e)
            return 'error'
