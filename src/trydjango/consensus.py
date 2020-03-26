from . import state
from .block import Block
from .transaction import Transaction

import json
import copy
import requests

def validate_chain(blockchain, pending):

    state.blockchain = [state.genesis_block]
    state.utxos = copy.deepcopy(state.genesis_utxos)
    state.valid_utxos = copy.deepcopy(state.genesis_utxos)

    state.transactions = []

    index = 1
    for block in blockchain:
        # `Block.validate_block()` will also update any pending transactions
        # with conflicting inputs
        res = Block.validate_block(block, update=False)
        if res != 'good':
            return False
    
    for tx in pending:
        tx_json = tx.dump_sendable()
        Transaction.validate_transaction(tx_json)
    
    return True

def consensus():
    
    MAX_BLOCKCHAIN = copy.deepcopy(state.blockchain)
    MAX_TRANSACTIONS = copy.deepcopy(state.transactions)
    MAX_UTXOS = copy.deepcopy(state.utxos)
    MAX_VALID_UTXOS = copy.deepcopy(state.valid_utxos)
    MAX_LENGTH = len(MAX_BLOCKCHAIN)
    TRANSACTIONS_BACKUP = copy.deepcopy(state.transactions)

    for participant in state.participants.values():
        if participant['id'] == state.participant_id:
            continue

        pid = participant['id']
        host = participant['host']
        api = f'{host}/get_blockchain/'

        response = requests.get(api)
        if response.status_code != 200:
            raise Exception('invalid blockchain response')

        received_blockchain = json.loads(response.json()['blockchain'])
        print(received_blockchain)

        if len(received_blockchain) < MAX_LENGTH:
            print(f'{pid}. Sorry smaller chain')
            continue
        
        #we dont send genesis block for validation
        if not validate_chain(received_blockchain[1:], TRANSACTIONS_BACKUP):
            print('invalid blockchain')
            continue
        
        # update with best blockchain found
        state.blockchain = MAX_BLOCKCHAIN
        state.transactions = MAX_TRANSACTIONS
        state.utxos = MAX_UTXOS
        state.valid_utxos = MAX_VALID_UTXOS

        

        
