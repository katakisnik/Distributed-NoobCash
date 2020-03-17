import datetime

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
