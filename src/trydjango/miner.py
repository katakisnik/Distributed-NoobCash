"""Implementing the mining process."""
import sys
import os
import json
import datetime
from random import randint
from subprocess import Popen
from signal import SIGTERM
from Crypto.Hash import SHA384
from . import nbcsettings, state, broadcast
from .block import Block

def check():
    if len(state.transactions) == nbcsettings.BLOCK_CAPACITY:
        if (start_mine()):
            return True
        else:
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
            res = Block.create_block(b['transactions'], b['nonce'], sha, b['timestamp'])
        #3ana3ekinaei?
            if res is None:
                print('block creation failed')
                return False

            broadcast.broadcast('receive_block', {
                'block': res.dump_sendable()
            })

            return True
        nonce = randint(0, nbcsettings.RAND)

# def start():
#     """Running a subprocess for mining"""
#     host = state.participants[state.publickey]['host']
#     transactions = [t.dump_sendable() for t in
#                     state.transactions[:nbcsettings.BLOCK_CAPACITY]]

#     try:
#         # if already running or None
#         os.kill(state.miner_pid)
#         print(f'Miner running already: PID={state.miner_pid}')
#     except Exception as e:
#         # Start miner
#         try:
#             process = Popen(nbcsettings.PYTHON_VERSION, __file__,
#                             host, json.dumps(transactions),
#                             state.token)
#             state.miner_pid = process.pid
#         except Exception as e:
#             print(e)


# def stop():
#     if state.miner_pid is not None:
#         try:
#             os.kill(state.miner_pid, SIGTERM)
#             state.miner_pid = None
#             print(f'Killing miner with PID:{state.miner_pid}')
#         except Exception as e:
#             print(e)


# def mine(host, transactions_json, token):
#     """Calculates the nonce."""
#     transactions = json.loads(transactions_json)
#     # Check transactions lenght
#     if len(transactions) != nbcsettings.BLOCK_CAPACITY:
#         raise NameError('Block incorrect size')



# if __name__ == '__main__':
#     # This section should run if miner.py is called
#     # by a process
#     mine(sys.argv[1], sys.argv[2], sys.argv[3])
