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
        FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'mineprocess.py')
        proc = Popen(['python', FILE_PATH, host, json.dumps(transactions[:nbcsettings.BLOCK_CAPACITY]), str(nbcsettings.DIFFICULTY)])
        state.miner_pid = proc.pid

