import itertools
import numpy.random as random

"""
Functions used for crossover:
    - crossover_half: combine half rules of two parents into a new rule
    - crossover_random_1p: combine two parent rules at a random position using one-point crossover
    - crossover_random_2p: combine two parent rules at two random positions using two-point crossover
"""

def crossover_half(parent1, parent2):
    """
    Combine half rules of two distinct parents into a new rule
    
    Parameters:
        - parent1 (dict): rule of the first parent
        - parent2 (dict): rule of the second parent
    
    Return:
        dict: new rule combining the first half of parent1 and the second half of parent2
    """

    half_rule = int(len(parent1)/2)
    rule = dict(itertools.islice(parent1.items(), half_rule))
    rule.update(dict(itertools.islice(parent2.items(), half_rule, int(len(parent2)))))

    return rule

def crossover_random_1p(parent1, parent2):
    """
    Combine two parent rules at a random position into a new rule
    
    Parameters:
        - parent1 (dict): rule of the first parent
        - parent2 (dict): rule of the second parent
    
    Return:
        dict: new rule combining the first part from parent1 and the remainder from parent2
    """
    
    # Randomly choose the position of the crossover
    pos = random.randint(1,len(parent1))

    rule = dict(itertools.islice(parent1.items(), pos))
    rule.update(dict(itertools.islice(parent2.items(), pos, int(len(parent2)))))

    return rule

def crossover_random_2p(parent1, parent2):
    """
    Combine two parent rules at two random positions using two-point crossover
    
    Parameters:
        - parent1 (dict): rule of the first parent
        - parent2 (dict): rule of the second parent
    
    Return:
        dict: new rule combining the first part from parent1 up to pos1, the middle part from parent2 between pos1 and pos2 and the last part from parent1 after pos2
    """
    
    # Randomly choose the positions of the crossover
    pos1 = random.randint(1,len(parent1)-2)
    pos2 = random.randint(pos1+1, len(parent1))

    rule = dict(itertools.islice(parent1.items(), pos1))
    rule.update(dict(itertools.islice(parent2.items(), pos1, pos2)))
    rule.update(dict(itertools.islice(parent1.items(), pos2, int(len(parent1)))))

    return rule