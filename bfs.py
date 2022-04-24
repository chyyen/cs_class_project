from generator import direction


# check wheater coor out of range
def check_valid(x_range, y_range, x, y) :
	return x >= 0 and x < x_range and y >= 0 and y < y_range


def bfs(grids, x_range, y_range, start_x, start_y) :
	que = [] # simulate queue
	queue_idx = 0
	tagged_num = 0 # the number of grids that is tagged and flipped
	flipped_num = 0 # the number of grids be flipped

	tagged_num += grids[start_x][start_y].flip() # return 1 if the grid has been tageed, -1 if the grid has bomb , 0 otherwise
	flipped_num += 1
	if tagged_num == -1 : # flip a bomb
		return (0,-1)

	if(grids[start_x][start_y].adj_bomb == 0) :
		que.append((start_x,start_y))

	while queue_idx < len(que) :
		cur_x, cur_y = que[queue_idx]
		queue_idx += 1
		# check through eight direction
		for xx,yy in direction : 
			adj_x, adj_y = cur_x+xx, cur_y+yy
			if check_valid(x_range, y_range, adj_x, adj_y) and grids[adj_x][adj_y].flipped == False :
				tagged_num += grids[adj_x][adj_y].flip() # flip up the grid
				flipped_num += 1
				if grids[adj_x][adj_y].adj_bomb == 0 : # if the grid has no adjancy bombs, push into queue
					que.append((adj_x, adj_y))

	return (flipped_num, tagged_num)
