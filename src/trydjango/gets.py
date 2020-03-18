import json
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

# from block import Block
# from transaction import Transaction
# import state
from . import nbcsettings, state
# from .block import Block

class GetSetting(View):
    '''
    Return current blockchain
    '''
    def get(self, request):
        
            
        return JsonResponse({
            'blockchain': json.dumps(nbcsettings.DIFFICULTY)
        })





