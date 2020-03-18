import state
import copy
import json
from Crypto.Hash import SHA256

class Transaction(object):

    #constructor
    def __init__(self, sender, receiver, amount, inputs, id=None, signature=None):
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

    def dump(self):
        '''convert transaction to string'''
        return json.dumps(dict(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
            inputs=self.inputs,
            ), sort_keys=True)

    def calculate_hash(self):
        # Convert object to string
        transaction_to_string = self.dump()
        # Hash string
        return SHA256.new(transaction_to_string.encode())

    #in sign the id and the signature of the transaction are created
    def sign(self):
        # Calculate hash
        hash = self.calculate_hash()
        self.signature = hash
        pass


    @staticmethod
    def create_transaction(receiver, amount):
        try:
            # Sender creates this transaction, at that time state.publickey is his pk
            sender = state.publickey
            sender_utxos = copy.deepcopy(state.utxos[sender])
            receiver_utxos = copy.deepcopy(state.utxos[receiver])

            # id for each transaction that led to the money that are being transfered
            inputs = []
            for tr in sender_utxos:
                inputs.append(tr['id'])

            # available money of the sender
            sender_money = [t_utxo['amount'] for t_utxo in sender_utxos if t_utxo['who'] == sender ]
            # Check if the available money is enough
            if sender_money < amount :
                raise Exception(f'User with PublicKey({sender}) has not enough money')

            # Create the transaction
            t = Transaction(sender,receiver,amount, inputs)
            t.sign()
            # Each transactions have
            # utxos[pubkey] = [{transaction_id, who, amount}]

            #create outputs
            t.outputs = [{
                'id': t.id,
                'who': t.sender,
                'amount': sender_money - amount
            }, {
                'id': t.id,
                'who': t.receiver,
                'amount': amount
            }]

            #save transaction
            state.transactions.append(t)

            #update the utxos
            state.utxos[sender] = [t.outputs[0]]
            state.utxos[receiver].append(t.outputs[1])
        
            return t

        except Exception as e:
            print(e)
            return None

    
    #the genesis transactions that happens as a participant enters the system
    @staticmethod
    def create_first_transaction():
        try:
            #each participant has 100NBC in his wallet at the start
            t = Transaction(state.publickey, state.publickey, 100, [])
            t.sign()

            t.outputs = [{
                'id': t.id,
                'who': t.sender,
                'amount': t.amount
            }]

            state.utxos[state.publickey] = [t.outputs[0]]
            state.transactions.append(t)

            return t
        
        except Exception as e:
            print(e)