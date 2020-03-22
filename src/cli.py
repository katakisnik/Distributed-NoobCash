import requests
import argparse
import sys

# BASE_DIR = os.path.dirname(__file__)
# sys.path.append(BASE_DIR)

#arguments parsing
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
    api = f'{coordinatorhost}/create_participant/'
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
