import numpy as np
import numpy.random as random

### Create initial matrix
def create_matrix(rows=100, columns=100, seed=None):
    """
    Create a random binary matrix.

    Parameters:
        row (int): number of rows of the matrix. Default=100
        column (int): number of columns of the matrix. Default=100
        seed (int, optional): seed to initialise random generator (for reproducibility)

    Return:
        numpy.ndarray: A binary matrix of shape (row, column)

    """
    random.seed(seed)
    m = random.randint(0, 2, size = (rows,columns))

    return m

### Transition functions
"""
There are two transition functions that depends on the encoding functions (see encode.py):
    - CellularAutomaton_living: takes as input a rule based on the number of living neighbours (EncodingLiving)
    - CellularAutomaton_pattern: takes as input a rule based on the pattern (EncodingPattern)
"""

def CellularAutomaton_living(rule, matrix, time=100):
    """
    Update a matrix according to given rule.

    Parameters:
        - rule (dict): encoded rule based on the number of living neighbours
        - matrix (np.ndarray): initial 2D matrix representing the cellular automaton
        - time (int, optional): number of iterations to update the matrix. Default=100

    Return:
        np.ndarray: updated matrix after applying the rule for the given number of iterations.
    """
    rows, columns = matrix.shape
    for t in range(time):
        m_new = np.zeros(shape=(rows, columns), dtype=int)
        for i in range (rows):
            for j in range (columns):
                # Current cell
                cell=matrix[i, j]

                # Count the number of living neighbours (8 surrounding cells, with periodic boundaries)
                neighbours=(
                    matrix[(i - 1) % rows, (j - 1) % columns]
                    + matrix[(i - 1) % rows, j % columns]
                    + matrix[(i - 1) % rows, (j + 1) % columns]
                    + matrix[i % rows, (j - 1) % columns]
                    + matrix[i % rows, (j + 1) % columns]
                    + matrix[(i + 1) % rows, (j - 1) % columns]
                    + matrix[(i + 1) % rows, j % columns]
                    + matrix[(i + 1) % rows, (j + 1) % columns]
                )

                # Retrieve key code and replace cell by its value from the rule
                key = str(cell) + str(neighbours)
                m_new[i,j] = rule[key]

        matrix = m_new

    return matrix

def CellularAutomaton_pattern(rule, matrix, time=100):
    """
    Update a matrix according to given rule.

    Parameters:
        - rule (dict): encoded rule based on the current cell states and that of its neighbouring cells
        - matrix (np.ndarray): initial 2D matrix representing the cellular automaton
        - time (int, optional): number of iterations to update the matrix. Default=100

    Return:
        np.ndarray: updated matrix after applying the rule for the given number of iterations.
    """
    rows, columns = matrix.shape
    for t in range(time):
        m_new = np.zeros(shape=(rows, columns), dtype=int)
        for i in range (rows):
            for j in range (columns):

                # Retrieve key code 
                key = (str(matrix[i, j]) 
                       + str(matrix[(i - 1) % rows, (j - 1) % columns])
                       + str(matrix[(i - 1) % rows, j % columns])
                       + str(matrix[(i - 1) % rows, (j + 1) % columns])
                       + str(matrix[i % rows, (j - 1) % columns])
                       + str(matrix[i % rows, (j + 1) % columns])
                       + str(matrix[(i + 1) % rows, (j - 1) % columns])
                       + str(matrix[(i + 1) % rows, j % columns])
                       + str(matrix[(i + 1) % rows, (j + 1) % columns])
                )

                # Replace cell by its value from the rule if the pattern is in the rule
                if key in rule:
                    m_new[i,j] = rule[key]
                else:
                    m_new[i,j] = matrix[i,j]

        matrix = m_new

    return matrix

### Fitness Evaluation
def fitness(matrix):
    """
    Calculate the fitness of a rule based on the final state of a cellular automaton. The fitness score is higher when the automaton reaches approximately 50% living cells.

    Parameters:
        matrix(np.ndarray): 2D matrix representing the final state of a cellular automaton

    Returns:
        float: fitness score
    """
    # Count the proportion of living cells
    rows, columns = matrix.shape
    prop = matrix.sum() / (rows * columns)

    # Gaussian function
    mu = 0.5
    sigma = 0.15
    fitness = 100 * np.exp( -((prop-mu)**2) / (2*sigma**2))

    return fitness