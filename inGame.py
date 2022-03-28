import pygame
from pygame.locals import *
from generator import generateMap
from bfs import bfs
from init import mainWindow, sound


width = int(0) # grid width 
gap = int(0) # blank space of left and right side


def initGrid(row, column) :
	global mainWindow, width, gap
	mainWindow.fill((255,255,255))

	# build vertical lines
	for i in range(column+1) :
		line = pygame.Rect(gap+i*width, 100, 2, width*row+1)
		pygame.draw.rect(mainWindow, (0, 0, 0), line)

	# build horizontal lines
	for i in range(row+1) :
		line = pygame.Rect(gap, 100+i*width, width*column+1, 2)
		pygame.draw.rect(mainWindow, (0, 0, 0), line)

	# draw image to grids
	img = pygame.image.load(f'imgs/size_{row}/cover.jpg')
	for i in range(row) :
		for j in range(column) :
			mainWindow.blit(img, (gap+j*width+2, 100+i*width+2))

	# show way to return to menu
	font = pygame.font.Font('fonts/ComicRelief.ttf', 30) 
	text = font.render("Press esc to return to menu", True, (0,0,0))
	mainWindow.blit(text, (10, 1570))

	pygame.display.flip()


# draw grid
def drawGrid(grids, row, updated_grids) :
	global mainWindow, width, gap
	# draw grid content	
	for r,c in updated_grids :
		grid = grids[r][c]
		if grid.flipped == False : # add (or cancel) tag
			img = pygame.image.load(f'imgs/size_{row}/cover.jpg')
			mainWindow.blit(img, (grid.x_coor, grid.y_coor))
			if grid.flag == True : # tag is flag
				img = pygame.image.load(f'imgs/size_{row}/flag.png')
				mainWindow.blit(img, (grid.x_coor, grid.y_coor))
			elif grid.marked == True : # tag is question mark
				img = pygame.image.load(f'imgs/size_{row}/Qmark.png')
				mainWindow.blit(img, (grid.x_coor, grid.y_coor))
		else : # flip
			whiteBG = pygame.Surface((width-2, width-2)) # draw grid to white
			whiteBG.fill((255, 255, 255))
			whiteBG.set_alpha(180)
			mainWindow.blit(whiteBG, (grid.x_coor, grid.y_coor))
			if grid.adj_bomb > 0 : # draw the number of adjacent bombs
				font = pygame.font.Font('fonts/ComicRelief.ttf', width//2)
				num = font.render(f'{grid.adj_bomb}', True, (0,0,0))
				rect = num.get_rect(center=((2*grid.x_coor+width)//2, (2*grid.y_coor+width)//2))
				mainWindow.blit(num, rect)
			if grid.adj_bomb == -1 : # there's a bomb
				img = pygame.image.load(f'imgs/size_{row}/bomb.png')
				mainWindow.blit(img, (grid.x_coor, grid.y_coor))


def show_bomb_num(num) :
	global mainWindow
	cover = pygame.Surface((400, 50)) # a new surface to show text
	cover.fill((255,255,255))
	mainWindow.blit(cover, (1200, 950))
	font = pygame.font.Font('fonts/ComicRelief.ttf', 30) 
	text = font.render(f"Remaining bombs : {num}", True, (0,0,0)) # text showimg remaining bombs
	rect = text.get_rect(right=1590, bottom=990)
	mainWindow.blit(text, rect)


# check wheather there are bomb flipped
def check_no_bomb(last_flipped, grids) :
	for x,y in last_flipped :
		if grids[x][y].adj_bomb == -1 and grids[x][y].flipped == True :
			return False
	return True


def runGame(row_size, col_size, bomb_num) :
	global mainWindow, width, gap

	# generate map
	grids, width, gap = generateMap(row_size, col_size, bomb_num)

	updated = [] # grids that are changed
	remain = row_size*col_size-bomb_num # remaing grid without bomb

	# initialize the grids
	initGrid(row_size, col_size)
	show_bomb_num(bomb_num)
	
	# main part of game
	while check_no_bomb(updated, grids) and remain :
		updated = []
		# iterate through the events 
		for event in pygame.event.get() :
			if event.type == QUIT : # end game directly
				pygame.quit()
				exit()
			if event.type == KEYDOWN and event.key == K_ESCAPE : # return to menu
				return
			if event.type == MOUSEBUTTONDOWN : # operation to grids
				# get the clicked grid
				x, y = pygame.mouse.get_pos()
				x = (x-gap-2)//width
				y = (y-102)//width
				# left click
				if event.button == 1 : 
					# use bfs to update grid's state
					if y >= 0 and y < row_size and x >= 0 and x < col_size and grids[y][x].flipped == False and grids[y][x].flag == False and grids[y][x].marked == False:
						updated = bfs(grids, row_size, col_size , y, x) 
						remain -= len(updated)
				# right click
				else : 
					if y >= 0 and y < row_size and x >= 0 and x < col_size and grids[y][x].flipped == False:
						grids[y][x].add_tag()
						updated = [(y,x)]
						if grids[y][x].flag == True : # use to show the number of bomb that haven't been flagged 
							bomb_num -= 1
						elif not grids[y][x].marked :
							bomb_num += 1
		drawGrid(grids,row_size, updated) # update surfaces (flip, add tag to grid)
		if len(updated) > 0 :
			show_bomb_num(bomb_num)
		pygame.display.flip()

	# end game
	if remain :
		sound.play() # play juju sama's subbing sound if lose
	endPage = pygame.Surface((1600,1000)) # a new surface to show text
	endPage.fill((255, 255, 255))
	endPage.set_alpha(180)
	mainWindow.blit(endPage, (0,0))
	font = pygame.font.Font('fonts/ComicRelief.ttf', 60) 
	text1 = font.render("You lose" if remain else "You win", True, (0,0,0)) # text to show play result
	text2 = font.render("Press esc to return to menu", True, (0,0,0))
	rect1 = text1.get_rect(center=(800, 450))
	rect2 = text2.get_rect(center=(800, 550))
	mainWindow.blit(text1, rect1)
	mainWindow.blit(text2, rect2)
	pygame.display.flip()

	while True :
		for event in pygame.event.get() :
			if event.type == QUIT : # end game directly
				pygame.quit()
				exit()
			if event.type == KEYDOWN and event.key == K_ESCAPE : # return to menu
				return

