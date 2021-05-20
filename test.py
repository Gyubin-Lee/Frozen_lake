from simulator import move_forward, turn_left, turn_right, reset_map, set_speed, show_animation, test, set_map
import numpy as np

q_table = np.load("q_table.npy")

orientation = ['N','E','S','W']
actions = [move_forward, turn_left, turn_right]

thin_ice_blocks = [(1, 3), (1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 6)]

set_speed(10)
test()
#(x, y), ori, sensor, done = set_map(thin_ice_blocks)

##############################################
#### Copy and paste your step 4 code here ####
##############################################

(x, y), ori, sensor, done = reset_map()

while True:
	if ori == 'N':
		ori_num = 0
	elif ori == 'E':
		ori_num = 1
	elif ori == 'S':
		ori_num = 2
	else:
		ori_num = 3

	l, f, r = sensor

	action_num = np.argmax(q_table[ori_num][l][f][r])
	action = actions[action_num]
	(x, y), ori, sensor, done = action()

	if done:
		break
    
    

raise NotImplementedError
##############################################