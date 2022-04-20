import pygame
import time
import config
import map
pygame.init()
pygame.font.init()


class Object():
	'''Class for objects (x, y, height, widht, color)'''
	def __init__(self, x: float, y: float, height, width, color):
		self.vector_pos = pygame.Vector2(x, y)
		self.height = height
		self.width = width
		self.color = color
		
class Moving_object(Object):
	'''Class for moving objects (x, y, height, width, speed, color)'''
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, color)
		self.speed = speed
		self.vector_vel = pygame.Vector2(0, 0)

	def move(self):
		'''Draws object on screen'''
		self.vector_pos += pygame.Vector2(self.vector_vel * self.speed * config.time_passed)	

class Draw_object():
	''' Class for drawing objects '''
	def draw_rect(self):
		'''Draws rectangle'''
		self.rect = pygame.draw.rect(config.screen, self.color, (self.vector_pos.x, self.vector_pos.y, self.width, self.height))
	def draw_fuel_amount(self):
		'''Draws fuel amount'''
		self.rect = pygame.draw.rect(config.screen, self.color, (self.vector_pos.x, self.vector_pos.y, self.fuel_amount, self.height))
	def draw_rect_border(self):
		'''Draws rectangle border'''
		self.rect = pygame.draw.rect(config.screen, self.border_color, (self.vector_pos.x - self.border, self.vector_pos.y - self.border, self.width + (self.border * 2), self.height + (self.border * 2)), self.border)
	def draw_poligon(self):
		'''Draws poligon'''
		self.rect = pygame.draw.polygon(config.screen, self.color, [p + self.vector_pos for p in self.points])
	def draw_circle(self):
		'''Draws cicle'''
		self.rect = pygame.draw.circle(config.screen, self.color, (self.vector_pos.x, self.vector_pos.y), self.width / 2)
	@staticmethod
	def draw_img(img, x, y):
		'''Draws image (image, (x, y))'''
		config.screen.blit(img, (x, y))

class Map():
	'''Class for game map'''
	def convert_map(self, map):
		'''Converts map file, takes in map file and returns list of blocks'''
		# Loops through rows
		blocks = []
		row = 0
		for list in map:
			# Loops through columns
			column = 0
			for tile in list:
				# If there is a tile it gets added to the block list
				if tile:
					blocks.append(Block(config.BLOCK_SIZE * column, config.BLOCK_SIZE * row, config.BLOCK_SIZE, config.BLOCK_SIZE, config.BLOCK_COLOR))
				column += 1
			row += 1
		return blocks

	def draw(self):
		'''Draws all blocks in block list, takes in list of blocks'''
		for block in blocks:
			block.draw_rect()

class Block(Object, Draw_object):
	'''Class for blocks, games obstacle '''
	def __init__(self, x, y, height, width, color):
		super().__init__(x, y, height, width, color)

class Bullet(Moving_object, Draw_object):
	'''Class for players bullet'''
	def __init__(self, x, y, height, width, speed, color, dir):
		super().__init__(x, y, height, width, speed, color)
		self.vector_vel = dir
		self.remove = False

	def update(self):
		'''Updates bullets position and draws it to screen'''
		self.move()				# Updates position
		self.draw_circle()		# Draws to screen
		
		# Removes bullet if collision with block
		for block in blocks: self.collision(block)

	def collision(self, other):
		'''Checks collision between bullet and object, if true bullet is removed'''
		if pygame.Rect.colliderect(self.rect, other.rect):
			self.remove = True

class Fuel_gauge(Object, Draw_object):
	'''Class for players fuel gauge, dispays players amount of fuel'''
	height = config.FUEL_GAUGE_HEIGHT
	width = config.FUEL_GAUGE_WIDTH
	def __init__(self, x, y, color):
		super().__init__(x, y, Fuel_gauge.height, Fuel_gauge.width, color)
		self.fuel_amount = Fuel_gauge.width
		self.use_fuel = False
		self.border = 3
		self.border_color = (60, 60, 60)
		self.fuel_consumption = 10
	
	def update(self):
		'''Updates fuel gauge, draws to screen and updates amount'''
		self.draw_rect_border()		# Draws border around fuel gauge
		self.draw_fuel_amount()		# Draws fuel amount in fuel gauge
		self.update_fuel_amount()	# Updates fuel amount
	
	def update_fuel_amount(self):
		'''Updates fuel amount'''
		if self.use_fuel:
			self.fuel_amount -= self.fuel_consumption * config.time_passed

class Fuel_can(Object, Draw_object):
	'''Class for fuel can, item that can be collected to refill fuel (x, y)'''
	def __init__(self, x, y):
		super().__init__(x, y, 40, 40, 0)
		self.draw_rect()
		self.collected = False
		self.time_collected = 0
		self.fuel_ready = False

	def update(self):
		'''Updates fuel cans timer and draws it to the screen'''
		# Draw if not collected
		if not self.collected:
			self.draw_img(config.fuel_can_img, self.vector_pos.x, self.vector_pos.y)
		# Else start a timer
		else:
			self.timer()
	
	def timer(self):
		'''Starts reset timer for fuel can'''
		# Check if next fuel can ready
		if time.time() > (self.time_collected + config.FUEL_DELAY):
			self.fuel_ready = True
		# Spawn fuel if next fuel ready
		if self.fuel_ready:
			self.collected = False
			self.time_collected = time.time()
			self.fuel_ready = False

class Player(Moving_object, Draw_object):
	'''Class for player (x, y, color, hud position)'''
	def __init__(self, x, y, color, hud_pos):
		super().__init__(x, y, config.PLAYER_HEIGHT, config.PLAYER_WIDTH, config.PLAYER_SPEED, color)
		self.points = (pygame.Vector2(0, self.height * -0.75), pygame.Vector2(self.width / 2, self.height * 0.25), pygame.Vector2(self.width / -2, self.height * 0.25))
		self.spawn = pygame.Vector2(x, y)
		self.keys = [False, False, False, False, False]
		self.score = 0
		self.start = False
		self.explode = (False, 0, 0)
		self.bullet_ready = True
		self.bullet_time = 0
		self.bullets = []
		self.hud_pos = hud_pos
		self.fuel = Fuel_gauge(hud_pos.x, hud_pos.y, self.color)

	def update(self):
		'''Updates players positon, hud, collisions, etc.'''
		self.player_inputs()									# Executes player inputs
		self.explosion()										# Draw players explosion
		self.draw_poligon()										# Draw player
		self.hud()												# Updates players hud info
		if self.start: self.move()								# Move player
		for block in blocks: self.check_collision(block)		# Check collisions with blocks
		for item in items: self.check_collect(item)
		
		# Check player collisions
		for other in players:
			# Player can't hit itself
			if other != self:
				# Check if players collide
				if hasattr(other, 'rect'): self.check_collision(other)

				# Loop through players bullets
				for bullet in self.bullets:
					bullet.update()	

					# Check if player hit other
					if other.check_collision(bullet):
						self.score += config.SCORE_AMOUNT	# Increase score
						self.bullets.remove(bullet)			# Remove bullet

	def player_inputs(self):
		'''Excecutes players inputs'''
		# If thrust...
		if self.keys[0] and self.fuel.fuel_amount > 0:	
			thrust_dir = self.points[0].normalize()
			self.vector_vel.x += thrust_dir.x * config.ACCEL_SPEED
			self.vector_vel.y += thrust_dir.y * (config.ACCEL_SPEED * 4)
			self.start = True
			self.fuel.use_fuel = True
		# Else reduce speed and add gravity
		else:
			self.vector_vel *= config.BREAK_SPEED
			self.gravity()
			self.fuel.use_fuel = False
		# If left...
		if self.keys[1]:
			# Rotate left
			self.points = [pygame.Vector2(p).rotate(-config.ROTATION_SPEED * config.time_passed) for p in self.points]
		# If right...
		if self.keys[3]:
			# Rotate right
			self.points = [pygame.Vector2(p).rotate(config.ROTATION_SPEED * config.time_passed) for p in self.points]
		# If shoot...
		if self.keys[2]:
			# Check if next bullet ready
			if time.time() > (self.bullet_time + config.BULLET_DELAY):
				self.bullet_ready = True
			# Fire bullet if next bullet ready
			if self.bullet_ready:
				# Adds bullet to players bullet list
				self.bullets.append(Bullet(self.vector_pos.x, self.vector_pos.y, config.BULLET_HEIGHT, config.BULLET_WIDTH, config.BULLET_SPEED, config.BULLET_COLOR, self.points[0].normalize()))
				# Reset timer
				self.bullet_time = time.time()	
				self.bullet_ready = False

	def gravity(self):
		'''Adds gravity to players velocity'''
		self.vector_vel.y += config.GRAVITY

	def player_respawn(self):
		'''Respawns player and updates'''
		self.explode = (True, self.vector_pos.x, self.vector_pos.y)		# Sets explotion at current position
		self.vector_pos = pygame.Vector2(self.spawn.x, self.spawn.y)	# Sets positon to spawn
		self.vector_vel = pygame.Vector2(0, 0)							# Reset velocity
		self.fuel.fuel_amount = self.fuel.width							# Reset fuel
		self.score -= config.SCORE_AMOUNT								# Reduces score
		self.start = False												# Makes player stand still when respawn

	def hud(self):
		'''Updates hud with player info'''
		# Update fuel gauge
		self.fuel.update()

		# Draw score
		self.draw_img(config.score_txt, self.hud_pos.x + 180, self.hud_pos.y - 10)						# Draws score text
		num_score_txt = pygame.font.SysFont("Impact", 30).render(str(self.score), True, (40, 40, 40))	# Converts numb score to text
		self.draw_img(num_score_txt, self.hud_pos.x + 260, self.hud_pos.y - 10)							# Draws numb score text

	def check_collision(self, other):
		'''Checks players collision with other object and if so respawns player'''
		if pygame.Rect.colliderect(self.rect, other.rect):
			self.player_respawn()
			return True
		return False

	def check_collect(self, item):
		'''Checks if player collects an item'''
		if pygame.Rect.colliderect(self.rect, item.rect) and not item.collected:
			self.fuel.fuel_amount = self.fuel.width
			item.collected = True

	def explosion(self):
		'''Checks if player has exploded and if so draws explotion'''
		if self.explode[0]:
			self.draw_img(config.explosion_img, self.explode[1] - (config.BLOCK_SIZE / 2), self.explode[2] - (config.BLOCK_SIZE / 2))

players = [Player(config.P1_SPAWN.x, config.P1_SPAWN.y, config.P1_COLOR, config.P1_TOP_HUD), Player(config.P2_SPAWN.x, config.P2_SPAWN.y, config.P2_COLOR, config.P2_TOP_HUD)]
items = [Fuel_can(565, 90), Fuel_can(445, 550)]
map1 = Map()
blocks = map1.convert_map(map.map1)