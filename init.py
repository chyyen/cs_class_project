import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

mainWindow = pygame.display.set_mode((1600, 1000)) # main window
sound = pygame.mixer.Sound("sound/test.wav") # sound effect when fail
# common size of font
font30 = pygame.font.Font('fonts/ComicRelief.ttf', 30) 
font60 = pygame.font.Font('fonts/ComicRelief.ttf', 60) 
