"""Implements a basic client """
import sys
import os
import argparse
import requests
import datetime

from trydjango.nbcsettings import SOURCE_INPUTS_PATH

# arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument('host', type=str)
parser.add_argument('port', type=int)
parser.add_argument('num_participants')
args = parser.parse_args()

coordinatorhost = f'http://192.168.1.5:8000'
host = f'http://{args.host}:{args.port}'
participants = int(args.num_participants)

api = f'{coordinatorhost}/create_coordinator/'

if participants == 0:
    print('Hello i am a normal participator')
    api = f'{host}/create_participant/'
    try:
        response = requests.post(api, {
            'num_participants': participants,
            'host': host
        })
        assert response.status_code == 200
    except Exception as e:
        print('failed')
        exit(1)

else:
    try:
        response = requests.post(api, {
            'num_participants': participants,
            'host': host
        })
        assert response.status_code == 200
    except Exception as e:
        print('failed')
        exit(1)

while True:
    cmd = input("> ")
    print(cmd)

    if cmd == 'view':
        # print list of transaction from all blocks
        api = f'{host}/get_transactions/'
        blocks = requests.get(api).json()['blocks']
        for b in blocks:
            if b == blocks[-1]:
                # Write final time
                with open('log.txt', mode='a+') as f:
                    current_time = b['timestamp']
                    f.write(f'Final block at {current_time}\n')

            print(f'\nBlock {b["index"]}: (SHA: {b["hash"]}\tPREV: {b["prev"]})')

            for tx in b['transactions']:
                print(f'{tx["sender_id"]}\t->\t{tx["receiver_id"]}\t{tx["amount"]}\tNBC\t{tx["id"][:10]}')

    if cmd == 'balance':
        api = f'{host}/get_balance/'
        balance = requests.get(api).json()
        for id, p in balance.items():
            print(f'{id}\t({p["publickey"]})\t{p["host"]}\t{p["amount"]}\tNBC')

    if cmd == 'exit':
        sys.exit(0)

    if cmd.startswith('source'):
        p = cmd.split(' ')[1]
        FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   SOURCE_INPUTS_PATH)
        # API call to get list of {host,pubkey,amount} per participant
        balance = requests.get(f'{host}/get_balance/').json()
        # Read input from source file
        filename = 'transactions' + str(p) + '.txt'
        file = os.path.join(FOLDER_PATH, filename)
        init_time = True
        with open(file, mode='r') as src:
            # data = [transaction0, transaction1, ....  , transaction_n]
            data = [line.replace('\n', '') for line in src.readlines()]
            transactions = [t.replace('id', '').split(' ') for t in data
                            if len(t) != 0]

            # Init time
            if init_time is True:
                with open('log.txt', mode='w') as f:
                    current_time = datetime.datetime.now()
                    f.write(f'Block created at {current_time}\n')
                    init_time = False

            # Now create API for each transaction
            for receiver_id, amount in transactions:
                    # Create transaction dictionary
                    receiver_pubkey = balance[receiver_id]['publickey']
                    transaction = dict(receiver=receiver_pubkey,
                                       amount=int(amount))
                    # Send post request
                    requests.post(host + '/send_transaction/', transaction)
