import json
import copy
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

from .transaction import Transaction
from .block import Block
from . import state, nbcsettings, broadcast, miner

class ReceiveTransaction(View):
    '''
    A new transaction is received and is checked in validate_transaction()
    '''
    def post(self, request):
        tx_json = request.POST.get('transaction')
        res, t = Transaction.validate_transaction(tx_json)

        # Start miner
        miner.check()

        # Validate response
        if res is True:
            status = 200
        else:
            status = 400
        return HttpResponse(res, status=status)

class SendTransaction(View):
    '''
    A transaction is created and is broadcasted to the other participants
    '''
    def post(self, request):
        receiver = request.POST.get('receiver')
        amount = request.POST.get('amount')
        
        res = Transaction.create_transaction(receiver, amount)
        if res is None:
            return HttpResponseBadRequest('invalid transaction')

        broadcast.broadcast('receive_transaction', {
            'transaction': res.dump_sendable()
        })

        # Start miner
        miner.check()

        return HttpResponse()
