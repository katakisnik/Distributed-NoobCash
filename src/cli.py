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

host = f'http://{args.host}:{args.port}'
participants = args.num_participants

API = f'{host}/create_coordinator/'

try:
    response = requests.post(API, {
        'num_participants': participants,
        'host': host
    })
    assert response.status_code == 200
except Exception as e:
    print('failed')
    exit(1)