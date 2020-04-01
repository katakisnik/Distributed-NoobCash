"""
Global variables for each state of our application.
Every Participant has his own state
"""
from threading import RLock
lock = RLock()

# list of validated blocks
blockchain = []

# list of valid transactions that are not yet in a block
transactions = []

# list of participants
participants = {}

# number of participants
num_participants = -1

# participant_id = 0 -> coordinator
participant_id = -1

# private and public key for each participant
publickey = None
privatekey = None

# unspent transactions of each participant
utxos = {}

# validated utxos, untill final validated block
valid_utxos = {}

# pid of miner
miner_pid = None

# genesis block and utxos
genesis_block = None
genesis_utxos = []

# token for transaction authentication
token = None
