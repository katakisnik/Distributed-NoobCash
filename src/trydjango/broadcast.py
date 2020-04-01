import requests
from . import state

def broadcast(api, message):
    '''Everytime a transaction or a block is send, we use broadcast to inform all the participants'''

    for participant in state.participants.values():
        if participant['id'] == state.participant_id:
            continue

        host = participant['host']

        req = requests.post(f'{host}/{api}/', message)

        if req.status_code != 200:
            print(f'Broadcast: "{host}/{api}/" failed')
