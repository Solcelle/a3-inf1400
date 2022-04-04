import time
import config
import map
import pygame

'''Object'''
class Object():
	def __init__(self, x: float, y: float, height, width, color):
		self.vector_pos = pygame.Vector2(x, y)
		self.height = height
		self.width = width
		self.color = color
		
'''Moving object'''
class Moving_object(Object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, color)
		self.speed = speed
		self.vector_vel = pygame.Vector2(0, 0)

	def move(self):
		self.vector_pos += pygame.Vector2(self.vector_vel * self.speed * time_passed)	

'''Draw object'''
class Draw_object():
	def draw_rect(self):
		self.rect = pygame.draw.rect(config.screen, self.color, (self.vector_pos.x, self.vector_pos.y, self.width, self.height))
	def draw_poligon(self):
		self.rect = pygame.draw.polygon(config.screen, self.color, [p + self.vector_pos for p in self.points])
	def draw_circle(self):
		self.rect = pygame.draw.circle(config.screen, self.color, (self.vector_pos.x, self.vector_pos.y), self.width / 2)
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
					blocks.append(Block(config.TILE_SIZE * column, config.TILE_SIZE * row, config.TILE_SIZE, config.TILE_SIZE, config.BLOCK_COLOR))
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

'''Bullet'''
class Bullet(Moving_object, Draw_object):
	def __init__(self, x, y, height, width, speed, color, dir):
		super().__init__(x, y, height, width, speed, color)
		self.vector_vel = dir

	def update(self):
		self.move()
		self.draw_circle()
		
'''Player'''
class Player(Moving_object, Draw_object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, speed, color)
		self.points = (pygame.Vector2(0, self.height * -0.75), pygame.Vector2(self.width / 2, self.height * 0.25), pygame.Vector2(self.width / -2, self.height * 0.25))
		self.spawn = pygame.Vector2(x, y)
		self.start = False
		self.keys = [False, False, False, False, False]
		self.lives = 3
		self.respawn = False
		self.explode = (False, 0, 0)
		self.bullet_ready = True
		self.bullet_time = 0
		self.bullets = []

	def update(self):
		self.player_inputs()									# Executes player inputs
		if self.start: self.move()								# Move object
		self.explosion()										# Draw explosion
		self.player_respawn()									# Respawn object
		self.draw_poligon()										# Draw object
		for block in blocks: self.check_collision(block)		# Check collisions with blocks
		
		# Check if bullet hits
		for player in players:
			if player != self:
				for bullet in self.bullets:
					bullet.update()						# Update bullet
					player.check_collision(bullet)		# Check bullet collision with other players

	# Executes players inputs
	def player_inputs(self):
		# If thrust...
		if self.keys[0]:	
			thrust_dir = self.points[0].normalize()
			self.vector_vel.x += thrust_dir.x * config.ACCEL_SPEED
			self.vector_vel.y += thrust_dir.y * (config.ACCEL_SPEED * 4)
			self.start = True
		# Else reduce direction speed and add gravity
		else:
			self.vector_vel *= config.BREAK_SPEED
			self.gravity()
		# If rotate left...
		if self.keys[1]:
			self.points = [pygame.Vector2(p).rotate(-config.ROTATION_SPEED * time_passed) for p in self.points]
		# If rotate right...
		if self.keys[3]:
			self.points = [pygame.Vector2(p).rotate(config.ROTATION_SPEED * time_passed) for p in self.points]
		# If shoot...
		if self.keys[2]:
			# Check if next bullet ready
			if time.time() > (self.bullet_time + config.BULLET_DELAY):
				self.bullet_ready = True
			# Fire bullet if next bullet ready
			if self.bullet_ready:
				self.bullets.append(Bullet(self.vector_pos.x, self.vector_pos.y, config.BULLET_HEIGHT, config.BULLET_WIDTH, config.BULLET_SPEED, config.BULLET_COLOR, self.points[0].normalize()))
				self.bullet_time = time.time()
				self.bullet_ready = False

	# Adds gravity to player velocity
	def gravity(self):
		self.vector_vel.y += config.GRAVITY

	# Respawn player
	def player_respawn(self):
		if self.respawn:
			self.vector_pos = pygame.Vector2(self.spawn.x, self.spawn.y)
			self.vector_vel = pygame.Vector2(0, 0)
			self.respawn = False

	# Check for collision with rect
	def check_collision(self, other):
		if pygame.Rect.colliderect(self.rect, other.rect):
			self.explode = (True, self.vector_pos.x, self.vector_pos.y)
			self.respawn = True
			self.lives -= 1
			self.start = False
	
	# Check for explosion and draw explostion
	def explosion(self):
		if self.explode[0]:
			self.draw_img(config.explosion_img, self.explode[1] - (config.TILE_SIZE / 2), self.explode[2] - (config.TILE_SIZE / 2))

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
			if event.key == pygame.K_SPACE:
				players[0].keys[2] = True
			if event.key == pygame.K_d:
				players[0].keys[3] = True
			
			# Player2 keys
			if event.key == pygame.K_UP:
				players[1].keys[0] = True
			if event.key == pygame.K_LEFT:
				players[1].keys[1] = True
			if event.key == pygame.K_RCTRL:
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
			if event.key == pygame.K_SPACE:
				players[0].keys[2] = False
			if event.key == pygame.K_d:
				players[0].keys[3] = False
			
			# Player2 keys
			if event.key == pygame.K_UP:
				players[1].keys[0] = False
			if event.key == pygame.K_LEFT:
				players[1].keys[1] = False
			if event.key == pygame.K_RCTRL:
				players[1].keys[2] = False
			if event.key == pygame.K_RIGHT:
				players[1].keys[3] = False

players = [Player(100, 100, 30, 20, config.PLAYER_SPEED, (100, 0, 100)), Player(100, 200, 30, 20, config.PLAYER_SPEED, (100, 0, 100))]
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