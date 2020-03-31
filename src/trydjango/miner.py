"""Implementing the mining process."""
import sys
import os
import django
import requests
import json
import datetime
from random import randint
from signal import SIGTERM
from Crypto.Hash import SHA384
from subprocess import Popen
from . import nbcsettings, state, broadcast, consensus

################################################################################

# # Set up django
# BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(BASE)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trydjango.settings')
# django.setup()


################################################################################

def check():
    """
    Checks block details and start mining.
    This is the function that should be used in the main program.
    """
    # Check block capacity is ok and also no miner has already started
    if len(state.transactions) >= nbcsettings.BLOCK_CAPACITY:
        # Check if no miner runs already. Then start if needed
        start()
        return True
    return False

def stop():
    """Manually stop a process."""
    try:
        if state.miner_pid is not None:
            print('Killing miner: PID', state.miner_pid)
            os.kill(state.miner_pid, SIGTERM)
            state.miner_pid = None
    except OSError as e:
        if e.errno != os.errno.ESRCH:
            print(f'miner.stop: {e.errno}: {e}')
    except Exception as e:
        print(f'miner.stop: {e.__class__.__name__}: {e}')

# def start_mine():
#     """Find nonce and send API back to the main process."""
#     transactions = [tx.dump_sendable() for tx in state.transactions]
#     b = {}
#     b['transactions'] = transactions
#     nonce = randint(0, nbcsettings.RAND)
#     # Create API
#     host = state.participants[state.publickey]['host']
#     API = f'{host}/create_block/'
#     while True:
#         b['nonce'] = nonce
#         b['timestamp'] = str(datetime.datetime.now())
#         b_json = json.dumps(b, sort_keys=True)
#         sha = SHA384.new(b_json.encode()).hexdigest()
#         if sha.startswith('0' * nbcsettings.DIFFICULTY):
#             # Send API to process that we forked from
#             block_details = {
#                 'transactions': b['transactions'],
#                 'nonce': b['nonce'],
#                 'sha': sha,
#                 'timestamp': b['timestamp']
#             }
#             requests.post(API, block_details)
#             exit(0)
#         # Continue until you compute nonce
#         nonce = randint(0, nbcsettings.RAND)


def start():
    """
    Find out if a miner is already running.
    If no one is running, then start one.
    """
    try:
        os.kill(state.miner_pid, 0)
        print(f'Miner already running with PID:{state.miner_pid}\n')

    except Exception as e:
        host = state.participants[state.publickey]['host']
        transactions = [tx.dump_sendable() for tx in state.transactions]
        # No miner has been started yet
        print('Starting miner')
        proc = Popen(['python', 'mineprocess.py', host, json.dumps(transactions), nbcsettings.DIFFICULTY])
        state.miner_pid = proc.pid
        print(f'miner.start: {e.__class__.__name__}: {e}')

# if __name__ == '__main__':
#     """If we run main then start_mine should be initialized."""
#     start_mine()
