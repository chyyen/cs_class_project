import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

mainWindow = pygame.display.set_mode((1600, 1000)) # main window
sound = pygame.mixer.Sound("sound/test.wav") # sound effect when fail

