from model import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
    if matrix != None:
        m = verify_matrix(matrix) # use provided matrix

    # Create the matrix if needed
    elif size != (None, None):
        row, column = size
        m = create_matrix(row, column, seed) # generate random matrix

    else:
        raise ValueError("Either provide a matrix or a valid size.")

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

### Test main
#anim = main(size=(100,100), seed=50)
#anim.save('animation.gif', writer='PillowWriter', fps=10)



