import json
import copy
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

from .transaction import Transaction
from .block import Block
from . import state, nbcsettings, broadcast, miner
from threading import Thread

class ReceiveTransaction(View):
    '''
    A new transaction is received and is checked in validate_transaction()
    '''
    def post(self, request):
        tx_json = request.POST.get('transaction')
        res, t = Transaction.validate_transaction(tx_json)

        #miner here
        # miner.check()
        t = Thread(target=miner.check)
        t.start()
        if res == True:
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
        token = request.POST.get('token')

        # ?checkarisma me token?
        res = Transaction.create_transaction(receiver, amount)
        if res is None:
            return HttpResponseBadRequest('invalid transaction')

        broadcast.broadcast('receive_transaction', {
            'transaction': res.dump_sendable()
        })

        # miner.check()
        t = Thread(target=miner.check)
        t.start()

        return HttpResponse()
