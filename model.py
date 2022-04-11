from pygame.surface import Surface
from pygame.rect import Rect
from pygame.sprite import Sprite
from init import mainWindow

class Grid(Sprite) :
	def __init__(self, x_coor, y_coor, width, adj_bomb, unflipped_sur, flipped_sur, flag_sur, mark_sur) :
		# (x_coor, y_coor) : coordinate of left top
		# width : width of the grid
		# adj_bomb : number of bombs that are adjacent to the grid
		# {unflipped, flipped, flag, mark}_sur : surface showed when the it is true
		super(Grid, self).__init__()
		self.rect = Rect(x_coor, y_coor, width, width)
		self.width = width
		self.adj_bomb = adj_bomb # -1 if there is a bomb
		self.flipped = False
		self.unflipped_sur = unflipped_sur
		mainWindow.blit(self.unflipped_sur, self.rect)
		self.flipped_sur = flipped_sur # if not a bomb, it will be a text that shows {adj_bomb}
		self.flipped_sur.set_alpha(180)
		# two tags : question mark (mark) or flag (flag)
		self.flag = False
		self.flag_sur = flag_sur
		self.mark = False
		self.mark_sur = mark_sur

	def flip(self) :
		self.flipped = True
		has_tagged = self.flag or self.mark # return if there are tagged
		if self.adj_bomb == -1 : # if flip a bomb, return -1
			has_tagged = -1
		self.flag = False
		self.mark = False
		cover = Surface((self.width, self.width)) 
		cover.fill((255,255,255))
		cover.set_alpha(180)
		mainWindow.blit(cover, self.rect) # set a white background first
		mainWindow.blit(self.flipped_sur, self.flipped_sur.get_rect(center=self.rect.center))
		return has_tagged

	def change_tag(self) :
		mainWindow.blit(self.unflipped_sur, self.rect)
		if self.flag :
			self.flag = False
			self.mark = True
			mainWindow.blit(self.mark_sur, self.rect)
		elif self.mark :
			self.mark = False
		else :
			self.flag = True			
			mainWindow.blit(self.flag_sur, self.rect)