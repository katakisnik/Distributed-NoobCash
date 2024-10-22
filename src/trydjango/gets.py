import json
import copy
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

from . import nbcsettings, state, keygenerator, broadcast
from .block import Block
from .transaction import Transaction

#the coordinator is created and is added to the participants
class CreateCoordinator(View):
    def post(self, request):
        num_participants = int(request.POST.get('num_participants'))
        host = request.POST.get('host')

        keygenerator.keygenerator()
        print(state.publickey)
        state.num_participants = num_participants
        state.participant_id = 0
        state.utxos = { }
        state.utxos[state.publickey] = []
        state.participants[state.publickey] = {
            'host': host,
            'id': state.participant_id
        }

        return HttpResponse(state.token)

#participant gets created
class CreateParticipant(View):
    def post(self, request):
        host = request.POST.get('host')
        keygenerator.keygenerator()
        #participant sends his configuration to the coordinator
        api = f'{nbcsettings.CORDINATOR}/participant_connect/'
        print(api)
        data = {
            'host': host,
            'publickey': state.publickey
        }
        response = requests.post(api, data=data)
        if response.status_code != 200:
            return HttpResponseBadRequest()

        return HttpResponse(state.token)

#the coordinator connects its participant to the noobcash network
class ConnectParticipant(View):
    def post(self, request):
        host = request.POST.get('host')
        publickey = request.POST.get('publickey')
        print(publickey)

        #id is equal to number of participants already present
        participantid = len(state.participants)
        state.participants[publickey] = {
            'host': host,
            'id': participantid
        }
        state.utxos[publickey] = []

        #if all clients have connected then we send to each one that they are accepted
        if len(state.participants) == state.num_participants:
            if not Block.create_genesis_block(state.num_participants):
                return HttpResponseBadRequest()
            for participant in state.participants.values():
                #we ignore the coordinator of course
                if participant['id'] == state.participant_id:
                    continue

                #we send to each participant the list with the things that should also know
                host = participant['host']
                api = f'{host}/participant_accept/'
                requests.post(api, {
                    'participant_id': participant['id'],
                    'participants': json.dumps(state.participants),
                    'genesis_block': state.genesis_block.dump_sendable(),
                    'genesis_utxos': json.dumps(state.utxos)
                })
            #after everyone connects the coordinator sends to everyone 100NBC
            for publickey in state.participants:
                if publickey == state.publickey:
                    continue
                transaction = Transaction.create_transaction(publickey, 100)
                #print(transaction.dump_sendable())
                if not transaction:
                    return HttpResponseBadRequest()

                #this needs to be broadcasted to everyone
                broadcast.broadcast('receive_transaction', {
                    'transaction': transaction.dump_sendable()
                })

        return HttpResponse()

#after the participant is accepted in the network he gets all the data that he needs
class AcceptParticipant(View):
    def post(self, request):
        participant_id = int(request.POST.get('participant_id'))
        participants = json.loads(request.POST.get('participants'))
        genesis_block = request.POST.get('genesis_block')
        genesis_utxos = json.loads(request.POST.get('genesis_utxos'))

        state.participant_id = participant_id
        state.participants = participants
        state.num_participants = len(state.participants)
        state.utxos = copy.deepcopy(genesis_utxos)
        state.blockchain = [Block(**json.loads(genesis_block), index=0)]
        state.valid_utxos = copy.deepcopy(state.utxos)
        state.genesis_block = Block(**json.loads(genesis_block), index=0)
        state.genesis_utxos = genesis_utxos

        return HttpResponse()

#test function to see if the coordinator is created
class GetParticipants(View):
    def get(self, request):
        return JsonResponse({
            'participants': json.dumps(state.participants)
        })

#returns every block with its transactions
class GetAllTransactions(View):
    def get(self, request):
        blocks = []
        for block in state.blockchain:
            txs = []
            for tx_json in block.transactions:
                tx = Transaction(**json.loads(tx_json))

                txs.append({
                    'sender_id': state.participants[tx.sender]['id'],
                    'receiver_id': state.participants[tx.receiver]['id'],
                    'id': tx.id,
                    'amount': tx.amount
                })
            blocks.append({
                'index': block.index,
                'transactions': txs,
                'hash': block.current_hash,
                'prev': block.previous_hash,
                'timestamp': block.timestamp
            })
        return JsonResponse({'blocks': blocks})

#return for each participant the amount of nbc they have
class GetBalance(View):
    """
    A method to return a list of {host,pubkey,amount}
    for each participant.
    """
    def get(self, request):
        result = {}
        for publickey in state.participants:
            result[state.participants[publickey]['id']] = {
                'host': state.participants[publickey]['host'],
                'publickey': publickey,
                'amount': sum(x['amount'] for x in state.valid_utxos[publickey])
            }
        return JsonResponse(result)

#return the entire blockchain
class GetBlockchain(View):
    def get(self, request):
        return JsonResponse({
            'blockchain': json.dumps([b.dump_sendable() for b in state.blockchain])
        })
