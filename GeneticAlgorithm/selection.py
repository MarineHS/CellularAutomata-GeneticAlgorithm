import numpy as np
import numpy.random as random
"""
Functions used to select rules:
    - select_random: randomly select the rules
    - select_best: select rules with the highest fitness score
    - select_weighted: randomly select rules weighted by their fitness score
    - select_tournament: randomly select two rules and choose the one with the higher fitness
"""

def select_random(population_fitness, n=4):
    """
    Randomly select a number of rules from a population.
    
    Parameters:
        - population (list): set of rules and their fitness score
        - n (int): number of rules selected. Default = 4

    Return:
        list: n randomly selected rules
    """
    rules = [i[0] for i in population_fitness]
    selected_rules = list(random.choice(rules, size=n, replace=False))

    return selected_rules


def select_best(population_fitness, n=4):
    """
    Select the rules with the highest fitness scores
    
    Parameters:
        - population_fitness (list): set of rules and their fitness score
        - n (int): number of rules selected. Default = 4
    
    Return:
        list: n best rules
    """

    population_fitness.sort(key=lambda tup: tup[1], reverse=True)
    selected_rules = [i[0] for i in population_fitness[0:n]] 

    return selected_rules


def select_weighted(population_fitness, n=4):
    """
    Randomly select rules weighted by their fitness score
    
    Parameters:
        - population_fitness (list): set of rules and their fitness score
        - n (int): number of rules selected. Default = 4
    
    Return:
        list: n distinct rules
    """

    rules = [i[0] for i in population_fitness]
    eps = 0.001 # prevent the division by 0
    fitness = [i[1]+eps for i in population_fitness] 
    weight = [i/sum(fitness) for i in fitness]

    selected_rules = list(random.choice(rules, size=n, replace=False, p=weight))

    return selected_rules


def select_tournament(population_fitness, n=4):
    """
    Randomly select two rules and choose the rule with the higher fitness
    
    Parameters:
        - population_fitness (list): set of rules and their fitness score
        - n (int): number of rules selected. Default = 4
    
    Return:
        list: n distinct rules
    """
    selected_rules = []

    for i in range(n):
        competitors = random.choice(np.arange(len(population_fitness)),2, replace=False)

        if population_fitness[competitors[0]][1]>population_fitness[competitors[1]][1]:
            selected_rules.append(population_fitness[competitors[0]][0])
        else:
            selected_rules.append(population_fitness[competitors[1]][0])

    return selected_rules

