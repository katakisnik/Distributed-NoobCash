import state
import copy

class Transaction(object):

    #constructor
    def __init__(self, sender, receiver, amount, id, inputs=None, signature=None):
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

    def sign(self):
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
            t = Transaction(sender,receiver,amount,id=new_id,inputs=inputs)
            t.sign()
            # Each transactions have
            # utxos[pubkey] = [{transaction_id, who, amount}]

        except Exception as e:
            print(e)
            return None
