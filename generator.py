from model import Grid
import random

direction = [(-1,0), (1,0), (0,-1), (0,1), (-1,1), (-1,-1), (1,1), (1,-1)]

def generateMap(row, column, mine_number) :
	# create grids
	width = 800//row
	gap = (1600-width*column)//2
	grids = []	
	for i in range(row) :
		grids.append([])
		for j in range(column) :
			grids[i].append(Grid(i, j, gap+j*width+2, 100+i*width+2, width, 0))
	
	# choose grid to plant mine randomly
	unplanted_grids = []
	for i in range(row) :
		for j in range(column) :
			unplanted_grids.append((i,j))

	while mine_number :
		random.shuffle(unplanted_grids)
		planted_x, planted_y = unplanted_grids.pop()
		grids[planted_x][planted_y].adj_bomb = -1
		mine_number -= 1

	# calculate other grids' adjancy bomb number
	for i in range(row) :
		for j in range(column) :
			if grids[i][j].adj_bomb == -1 :
				continue
			for adj_x, adj_y in direction :
				if i+adj_x >= 0 and i+adj_x < row and j+adj_y >= 0 and j+adj_y < column :
					if grids[i+adj_x][j+adj_y].adj_bomb == -1 :
						grids[i][j].adj_bomb += 1
	
	return (grids, width, gap)
		
