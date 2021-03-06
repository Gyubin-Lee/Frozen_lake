from simulator import move_forward, turn_left, turn_right, reset_map, set_speed, show_animation, test
# DO NOT MODIFY LINE 1
# You may import any libraries you want. But you may not import simulator_hidden

import numpy as np
import time
import random

show_animation(True)
set_speed(10000)          # This line is only meaningful if animations are enabled.
 
#####################################
#### Implement steps 1 to 3 here ####
#####################################
grid_size   = (8, 8)             # Size of the map
goal        = (6, 6)             # Coordinates of the goal
orientation = ['N','E','S','W']  # List of orientations

# Hyperparameters: Feel free to change all of these!
actions = [move_forward, turn_left, turn_right]
num_epochs = 15000
alpha = 0.05
gamma = 0.99
epsilon = 0.3
q_table = np.zeros((4, 2, 2, 2, 3)) #(4, 2, 2, 2) for state, 3 for action

# Define your reward function
max_step = 100

def reward(done, dead, action_num):
	if dead:
		return -1
	
	if done:
		return 10
	
	if action_num == 0:
		return 0
	
	return -0.05
	raise NotImplementedError

def return_ori_num(ori):
	if ori == 'N':
		return 0
	elif ori == 'E':
		return 1
	elif ori == 'S':
		return 2
	else:
		return 3

def e_greedy(ori_num, l, f, r, eps):
	p = np.random.rand()
	if p < eps: #exploration
		action_num = (np.random.randint(3, 6)*np.random.randint(2, 5))%3
		action = actions[action_num]

	else: #exploitation
		action_num = np.argmax(q_table[ori_num][l][f][r])
		action = actions[action_num]
	
	return action, action_num

for i in range(num_epochs):
	(x, y), ori, sensor, done = reset_map()

	step = 0
	ori_num = return_ori_num(ori)
	#Q-learning
	while step < max_step:
		old_ori_num = ori_num
		old_l, old_f, old_r = sensor

		#select action by e-greedy policy
		action, action_num = e_greedy(old_ori_num, old_l, old_f, old_r, epsilon)
		
		if old_f == 1 and action_num == 0:	#terminate episode before robot falls into the lake
			dead = True
			rwrd = reward(done, dead, action_num)
			q_table[old_ori_num][old_l][old_f][old_r][action_num] = (1-alpha)*q_table[old_ori_num][old_l][old_f][old_r][action_num] + alpha*rwrd
			break
		else:
			dead = False

		#do transition
		(x, y), ori, sensor, done = action()
		step += 1

		if done: #terminate when robot arrived at the end point
			rwrd = reward(done, dead, action_num)
			q_table[old_ori_num][old_l][old_f][old_r][action_num] = (1-alpha)*q_table[old_ori_num][old_l][old_f][old_r][action_num] + alpha*rwrd
			break
		
		#update Q-table
		rwrd = reward(done, dead, action_num)
		ori_num = return_ori_num(ori)
		l, f, r = sensor
		max_qsa = np.max(q_table[ori_num][l][f][r])
		q_table[old_ori_num][old_l][old_f][old_r][action_num] = (1-alpha)*q_table[old_ori_num][old_l][old_f][old_r][action_num] + alpha*(rwrd + gamma*max_qsa)

	
	if i%100 == 99:
		epsilon *= 0.98
	
	#raise NotImplementedError

####################################

np.save("q_table", q_table)

set_speed(3)
test()
(x, y), ori, sensor, done = reset_map()


###############################
#### Implement step 4 here ####
###############################

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
	

#raise NotImplementedError
###############################

### If you want to try moving around the map with your keyboard, uncomment the below lines 
# import pygame
# set_speed(5)
# show_animation(True)
# while True:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			exit("Closing...")
# 		if event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_LEFT: print(turn_left())
# 			if event.key == pygame.K_RIGHT: print(turn_right())
# 			if event.key == pygame.K_UP: print(move_forward())
# 			if event.key == pygame.K_t: test()
# 			if event.key == pygame.K_r: print(reset_map())
# 			if event.key == pygame.K_q: exit("Closing...")