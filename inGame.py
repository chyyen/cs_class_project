from pip import main
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
	img = pygame.image.load(f'imgs/covered{row}.jpg')
	for i in range(row) :
		for j in range(column) :
			mainWindow.blit(img, (gap+j*width+2, 100+i*width+2))
		
	pygame.display.flip()


# draw grid
def drawGrid(grids, row, updated_grids) :
	global mainWindow, width, gap

	# draw grid content	
	for r,c in updated_grids :
		grid = grids[r][c]
		print(r,c,grid.flipped)
		if grid.flipped == False : # add tag
			pass
		else : # flip 
			img = pygame.image.load(f'imgs/blank{row}.png') # draw grid to white
			mainWindow.blit(img, (grid.x_coor, grid.y_coor))
			# draw the number of adjacent bombs
			if grid.adj_bomb > 0 : 
				font = pygame.font.Font('fonts/ComicRelief.ttf', width//2)
				num = font.render(f'{grid.adj_bomb}', True, (0,0,0))
				rect = num.get_rect(center=((2*grid.x_coor+width)//2, (2*grid.y_coor+width)//2))
				mainWindow.blit(num, rect)
			# there's a bomb
			if grid.adj_bomb == -1 : 
				img = pygame.image.load(f'imgs/bomb{row}.png')
				mainWindow.blit(img, (grid.x_coor, grid.y_coor))

	pygame.display.flip()


# check wheather there are bomb flipped
def check_no_bomb(last_flipped, grids) :
	for x,y in last_flipped :
		if grids[x][y].adj_bomb == -1 :
			return False
	return True


# main part
def runGame(row_size, col_size, bomb_num) :
	global mainWindow, width, gap

	# generate map
	grids, width, gap = generateMap(row_size, col_size, bomb_num)
	updated = [] # grids that are changed
	remain = row_size*col_size-bomb_num

	# initialize the grids
	initGrid(row_size, col_size)

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
					# bfs to update grid's state
					if y >= 0 and y < row_size and x >= 0 and x < col_size and grids[y][x].flipped == False:
						updated = bfs(grids, row_size, col_size , y, x) 
						remain -= len(updated)
				# right click
				else : 
					if y >= 0 and y < row_size and x >= 0 and x < col_size and grids[y][x].flipped == False:
						grids[y][x].add_tag()
						updated = [(y,x)]

		drawGrid(grids,row_size, updated) # update surfaces

	# end game
	endPage = pygame.Surface((1600,1000))
	endPage.fill((255, 255, 255))
	endPage.set_alpha(180)
	mainWindow.blit(endPage, (0,0))
	font = pygame.font.Font('fonts/ComicRelief.ttf', 60) 
	text1 = font.render("You lose" if remain else "You win", True, (0,0,0))
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

