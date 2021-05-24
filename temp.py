import numpy as np

q_table = np.load("q_table.npy")

t = q_table[0][1][0][0]

print("move_forward: {}, turn_left: {}, turn_right: {}".format(t[0], t[1], t[2]))