from model import Grid
from init import mainWindow
import pygame
import random

direction = [(-1,0), (1,0), (0,-1), (0,1), (-1,1), (-1,-1), (1,1), (1,-1)]

def generateMap(row, column, mine_number) :
	# choose grid to plant mine randomly
	unplanted_grids = []
	adj_bomb_num = [[int(0) for j in range(column)] for i in range(row)] 
	for i in range(row) :
		for j in range(column) :
			unplanted_grids.append((i,j))
	while mine_number :
		random.shuffle(unplanted_grids)
		planted_x, planted_y = unplanted_grids.pop()
		adj_bomb_num[planted_x][planted_y] = -1
		mine_number -= 1
	# calculate other grid's adjacent bomb number
	for i in range(row) :
		for j in range(column) :
			if adj_bomb_num[i][j] == -1 :
				continue
			for adj_x, adj_y in direction :
				if i+adj_x >= 0 and i+adj_x < row and j+adj_y >= 0 and j+adj_y < column :
					if adj_bomb_num[i+adj_x][j+adj_y] == -1 :
						adj_bomb_num[i][j] += 1
	# create grids
	width = 800//row # grid width 
	gap = (1600-width*column)//2 # blank space of left and right side
	grids = []
	no_adj_bomb = [] # grids that have no adjacent bomb
	unflipped_img = pygame.image.load(f'imgs/size_{row}/cover.jpg') # for unflipped_sur
	bomb_img = pygame.image.load(f'imgs/size_{row}/bomb.png') # for flipped_sur
	flag_img = pygame.image.load(f'imgs/size_{row}/flag.png') # for flag_sur
	mark_img = pygame.image.load(f'imgs/size_{row}/Qmark.png') # for mark_sur
	font = pygame.font.Font('fonts/ComicRelief.ttf', width//2) # set text font showing adjacent bombs number
	for i in range(row) :
		grids.append([])
		for j in range(column) :
			# get flipped_sur ( blank/text/bomb image )
			flipped_img = pygame.Surface((width-2, width-2))
			flipped_img.fill((255,255,255))
			if adj_bomb_num[i][j] == -1 :
				flipped_img = bomb_img
			elif adj_bomb_num[i][j] != 0 :
				flipped_img = font.render(f"{adj_bomb_num[i][j]}", True, (0,0,0))
			else :
				no_adj_bomb.append((i,j))
			grids[i].append(Grid(gap+j*width+2, 100+i*width+2, width-2, adj_bomb_num[i][j], unflipped_img, flipped_img, flag_img, mark_img))
	# randomly mark a grid that has no adjacent bomb for the hint of first step
	random.shuffle(no_adj_bomb)
	x,y = no_adj_bomb[0]
	pygame.draw.rect(mainWindow, (236, 112, 99), grids[x][y].rect)

	return (grids, width, gap)
		
