import requests
import json
import datetime

from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

from .transaction import Transaction
from .block import Block
from . import state, nbcsettings, broadcast, miner, consensus
from threading import Thread

class ReceiveBlock(View):
    def post(self, request):
        block_json = request.POST.get('block')

        # Stop miner
        miner._stop()

        res = Block.validate_block(block_json)
        if res == 'error':
            return HttpResponseBadRequest(res)

        if res == 'consensus':
            print('we need consensus')
            res = consensus.consensus()

        if res == 'good':
            print('block is good')

        if res == 'dropped':
            print('block dropped')

        # Start miner
        miner.check()

        return HttpResponse(res)

class SendBlock(View):
    def post(self, request):
        transactions = json.loads(request.POST.get('transactions'))
        nonce = int(request.POST.get('nonce'))
        sha = request.POST.get('sha')
        # token = request.POST.get('token')
        timestamp = request.POST.get('timestamp')

        # Stop miner
        miner.stop()

        res = Block.create_block(transactions, nonce, sha, timestamp)

        if res is None:
            return HttpResponseBadRequest()

        broadcast.broadcast('receive_block', {
            'block': res.dump_sendable()
        })

        # Start miner
        miner.check()

        return HttpResponse()
