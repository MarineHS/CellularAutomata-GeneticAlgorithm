import numpy.random as random
import itertools

"""
Encoding functions
- EncodingLiving: Create a rule according to the number of living neighbouring cells
- EncodingPattern: Create a rule according to the pattern around the target cell
"""

def EncodingLiving():
    """
    Encode a random transition rule based on the current cell states and the number of living cells.

    Return:
        dict:
            - keys are two-digit strings where the first digit is the initial state of the cell (0 = dead, 1 = alive) and the second digit is the number of living neighbors
            - values are the resulting state
    """
    
    keys = [str(i)+str(x) for i in range(2) for x in range(9)]
    values = random.randint(0, 2, size=len(keys)).tolist()

    rule = dict(zip(keys, values))

    return rule

def EncodingPattern():
    """
    Encode a random transition rule based on the current cell states and the states of the neighbouring cells.

    Return:
        dict:
            - keys are nine-digit strings where the first digit is the initial state of the cell (0 = dead, 1 = alive) and the rest represent the state of the neighbours starting on the starting from the upper-left corner and circling clockwise
            - values are the resulting state
    """

    # List of all possible combination
    combination = list(itertools.product([0, 1], repeat=9))

    keys = []
    for i in combination:
        # Convert tuple into string
        keys.append(''.join(str(val) for val in i))
    values = random.randint(0, 2, size=len(keys)).tolist()

    rule = dict(zip(keys, values))

    return rule
