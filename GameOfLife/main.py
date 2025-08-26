from model import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse
import json

### main function
def main(matrix=None, size=(None, None), seed=None, time=100):
    """
    Create a matrix and update it according to Conway's Game of Life Rules

    Parameters:
        matrix (list optional): Input matrix. If provided, 'size' and 'seed' are ignored.
        size (tuple of ints, optional): Dimensions (rows, columns) of the matrix to create if 'matrix' is None.
        seed (int optional): Random seed for reproducibility when creating a new matrix.
        time (int optional): Number of frames / updates. Default is 100.


    Returns:
        matplotlib.animation.FuncAnimation: The animation object showing the evolution of the cellular automaton.
    """

    # Verify or create the initial matrix
    if matrix is not None:
        m = verify_matrix(matrix) # use provided matrix

    # Create the matrix if needed
    else:
        row, column = size
        m = create_matrix(row, column, seed) # generate random matrix

    # Create the figure and display the initial state
    fig, ax = plt.subplots()
    ax.set_axis_off()
    im = ax.imshow(m, cmap="Greys")

    # Define the function to update the matrix for each frame
    def animate(frame):
        nonlocal m
        m = transition_deepcopy(m)
        im.set_data(m)
        return [im]

    # Create the animation object
    anim = FuncAnimation(
        fig,
        animate,
        frames = time,
        blit=True,
    )

    plt.show()

    return anim

### Parse the arguments
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run Conway\'s Game of Life')
    input_type = parser.add_mutually_exclusive_group(required=True)
    input_type.add_argument("-m", "--matrix", type=str, help="Path to a JSON file containing the input matrix")
    input_type.add_argument("-s", "--size", nargs=2, type=int, help="Size (row, column) of a random matrix")

    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--time", type=int, default=100, help="Number of frames / updates. Default is 100")
    parser.add_argument("--save", type=str, help="Save a gif animation under the given filename")
    args = parser.parse_args()

    size = tuple(args.size) if args.size else (None, None)
    if args.matrix:
        with open(args.matrix, 'r') as file:
            matrix = json.load(file)
    else:
        matrix = None

    anim = main(matrix=matrix, size=size, seed=args.seed, time=args.time)
    
    if args.save:
        anim.save(args.save + '.gif', writer='PillowWriter', fps=10)




