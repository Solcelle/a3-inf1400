import config
import map
import pygame

'''Object'''
class Object():
	def __init__(self, x: float, y: float, height, width, color):
		self.vector_pos = pygame.math.Vector2(x, y)
		self.height = height
		self.width = width
		self.color = color
		
'''Moving object'''
class Moving_object(Object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, color)
		self.speed = speed

	def move(self):
		if self.vector_vel.x != 0 or self.vector_vel.y != 0:
			self.vector_vel = pygame.math.Vector2.normalize(self.vector_vel)
		self.vector_pos += pygame.math.Vector2(self.vector_vel * self.speed * time_passed)
		if self.respawn:
			self.vector_pos = pygame.math.Vector2(self.spawn.x, self.spawn.y)
			self.respawn = False

'''Draw object'''
class Draw_object():
	def draw_rect(self):
		self.rect = pygame.draw.rect(config.screen, self.color, (self.vector_pos.x, self.vector_pos.y, self.width, self.height))
	def draw_poligon(self):
		self.rect = pygame.draw.polygon(config.screen, self.color, [p + self.vector_pos for p in self.points])
	@staticmethod
	def draw_img(img, x, y):
		config.screen.blit(img, (x, y))

'''Map'''
class Map():
	# Creates a map of blocks
	def create(self):
		# Loops through rows
		row = 0
		for list in map.map1:
			# Loops through columns
			column = 0
			for tile in list:
				# If there is a tile it gets added to the block list
				if tile:
					blocks.append(Block(tile_size * column, tile_size * row, tile_size, tile_size, config.BLOCK_COLOR))
				column += 1
			row += 1

	# Draws all tiles in block list
	def draw(self):
		for block in blocks:
			block.draw_rect()

'''Block'''
class Block(Object, Draw_object):
	def __init__(self, x, y, height, width, color):
		super().__init__(x, y, height, width, color)

'''Player'''
class Player(Moving_object, Draw_object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, speed, color)
		self.points = (pygame.math.Vector2(0, self.height * 0.75), pygame.math.Vector2(self.width / 2, self.height * -0.25), pygame.math.Vector2(self.width / -2, self.height * -0.25))
		self.keys = [False, False, False, False, False]
		self.vector_vel = pygame.math.Vector2(0, 0)
		self.rot_speed = 400
		self.lives = 3
		self.spawn = pygame.math.Vector2(x, y)
		self.respawn = False
		self.explode = (False, 0, 0)

	def update(self):
		self.player_inputs()			# Executes player inputs
		self.move()						# Move object
		self.draw_poligon()				# Draw object
		for block in blocks: player.check_collision(block)
		self.explosion()
	
	# Executes players inputs
	def player_inputs(self):
		if any(self.keys):
			if self.keys[0]:	# Thrust
				self.vector_vel += self.points[0]
			else:
				self.vector_vel = pygame.math.Vector2(0, 0)
			if self.keys[1]:	# Rotate left
				self.points = [pygame.math.Vector2(p).rotate(-self.rot_speed * time_passed) for p in self.points]
			if self.keys[2]:	# Shoot
				pass
			if self.keys[3]:	# Right
				self.points = [pygame.math.Vector2(p).rotate(self.rot_speed * time_passed) for p in self.points]
		else:
			self.vector_vel = pygame.math.Vector2(0, 0)

	def check_collision(self, other):
		if pygame.Rect.colliderect(self.rect, other.rect):
			self.explode = (True, self.vector_pos.x, self.vector_pos.y)
			self.respawn = True
			self.lives -= 1
	
	def explosion(self):
		if self.explode[0]:
			self.draw_img(config.explosion_img, self.explode[1] - (tile_size / 2), self.explode[2] - (tile_size / 2))

def check_events():
	# Check for events
	events = pygame.event.get()
	for event in events:
		
		# Quits game if window is closed
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# Check if a key is pressed
		if event.type == pygame.KEYDOWN:
			# Quit game with ESC
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			# Player1 keys
			if event.key == pygame.K_w:
				players[0].keys[0] = True
			if event.key == pygame.K_a:
				players[0].keys[1] = True
			if event.key == pygame.K_s:
				players[0].keys[2] = True
			if event.key == pygame.K_d:
				players[0].keys[3] = True
			
			# Player2 keys
			if event.key == pygame.K_UP:
				players[1].keys[0] = True
			if event.key == pygame.K_LEFT:
				players[1].keys[1] = True
			if event.key == pygame.K_DOWN:
				players[1].keys[2] = True
			if event.key == pygame.K_RIGHT:
				players[1].keys[3] = True

		# Check if a key is relesed
		if event.type == pygame.KEYUP:
			# Player1 keys
			if event.key == pygame.K_w:
				players[0].keys[0] = False
			if event.key == pygame.K_a:
				players[0].keys[1] = False
			if event.key == pygame.K_s:
				players[0].keys[2] = False
			if event.key == pygame.K_d:
				players[0].keys[3] = False
			
			# Player2 keys
			if event.key == pygame.K_UP:
				players[1].keys[0] = False
			if event.key == pygame.K_LEFT:
				players[1].keys[1] = False
			if event.key == pygame.K_DOWN:
				players[1].keys[2] = False
			if event.key == pygame.K_RIGHT:
				players[1].keys[3] = False

tile_size = 40

players = [Player(100, 100, 30, 20, 400, (100, 0, 100)), Player(900, 620, 30, 20, 400, (100, 0, 100))]
blocks = []
map1 = Map()
map1.create()


# Game loop
while True:
	# Checks for events
	check_events()

	# Sets amount of updates per second
	time_passed = config.clock.tick(config.GAME_TICK) / 1000.0

	# Set background colour
	config.screen.fill(config.BACKGROUND_COLOR)

	# Draw map
	map1.draw()

	# Update players
	for player in players: player.update()

	# Update display too show new frame
	pygame.display.update()