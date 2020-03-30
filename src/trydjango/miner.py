"""Implementing the mining process."""
import sys
import os
import json
import datetime
from random import randint
from subprocess import Popen
from signal import SIGTERM
from Crypto.Hash import SHA384
from . import nbcsettings, state, broadcast, consensus
from .block import Block

def check():
    if len(state.transactions) >= nbcsettings.BLOCK_CAPACITY:
        if (start_mine()):
            return True
        else:
            return False
    else:
        return False

def start_mine():
    transactions = state.transactions
    b = {}
    b['transactions'] = transactions
    nonce = randint(0, nbcsettings.RAND)
    while True:
        b['nonce'] = nonce
        b['timestamp'] = str(datetime.datetime.now())
        b_json = json.dumps(b, sort_keys=True)
        sha = SHA384.new(b_json.encode()).hexdigest()
        if sha.startswith('0' * nbcsettings.DIFFICULTY):
            res = Block.create_block(b['transactions'], b['nonce'], sha, b['timestamp'])
        #3ana3ekinaei?
            if res is None:
                print('block creation failed')
                return False

            broadcast.broadcast('receive_block', {
                'block': res.dump_sendable()
            })
            consensus.consensus()
            return True
        nonce = randint(0, nbcsettings.RAND)
