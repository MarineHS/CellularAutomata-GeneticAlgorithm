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
import argparse

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

### Main function 
def genetic_algorithm(encode, selection, crossover, output, mutation_rate=0.1, N=10, n_select=4, generation=10):
    """
    Select the best rule to achieve a given target
    
    Parameters :
        - encode (str) : select the encoding type. Takes 2 possible values: 'living' or 'pattern'
        - selection (str) : select the type of selection. Takes 4 possible values: 'random', 'best', 'weighted' or 'tournament'
        - crossover (str) : select the type of crossover. Takes 3 possible values: 'half', '1p' or '2p'
        - output (str) : name of the output files
        - mutation_rate (float optional) : set the mutation rate. Default = 0.1
        - n_select (int optional) : number of parent rules selected. Default = 4
        - N (int optional) : initial population size. Default = 10
        - generation (int optional) : number of generations. Default = 10 

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
        df.loc[len(df)] = [int(g)] + [i[1] for i in population]

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

    df.loc[len(df)] = [int(g)] + [i[1] for i in population] 

    best_rules = select_best(population, 3)
    
    # Return .json file with best rules and .csv with fitness score and parameters in Results folder
    results_dir = os.path.join(os.getcwd(), "Results")
    os.makedirs(results_dir, exist_ok=True)

    df["encode"] = encode
    df["selection"] = selection
    df["crossover"] = crossover
    df["mutation"] = mutation_rate
    df["N"] = N
    df["n_select"] = n_select

    df.to_csv(os.path.join(results_dir, output + ".csv"), index=False) 

    with open(os.path.join(results_dir, output + ".json"), 'w') as file:
        json.dump([i for i in best_rules], file, indent=4)
  
    logger.info('Genetic algorithm completed')

### Parse the arguments
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run Genetic Algorithm')
    parser.add_argument('-e', '--encode', type=str, choices=['living', 'pattern'], required=True, help='Select the encoding type between "living" or "pattern"')
    parser.add_argument('-s', '--selection', type=str, choices=['random', 'best', 'weighted', 'tournament'], required=True, help='Select the type of selection between "random", "best", "weighted" or "tournament"')
    parser.add_argument('-c', '--crossover', type=str, choices=['half', '1p', '2p'], required=True, help='Select the type of crossover between "half", "1p" or "2p"')
    parser.add_argument('-o', '--output', type=str, required=True, help='Name of the output files')

    parser.add_argument('--mutation', type=float, default=0.1, help='Set the mutation rate (0.1 by default)')
    parser.add_argument('--parents', type=int, default=4, help='Number of parent rules selected (4 by default)')
    parser.add_argument('--N', type=int, default=10, help='Initial population size (10 by default)')
    parser.add_argument('--generation', default=10, type=int, help='Number of generations (10 by default)')
    args = parser.parse_args()

    if args.parents > args.N:
        parser.error("Number of parents cannot exceed population size N")

    genetic_algorithm(
        encode=args.encode, 
        selection=args.selection, 
        crossover=args.crossover, 
        output=args.output, 
        mutation_rate=args.mutation, 
        N=args.N, 
        n_select=args.parents, 
        generation=args.generation)
