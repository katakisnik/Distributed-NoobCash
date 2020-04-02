"""Create stat diagrams for Noobcash Blockchain"""
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# SAVECONFIG
FOLDER = 'plots/'

def get_parameters(filename):
    """Parse file and get all the parameters"""

    with open(filename,mode='r') as f:
        # Open file
        data_raw = [l.replace('\n', '') for l in f.readlines() if l[0] != '#']

        # Get sample size
        samples_size = int(len([s for s in data_raw if len(s) != 0]) / 2)
        # Initialize empty numpy arrays
        block5 = []
        transactions5 = []
        block10 = []
        transactions10 = []

        # Parse each line
        for i, line in enumerate(data_raw):
            # Skip empty lines
            if len(line) == 0:
                continue
            # Remove descriptions
            line = line.replace('capacity', '').replace(
                                ', difficulty', '').replace(
                                '->', '').replace(
                                'block/min,', '').replace(
                                'transactions/min', '')
            cap, dif, bl, tr = [e for e in line.split(' ') if len(e) != 0]
            if i < samples_size:
                block5.append([float(bl), f'({cap}, {dif})'])
                transactions5.append([float(tr), f'({cap}, {dif})'])
                continue
            block10.append([float(bl), f'({cap}, {dif})'])
            transactions10.append([float(tr), f'({cap}, {dif})'])

        return block5, transactions5, block10, transactions10

def draw_graph(a5, a10, ylabel='', fname=''):
    """Draw and save the figure"""

    plt.figure(figsize=(10, 10))
    for a in [a5, a10]:
        y = [v[0] for v in a]
        x = [v[1] for v in a]
        plt.scatter(x, y)
        plt.plot(x, y)
    plt.xlabel('(Capacity, Difficulty)')
    plt.ylabel(ylabel)
    plt.suptitle(fname)
    plt.savefig(f'{FOLDER}plot_{fname}')

if __name__ == '__main__':
    """Read the output files and create a plot"""

    b5, t5, b10, t10 = get_parameters(sys.argv[1])
    # Check folder exists
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

    # Draw graph for block capacity
    draw_graph(b5, b10, ylabel='Block added/min', fname='Block_per_min')
    # Draw graph for transactions
    draw_graph(t5, t10, ylabel='transactions/min', fname='Throughput')
