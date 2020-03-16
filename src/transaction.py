import state
import copy

class Transaction(object):

    #constructor
    def __init__(self, sender, receiver, amount, id, inputs, signature):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.id = id
        self.inputs = inputs
        self.signature = signature
        self.outputs = []

    #compare
    def __eq__(self, value):
        if not isinstance(value, Transaction):
            return False
        if (self.sender == value.sender and self.receiver == value.receiver and self.amount == value.amount and self.id == value.id and self.inputs == value.inputs and self.signature == value.signature):
            return True

    @staticmethod
    def create_transaction(receiver, amount):
        try:
            sender = state.publickey
            sender_utxos = copy.deepcopy(state.utxos[sender]) 
            receiver_utxos = copy.deepcopy(state.utxos[receiver])

            #id for each transaction that led to the money that are being transfered
            inputs = []
            for tr in sender_utxos:
                inputs.append(tr['id'])
        
        except Exception as e:
            print(e)
            return None
