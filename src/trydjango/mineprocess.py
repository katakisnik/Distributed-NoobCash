import sys
from random import randint
import datetime
import json
import requests

from Crypto.Hash import SHA384


def start_mine(host, transactions, difficulty):
    """Find nonce and send API back to the main process."""
    try:
        transactions = transactions
        b = {}
        b['transactions'] = transactions
        nonce = randint(0, 1000000)
        # Create API
        API = f'{host}/send_block/'
        while True:
            b['nonce'] = nonce
            b['timestamp'] = str(datetime.datetime.now())
            b_json = json.dumps(b, sort_keys=True)
            sha = SHA384.new(b_json.encode()).hexdigest()
            if sha.startswith('0' * int(difficulty)):
                # Send API to process that we forked from
                block_details = {
                    'transactions': b['transactions'],
                    'nonce': b['nonce'],
                    'sha': sha,
                    'timestamp': b['timestamp']
                }
                requests.post(API, block_details)
                exit(0)
            # Continue until you compute nonce
            nonce = randint(0, 1000000)
    except Exception as e:
        with open('error.txt',mode='w') as f:
            f.write(e)


if __name__ == '__main__':
    """If we run main then start_mine should be initialized."""
    start_mine(sys.argv[1], sys.argv[2], sys.argv[3])
