from . import state

from Crypto.PublicKey import RSA
from Crypto.Hash import SHA384

#function too create the public and private key of each participant and also the token for the transactions
def keygenerator():
    if state.privatekey == None and state.publickey == None:
        return

    keypair = RSA.generate(2048)
    state.privatekey = keypair.exportKey('PEM').decode()
    state.publickey = keypair.publickey().exportKey('PEM').decode()

    state.token = SHA384.new(state.privatekey[::2].encode()).hexdigest()
