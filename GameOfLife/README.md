# Conway's Game of Life

In this section, I implement a cellular automaton that evolves according to Conway's Game of Life rules. The rules are as follows:
- a living cell dies if it has fewer than two living neighbours;
- a living cell dies if it has more than three living neighbours;
- a dead cell becomes alive if it has exactly three living neighbours


## Requirements

I used a Python3 environment to run the script. You may find all the external packages required in `requirements.txt`. Use the following command to install them if needed:

```bash
pip install -r requirements.txt
```


## Functionalities  

This folder includes **three main scripts**:  
- **main.py** →  Contains the main function, designed to be run from the terminal.
- **model.py** → Contains the core functions used by `main.py`, including functions to create (`create_matrix`) or verify (`verify_matrix`) the initial matrix and two transitions functions (`transition_deepcopy` and `transition_fillmatrix`).
- **performance.py** →  Compares the performance of the two transition functions.

**Note:** While developing transition functions, I considered two approaches: making a copy of the matrix and updating it (`transition_deepcopy`), or filling an empty matrix (`transition_fillmatrix`). I tested both on a 100 x 100 matrix (seed=885) over 10 000 iterations and 5 repetitions. On average, `transition_deepcopy` was slightly faster (434s against 459s). Therefore, I used it in `main.py`.


## Implementation

The main application can be run directly from the terminal. It requires either a matrix size or an input matrix provided by a JSON file and produces an animation. Example commands:

```bash
# Create a random matrix
python main.py -s 50 50

# Use an input matrix
python main.py -m file.json
```

Optional parameters:
- `--seed`: to set the seed while creating a random matrix (for reproducibility).
- `--time`: the number of animation frames (default is 100).
- `--save`: to save the animation as a GIF.


## Examples

This folder also provides several examples:

`example.gif` was generated with:

```bash
python main.py -s 100 100 --seed 50
```

From this example, different types of patterns can be observed: static, periodic and others that emerge and disappear. These patterns have been studied, and lists are available online. 

I also provide three input matrices with their animation results to illustrate static patterns (`input_pattern1`), oscillators (`input_pattern1` and `input_pattern2`) and gliders (`input_pattern3`).


Feel free to experiment with different matrices or your own custom matrix! You might discover new and surprising behaviors! :sparkles: