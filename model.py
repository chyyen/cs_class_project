class Grid() :
	def __init__(self, row, col, x_coor, y_coor, width, adj_bomb) :
		self.row = row
		self.col = col
		self.x_coor = x_coor
		self.y_coor = y_coor
		self.width = width
		self.adj_bomb = adj_bomb # -1 if there is a bomb
		self.flipped = False
		self.flag = False
		self.marked = False
		# two tags : question mark (marked) or flag (flag)

	def __repr__(self) :
		return f"{self.adj_bomb}"

	def flip(self) :
		self.flipped = True

	def add_tag(self) :
		if self.flag :
			self.flag = False
			self.marked = True
		elif self.marked :
			self.marked = False
		else :
			self.flag = True
