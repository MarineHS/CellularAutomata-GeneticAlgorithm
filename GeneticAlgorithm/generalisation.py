from automaton_fitness import *
import json
import pandas as pd
import logging
import argparse
import os

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

def generalisation(json_file, encode, rep=100):
    """
    Extracts rules from a JSON file and evaluate their performance on randomly generated cellular automata.

    Parameters:
        json_file (str) : path to the json file containing the rules
        encode (str) : Encoding type to use. Takes 2 possible values: 'living' or 'pattern'
        rep (int) : number of tests to run per rule

    Returns:
        csv : evaluation scores for each rule
    """
    idx = json_file.find('.json')
    prefix = json_file[:idx]

    # Create dataframe
    col_names = ['rule'] + ['rep'+str(i) for i in range (1, rep+1)] 
    df = pd.DataFrame(columns=col_names)

    # Retrieve rules
    with open(json_file, 'r') as file:
        rule = json.load(file)

    nb_rule = 1

    for i in rule:

        logger.info(f'Considering rule number: {nb_rule}')
        new_line = [int(nb_rule)]

        # Evaluate performance on random matrices
        for r in range (rep):
            init_CA = create_matrix(rows=100, columns=100)

            if encode == 'living':
                final_CA = CellularAutomaton_living(i, init_CA, time=100)
            else:
                final_CA = CellularAutomaton_pattern(i, init_CA, time=100)

            new_line.append(round(fitness(final_CA), 4))

        # Add new line to dataframe with rule number and their scores
        df.loc[len(df)] = new_line
        nb_rule += 1

    df['rule'] = df['rule'].astype('int')
    df.to_csv(os.path.join(prefix + "_generalisation.csv"), index=False) 

### Parse arguments
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get performance scores from random matrices')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to JSON input file')
    parser.add_argument('-e', '--encode', type=str, choices=['living', 'pattern'], required=True, help='Select the encoding type between "living" or "pattern"')
    parser.add_argument('--rep', type=int, default=100, help='Number of repetitions (100 by default).')
    args = parser.parse_args()

    generalisation(json_file=args.file, encode=args.encode, rep=args.rep)