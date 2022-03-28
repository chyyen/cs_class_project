from generator import direction


def check_valid(x_range, y_range, x, y) :
	return x >= 0 and x < x_range and y >= 0 and y < y_range


def bfs(grids, x_range, y_range, start_x, start_y) :
	que = [] # simulate queue
	queue_idx = 0
	updated = []

	grids[start_x][start_y].flip()
	updated.append((start_x, start_y))
	if(grids[start_x][start_y].adj_bomb == 0) :
		que.append((start_x,start_y))

	while queue_idx < len(que) :
		cur_x, cur_y = que[queue_idx]
		queue_idx += 1
		# check through eight direction
		for xx,yy in direction : 
			adj_x, adj_y = cur_x+xx, cur_y+yy
			if check_valid(x_range, y_range, adj_x, adj_y) and grids[adj_x][adj_y].flipped == False :
				grids[adj_x][adj_y].flip() # flip up the grid
				updated.append((adj_x, adj_y))
				if grids[adj_x][adj_y].adj_bomb == 0 : # if the grid has no adjancy bombs, push into queue
					que.append((adj_x, adj_y))
			
	return updated