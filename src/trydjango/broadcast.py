import requests
from . import state

def broadcast(api, message):
    #we send the message as data for each other /host/api

    for participant in state.participants:
        if participant['id'] == state.participant_id:
            continue

        host = participant['host']

        req = requests.post(f'{host}/{api}/', message)

        if req.status_code != 200:
            print(f'Broadcast: "{host}/{api}/" failed')