"""Implementing the mining process."""
import sys
import os
import json
from subprocess import Popen
import nbcsettings
import state

def start():
    """Running a subprocess for mining"""
    host = state.participants[state.publickey]['host']
    transactions = [t.dump_sendable() for t in
                    state.transactions[:nbcsettings.BLOCK_CAPACITY]]

    try:
        # if already running or None
        os.kill(state.miner_pid)
        print(f'Miner running already: PID={state.miner_pid}')
    except Exception as e:
        # Start miner
        try:
            process = Popen(nbcsettings.PYTHON_VERSION, __file__,
                            host, json.dumps(transactions),
                            state.token)
            state.miner_pid = process.pid
        except Exception as e:
            print(e)


def mine(host, transactions_json, token):
    """Calculates the nonce."""
    transactions = json.loads(transactions_json)
    # Check transactions lenght
    if len(transactions) != nbcsettings.BLOCK_CAPACITY:
        raise NameError('Block incorrect size')



if __name__ == '__main__':
    # This section should run if miner.py is called
    # by a process
    mine(sys.argv[1], sys.argv[2], sys.argv[3])
