from genetic_algorithm import *

### Initialisation
encode = 'living'   # ['living' or 'pattern']
selection = ['random', 'best', 'weighted', 'tournament']
crossover = 'half'    # ['half', '1p', '2p']
mutation_rate = 0.1    # [0.01, 0.05, 0.1, 0.5]
n_select = 4    # [2, 4, 6]

param_modif = selection

### Test function
def test_parameter(encode, selection, crossover, mutation_rate, n_select):
    for i in range(len(param_modif)):
        output = 'selection_'+str(param_modif[i])
        genetic_algorithm(encode, selection, crossover, output, mutation_rate, N=10, n_select, generation=10)
        print(str(output) + ' done')

### Run test parameters
test_parameter(encode, selection, crossover, mutation_rate, n_select)