from simulator import move_forward, turn_left, turn_right, reset_map, set_speed, show_animation, test, set_map
import numpy as np

q_table = np.load("q_table.npy")

orientation = ['N','E','S','W']
actions = [move_forward, turn_left, turn_right]

thin_ice_blocks = [(4, 6), (3, 5)]

show_animation(True)
set_speed(10000)
#test()
#(x, y), ori, sensor, done = set_map(thin_ice_blocks)
(x, y), ori, sensor, done = reset_map()

##############################################
#### Copy and paste your step 4 code here ####
##############################################

for j in range(5):
	score = 0
	for i in range(1000):
		(x, y), ori, sensor, done = reset_map()
		
		step = 0
		while step < 50:
			
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

			if f == 1 and action_num == 0:	
				dead = True
			else:
				dead = False
			
			(x, y), ori, sensor, done = action()
			step += 1

			if done:
				break
		
		if done:
			if not dead:
				score += 1

	print("test{}: Model score -> {}%".format(j+1, score/10))   

#raise NotImplementedError
##############################################