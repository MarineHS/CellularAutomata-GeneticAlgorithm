from model import *
import timeit
import numpy as np

"""
Performance comparison of two matrix update functions used in the main script.
Both functions apply Conway's Game of Life rules to update a matrix:
    - transition_deepcopy: updates the matrix using a deepcopy of the original
    - transition_fillmatrix: creates an empty matrix and fill it based on the origin
"""

# Create a random binary matrix for the test.
# Fix the seed for reproducibility.
M=create_matrix(100, 100, seed=885)

# Parameters for the performance test
rep = 5  # Number of repetitions of the measurement
N = 10000 # Number of executions per repetition

# Measure performance of transition deepcopy
time_deepcopy = timeit.repeat(lambda: transition_deepcopy(M), repeat=rep, number=N)
print(f"[deepcopy] Average time over {rep} runs of {N} executions: {round(np.mean(time_deepcopy), 2)} s")


# Measure performance of transition_fillmatrix
time_fillmatrix = timeit.repeat(lambda: transition_fillmatrix(M), repeat=rep, number=N)
print(f"[fillmatrix] Average time over {rep} runs of {N} executions: {round(np.mean(time_fillmatrix), 2)} s")





