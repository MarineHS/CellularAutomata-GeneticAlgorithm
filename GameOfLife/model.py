import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import copy

### Create a random binary matrix
def create_matrix(row, column, seed=None):
    """
    Create a random binary matrix.

    Parameters:
        row (int): number of rows of the matrix
        column (int): number of columns of the matrix
        seed (int, optional): seed to initialise random generator (for reproductibility)

    Return:
        numpy.ndarray: A binary matrix of shape (row, column)

    """

    random.seed(seed)
    m = random.randint(0, 2, size = (row,column))

    return m

### Verify if matrix is binary
def verify_matrix(m):
    """
    Convert to np.ndarray type and check if the input matrix is a valid binary 2D numpy array.

    Parameters:
        m: Input matrix.

    Returns:
        numpy.ndarray: a binary matrix

    Raises:
        ValueError: If the matrix is not 2D or smaller than 2x2.
        ValueError: If the matrix contains values other than 0 and 1.

    """

    # Convert to np.ndarray type
    m=np.array(m)

    # Check if the matrix not 2D or smaller than 2x2
    matrix_shape = m.shape
    if len(matrix_shape)!=2 or any(x < 2 for x in m.shape):
        raise ValueError('The matrix is not 2D or smaller than 2x2.')

    # Check if the matrix is binary
    if not np.isin(m, [0,1]).all():
        raise ValueError('The matrix contains values other than 0 and 1.')

    return m


### Transition functions using deepcopy or empty matrix to fill
def transition_deepcopy(m):
    """
    Update each cell of a cellular automaton according to Conway's Game of Life rules.
    This implementation uses a deepcopy of the original matrix to avoid modifying it in place.

    Parameters:
        m (numpy.ndarray): The input binary matrix representing the cellular automaton.

    Returns:
        numpy.ndarray: The updated matrix after applying the transition rules.
    """

    row, column = m.shape

    # Make a deepcopy to update and keep the original
    m_copy = copy.deepcopy(m)

    for i in range (row):
        for j in range (column):
            # Current cell
            cell=m[i, j]

            # Count the number of living neighbours (8 surrounding cells, with periodic boundaries)
            neighbours=(
                m[(i - 1) % row, (j - 1) % column]
                + m[(i - 1) % row, j % column]
                + m[(i - 1) % row, (j + 1) % column]
                + m[i % row, (j - 1) % column]
                + m[i % row, (j + 1) % column]
                + m[(i + 1) % row, (j - 1) % column]
                + m[(i + 1) % row, j % column]
                + m[(i + 1) % row, (j + 1) % column]
            )

            # Update the deepcopy according to the rules
            if cell == 0 and neighbours == 3:
                m_copy[i, j] = 1
            elif cell == 1 and (neighbours < 2 or neighbours > 3):
                m_copy[i, j] = 0

    return m_copy


def transition_fillmatrix(m):
    """
    Update each cell of a cellular automaton according to Conway's Game of Life rules.
    This implementation uses en empty matrix to avoid modifying the original one in place.

    Parameters:
        m (numpy.ndarray): The input binary matrix representing the cellular automaton.

    Returns:
        numpy.ndarray: The updated matrix after applying the transition rules.
    """

    row, column = m.shape

    matrix_update = np.zeros([row, column], dtype = int)

    for i in range (row):
        for j in range (column):
            cell = m[i, j]

            # Count the number of living neighbours (8 surrounding cells, with periodic boundaries)
            neighbours=(
                m[(i - 1) % row, (j - 1) % column]
                + m[(i - 1) % row, j % column]
                + m[(i - 1) % row, (j + 1) % column]
                + m[i % row, (j - 1) % column]
                + m[i % row, (j + 1) % column]
                + m[(i + 1) % row, (j - 1) % column]
                + m[(i + 1) % row, j % column]
                + m[(i+1) % row, (j + 1) % column]
            )

            # Update the deepcopy according to the rules
            if cell == 0 and neighbours == 3:
                matrix_update[i, j] = 1
            elif cell == 1 and (neighbours < 2 or neighbours > 3):
                matrix_update[i, j] = 0
            else:
                matrix_update[i, j] = cell

    return matrix_update