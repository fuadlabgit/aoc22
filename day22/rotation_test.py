
import numpy as np


def rotate_position(pos,N ):

    my_matrix = np.zeros((N,N))
    my_matrix[pos] = 1
    my_matrix = np.rot90(my_matrix)
    w = np.where(my_matrix==1)
    new_pos = (w[0][0],w[1][0])

    return new_pos

if __name__ == "__main__":

    N = 4
    pos = (1,3)
    pos2 = rotate_position(pos,N)
    pos3 = rotate_position(pos2,N)

    print(pos, pos2, pos3)
