import pygame

class Grid(pygame.sprite.Sprite) :
	def __init__(self, row, col, x_coor, y_coor, width, adj_bomb) :
		super(Grid, self).__init__()
		self.row = row
		self.col = col
		self.x_coor = x_coor
		self.y_coor = y_coor
		self.width = width
		self.adj_bomb = adj_bomb # -1 if there is a bomb
		self.flipped = False
		self.flag = False
		self.marked = False
	
	def __repr__(self) :
		return f"{self.adj_bomb}"

	def flip(self) :
		self.flipped = True

	def add_tag(self) :
		# two tags : question mark (marked) or flag (flag)
		if self.flag :
			self.flag = False
			self.marked = True
		elif self.marked :
			self.marked = False
		else :
			self.flag = True
