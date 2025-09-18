# Genetic algorithm

Genetic algorithms are commonly used to explore and optimize solutions to complex problems. In this section, I implemented a genetic algorithm inspired by three biological processes: selection, crossover, and mutation.

In our case, the problem is to evolve a cellular automaton that ends up with about 50% living cells after 100 time steps (see *CellularAutomaton* for more details). The main objective here is not to find the “perfect” rule, but rather to study how different parameters influence the algorithm’s behaviour and performance.


## Requirements

I used a Python3 environment to run the script. You may find all the external packages required in `requirements.txt`. Use the following command to install them if needed:

```bash
pip install -r requirements.txt
```


## Functionalities

This folder includes the main script and its modules:

- `genetic_algorithm`: main script that creates an initial population and evolves it through generations. It returns a JSON file with the three best rules and a CSV file with the fitness score of each individual at every generation
- `encode.py`: contains two encoding functions to create rules as dictionaries, based either on the number of living cells or on the pattern of neighbouring cells
- `automaton_fitness.py`: provides the functions to create and update a cellular automaton, as well as a function to evaluate rules with a fitness score
- `selection.py`: contains four functions to select parent rules
- `crossover.py`: contains three functions to create a new rule from two parents
- `mutation.py`: contains the function to apply random mutations at a given rate


## Implementation

The main application can be run directly from the terminal. It requires the encoding, selection, and crossover types, as well as an output name. Example command:

```bash
python genetic_algorithm.py --encode living --selection tournament --crossover 2p --output test
```


:construction: **Work in progress**

I am currently working on the impact of the main parameters of the genetic algorithm.  
Planned additions include three extra scripts:
- Evaluation of the performance of the best rules on random matrices
- Automation multiple runs with varying parameters
- Visualisation and summary of results