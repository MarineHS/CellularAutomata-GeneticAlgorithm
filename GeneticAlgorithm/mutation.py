import numpy.random as random

def mutation(rule, mutation_rate=0.1):
    """
    Apply random mutations (in place) to a rule.

    Parameters:
        - rule (dict): chromosome encoding the rule (set of conditions)
        - mutation_rate (float): probability for each condition to flip (0 -> 1 or 1 -> 0). Default = 0.1

    Return:
        dict: mutated rule
    """

    for i in rule:
        if random.random() < mutation_rate:
            rule[i] = (rule[i]+1) %2
    
    return rule