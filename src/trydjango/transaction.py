import copy
import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from . import state


class Transaction(object):

    # constructor
    def __init__(self, sender, receiver, amount, inputs, id=None, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.id = id
        self.inputs = inputs
        self.signature = signature
        self.outputs = []

    # compare
    def __eq__(self, value):
        if not isinstance(value, Transaction):
            return False
        if (self.sender == value.sender and self.receiver == value.receiver and
           self.amount == value.amount and self.id == value.id and
           self.inputs == value.inputs and self.signature == value.signature):
            return True
        else:
            return False

    def dump_sendable(self):
        '''convert to sendable json string'''
        return json.dumps(dict(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
            inputs=self.inputs,
            id=self.id,
           signature=self.signature
        ), sort_keys=True)

    def dump(self):
        '''convert transaction to string'''
        return json.dumps(dict(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
            inputs=self.inputs,
            ), sort_keys=True)

    def dict(self):
        '''convert to dict'''
        return dict(
            sender=self.sender,
            receiver=self.receiver,
            amount=self.amount,
            inputs=self.inputs,
            id=self.id,
            signature=self.signature
        )

    def calculate_hash(self):
        # Convert object to string
        transaction_to_string = self.dump()
        # Hash string
        return SHA256.new(transaction_to_string.encode())

    def sign(self):
        '''Creates the id and the signature of the transaction'''

        # Calculate hash - hash compresses the string
        hash = self.calculate_hash()

        # Now sign using the private key
        key = RSA.importKey(state.privatekey)
        # Create the signer using his private key
        signer = PKCS1_v1_5.new(key)
        # Now sign the transaction (hashed/compressed)
        self.signature = base64.b64encode(signer.sign(hash)).decode()

        # id is the hex of the hashed transaction
        # returns a HEX string representing the hash
        self.id = hash.hexdigest()

        return self.signature

    def verify_signature(self):
        '''Verifies the signature of a transaction.
           If the signature is verified returns True.
           Otherwise returns False'''
        # Set the signature
        signature = self.signature
        # Get the public key
        pub_key = self.sender
        # import to RSA
        key = RSA.importKey(pub_key.encode())
        # Create the verifier (same as signer)
        verifier = PKCS1_v1_5.new(key)
        # Get the transaction hash
        hash = self.calculate_hash()
        # Verify the signature
        if verifier.verify(hash, signature):
            return True
        return False


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
            if sum(sender_money) < amount :
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
                'amount': sum(sender_money) - amount
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
    def create_first_transaction(num_participants):
        try:
            # each participant has 100NBC in his wallet at the start
            t = Transaction(state.publickey, state.publickey, 100*num_participants, [])
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

    @staticmethod
    def validate_transaction(transaction_json):
        try:
            t = Transaction(**json.loads(transaction_json))

            if t in state.transactions:
                return False, t

            if t.id != t.calculate_hash().hexdigest():
                raise Exception('invalid hash')

            #if not t.verify_signature():
            #   raise Exception('invalid signature')

            # verify that inputs are utxos
            sender_utxos = copy.deepcopy(state.utxos[t.sender])
            budget = 0
            for txin_id in t.inputs:
                found = False
                for utxo in sender_utxos:
                    if utxo['id'] == txin_id and utxo['who'] == t.sender:
                        found = True
                        budget += utxo['amount']
                        sender_utxos.remove(utxo)
                        break

                if not found:
                    raise Exception('missing inputs')

            if budget < t.amount:
                raise Exception('not enough money')

            # create outputs
            t.outputs = [{
                'id': t.id,
                'who': t.sender,
                'amount': budget - t.amount
            }, {
                'id': t.id,
                'who': t.receiver,
                'amount': t.amount
            }]

            # update utxos
            sender_utxos.append(t.outputs[0])
            state.utxos[t.sender] = sender_utxos
            state.utxos[t.receiver].append(t.outputs[1])
            state.transactions.append(t)

            return True, t

        except Exception as e:
            print(e)
            return False, None
