"""All settings needed for nbc to be functional."""
# Python settings
PYTHON_VERSION = 'python3.7'

BLOCK_CAPACITY = 2

# Blockchain settings
DIFFICULTY = 3

RAND = 1000000

# Django settings
COORDINATOR_PORT = 8000

CORDINATOR = f'http://192.168.1.5:{COORDINATOR_PORT}'

SOURCE_INPUTS_PATH = 'source_files/inputs3/'
