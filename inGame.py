import pygame
from pygame.locals import *
from datetime import datetime
from generator import generateMap
from bfs import bfs
from init import mainWindow, sound


width = int(0) # grid width 
gap = int(0) # blank space of left and right side


def initGrid(row, column) :
	global mainWindow, width, gap

	# build vertical lines
	for i in range(column+1) :
		line = pygame.Rect(gap+i*width, 100, 2, width*row+1)
		pygame.draw.rect(mainWindow, (0, 0, 0), line)

	# build horizontal lines
	for i in range(row+1) :
		line = pygame.Rect(gap, 100+i*width, width*column+1, 2)
		pygame.draw.rect(mainWindow, (0, 0, 0), line)


def show_bomb_num(num) :
	global mainWindow
	cover = pygame.Surface((400, 50)) # a new surface to show text
	cover.fill((255,255,255))
	mainWindow.blit(cover, (1200, 950))
	font = pygame.font.Font('fonts/ComicRelief.ttf', 30) 
	text = font.render(f"Remaining bombs : {num}", True, (0,0,0)) # text showimg remaining bombs
	rect = text.get_rect(right=1590, bottom=990)
	mainWindow.blit(text, rect)


def update_time(period) :
	global mainWindow
	if period < 0 : # new day 
		period += 24*60*60
	cover = pygame.Surface((400, 50)) # a new surface to show current time
	cover.fill((255,255,255))
	mainWindow.blit(cover, (0, 0))
	font = pygame.font.Font('fonts/ComicRelief.ttf', 30) 
	text = font.render(f"Time : {period//60}min {period%60}sec", True, (0,0,0)) # text showimg current time
	rect = text.get_rect(left=10, top=10)
	mainWindow.blit(text, rect)
		


def runGame(row_size, col_size, bomb_num) :
	global mainWindow, width, gap

	mainWindow.fill((255, 255, 255))
	 
	# generate map
	grids, width, gap = generateMap(row_size, col_size, bomb_num)

	# initialize the grids
	initGrid(row_size, col_size)
	show_bomb_num(bomb_num)

	remain = row_size*col_size-bomb_num # remaing grid without bomb
	start_time = datetime.today().hour*3600+datetime.today().minute*60+datetime.today().second # use to compute current play time
	update_time(datetime.today().hour*3600+datetime.today().minute*60+datetime.today().second-start_time) 
	
	pygame.display.flip()

	boom = False # wheather flip a bomb

	# main part of game
	while (not boom) and remain :
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
					if y >= 0 and y < row_size and x >= 0 and x < col_size and grids[y][x].flipped == False and grids[y][x].flag == False and grids[y][x].mark == False :
						flipped_num, res = bfs(grids, row_size, col_size , y, x) # return (the number of girds be flipped, the number of grids that is tagged and flipped)
						if res == -1 : # flip a bomb
							boom = True 
						else :
							bomb_num += res
						remain -= flipped_num
				# right click
				else : 
					if y >= 0 and y < row_size and x >= 0 and x < col_size and grids[y][x].flipped == False:
						grids[y][x].change_tag()
						if grids[y][x].flag == True : # use to show the number of bomb that haven't been flagged 
							bomb_num -= 1
						elif not grids[y][x].mark :
							bomb_num += 1
		update_time(datetime.today().hour*3600+datetime.today().minute*60+datetime.today().second-start_time)
		show_bomb_num(bomb_num)
		pygame.display.flip()

	# end game
	# show a text to imform player, and wait player to exit
	if boom :
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

