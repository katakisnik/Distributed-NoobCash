"""Implementing the mining process."""
import sys
import os
import json
import datetime
from random import randint
from signal import SIGTERM
from Crypto.Hash import SHA384
from . import nbcsettings, state, broadcast, consensus
from .block import Block
from threading import current_thread

def check():
    # Lock so only this thread can change variables here.
    with state.lock:
        # Check block capacity is ok and also no miner has already started
        if len(state.transactions) >= nbcsettings.BLOCK_CAPACITY:
            # Get the miner so that no thread can run at the same time
            state.MINER_RUNNING = True
            # Save thread
            state.thread_running = current_thread()
            if (start_mine()):
                # Set miner available again
                state.MINER_RUNNING = False
                return True
            else:
                # Set miner available again
                state.MINER_RUNNING = False
                return False
        else:
            return False

def start_mine():
    transactions = [tx.dump_sendable() for tx in state.transactions]
    b = {}
    b['transactions'] = transactions
    nonce = randint(0, nbcsettings.RAND)
    while True:
        b['nonce'] = nonce
        b['timestamp'] = str(datetime.datetime.now())
        b_json = json.dumps(b, sort_keys=True)
        sha = SHA384.new(b_json.encode()).hexdigest()
        if sha.startswith('0' * nbcsettings.DIFFICULTY):
            res = Block.create_block(state.transactions, b['nonce'], sha, b['timestamp'])
        #3ana3ekinaei?
            if res is None:
                print('block creation failed')
                return False

            broadcast.broadcast('receive_block', {
                'block': res.dump_sendable()
            })
            #consensus.consensus()
            return True
        nonce = randint(0, nbcsettings.RAND)
