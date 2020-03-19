import json
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import nbcsettings, state, keygenerator
from .block import Block

class GetSetting(View):
    def get(self, request):
        
            
        return JsonResponse({
            'blockchain': json.dumps(nbcsettings.DIFFICULTY)
        })

#the coordinator is created and is added to the participants
class CreateCoordinator(View):
    @csrf_exempt
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

#test function to see if the coordinator is created
class GetParticipants(View):
    def get(self, request):
        return JsonResponse({
            'participants': json.dumps(state.participants)
        })
