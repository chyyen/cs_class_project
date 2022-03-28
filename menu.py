import pygame 
from pygame.locals import *
from init import mainWindow
from inGame import runGame


def drawMenuPage() :
	global mainWindow
	mainWindow.fill((255,255,255))

	title_font = pygame.font.Font('fonts/ComicRelief.ttf', 60) 
	
	_8to8 = title_font.render('Press 1 to enter a 8*8 map (with 10 mines)', True, (0,0,0))
	_16to16 = title_font.render('Press 2 to enter a 16*16 map (with 10 mines)', True, (0,0,0))
	_16to30 = title_font.render('Press 3 to enter a 16*30 map (with 10 mines)', True, (0,0,0))
	_quit = title_font.render('Press esc to quit the game', True, (0,0,0))
	
	mainWindow.blit(_8to8, _8to8.get_rect(center=(800,290)))
	mainWindow.blit(_16to16, _16to16.get_rect(center=(800,420)))
	mainWindow.blit(_16to30, _16to30.get_rect(center=(800,550)))
	mainWindow.blit(_quit, _quit.get_rect(center=(800,680)))

	pygame.display.flip()



while True :
	drawMenuPage()
	for event in pygame.event.get() :
		if event.type == QUIT :
			pygame.quit()
			exit()
		if event.type == KEYDOWN :
			if event.key == K_ESCAPE :
				pygame.quit()
				exit()
			elif event.key == K_1 :
				runGame(8, 8, 10)
			elif event.key == K_2 :
				runGame(16, 16, 50)
			elif event.key == K_3 :
				runGame(16, 30, 99)	
