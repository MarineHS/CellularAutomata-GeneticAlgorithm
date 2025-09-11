from encode import *
from automaton_fitness import *
from selection import *
from crossover import *
from mutation import *
import numpy.random as random
import numpy as np
import pandas as pd
import json
import os
import logging

### Set logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
ch.setFormatter(formatter)
logger.addHandler(ch)

def genetic_algorithm(encode, selection, crossover, output, mutation_rate=0.1, N=10, n_select=4, generation=10):
    """
    Select the best rule to achieve a given target
    
    Parameters :
        - encode (str) : select the encoding type. Takes 2 possible values: 'living' or 'pattern'
        - selection (str) : select the type of selection. Takes 4 possible values: 'random', 'best', 'weighted' or 'tournament'
        - crossover (str) : select the type of crossover. Takes 3 possible values: 'half', '1p', '2p'
        - output (str) : name of the output files
        - mutation_rate (float optional) : set the mutation rate. Default = 0.1
        - n_select (int optional) : number of parent rules selected. Default = 4
        - N (int optional) : initial population size. Default = 10
        - generation (int optional) : number of generation. Default = 10 

    Return :
        - json : 3 best rules
        - csv : fitness scores and parameters
    """

    # Initialisation
    logger.info('Initialisation')
    # Create the initial population
    g = 0
    if encode == 'living':
        population = [EncodingLiving() for i in range(N)]
    else:
        population = [EncodingPattern() for i in range(N)]

    # Create empty dataframe
    col_names = ['generation'] + ['rule_'+str(i) for i in range (1, N+1)] 
    df = pd.DataFrame(columns=col_names)

    # Create cellular automata
    init_CA = create_matrix(rows=100, columns=100, seed=70)


    # Start genetic algorithm
    while g < generation:
        # Evaluate fitness score
        for rule in range(N):
            if encode == 'living':
                final_CA = CellularAutomaton_living(population[rule], init_CA, time=100)
            else:
                final_CA = CellularAutomaton_pattern(population[rule], init_CA, time=100)

            fitness_score = fitness(final_CA)

            population[rule] = (population[rule], round(fitness_score, 4))

        # Add fitness values to csv
        df.loc[len(df)] = [g] + [i[1] for i in population]

        logger.info(f'generation: {g}; max fitness: {np.max([i[1] for i in population])}; mean fitness: {round(np.mean([i[1] for i in population]),2)}')

        # Select parent rules
        if selection == 'random':
            selected_rules = select_random(population, n_select)
        
        elif selection == 'best':
            selected_rules = select_best(population, n_select)

        elif selection == 'weighted':
            selected_rules = select_weighted(population, n_select)

        else:
            selected_rules = select_tournament(population, n_select)
        
        # Create new rules with crossover and mutation
        new_pop = []
        for i in range(N):
            parent1, parent2 = random.choice(selected_rules, size=2, replace=False)

            if crossover == 'half':
                new_rule = crossover_half(parent1, parent2)

            elif crossover == '1p':
                new_rule = crossover_random_1p(parent1, parent2)
            
            else:
                new_rule = crossover_random_2p(parent1, parent2)

            new_rule = mutation(new_rule, mutation_rate)

            new_pop.append(new_rule)
        
        population = new_pop
        g = g+1
    

    # End genetic algorithm and evaluate the final population
    for rule in range(N):
        if encode == 'living':
            final_CA = CellularAutomaton_living(population[rule], init_CA, time=100)
        else:
            final_CA = CellularAutomaton_pattern(population[rule], init_CA, time=100)

        fitness_score = fitness(final_CA)

        population[rule] = (population[rule], round(fitness_score), 4)

    df.loc[len(df)] = [g] + [i[1] for i in population] 

    best_rules = select_best(population, 3)
    
    # Return .json file with best rules and .csv with fitness score and parameters in Results folder
    results_dir = os.path.join(os.getcwd(), "Results")
    os.makedirs(results_dir, exist_ok=True)

    df.assign(
        encode = encode,
        selection = selection,
        crossover = crossover,
        mutation = mutation_rate,
        N = N,
        n_select = n_select
    )
    df.to_csv(os.path.join(results_dir, output + ".csv"), index=False) 

    with open(os.path.join(results_dir, output + ".csv"), 'w') as file:
        json.dump([i for i in best_rules], file, indent=4)
  
    logger.info('Genetic algorithm completed')

#genetic_algorithm(encode='living', selection='random', crossover='1p', output='test', mutation_rate=0.1, N=10, n_select=4, generation=10)