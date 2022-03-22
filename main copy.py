import vector
import config
import random
import pygame
import math

'''Object'''
class Object():
	def __init__(self, x: float, y: float, height, width, speed, color):
		self.vector_pos = pygame.math.Vector2(x, y)
		self.height = height
		self.width = width
		self.speed = speed
		self.color = color
		
'''Move object'''
class Move_object():
	def move(self):
		self.vector_pos += pygame.math.Vector2(self.vector_vel * self.speed * time_passed)

'''Draw object'''
class Draw_object():
	def draw_poligon(self):
		pygame.draw.polygon(config.screen, self.color, [p + self.vector_pos for p in self.points])

'''Triangle'''
class Triangle(Object, Move_object, Draw_object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, speed, color)
		self.keys = [False, False, False, False, False]
		self.direction = 0
		self.vector_vel = pygame.math.Vector2(0, 0)
		self.center = pygame.math.Vector2(x, (y + (self.height * 0.75)))
		self.points = (pygame.math.Vector2(0, self.height * 0.75), pygame.math.Vector2(self.width / 2, self.height * -0.25), pygame.math.Vector2(self.width / -2, self.height * -0.25))
		self.rot_speed = 4

	def update(self):
		self.player_inputs()			# Executes player inputs
		self.move()						# Move object
		self.player_direction()			# Sets objects direction
		self.rotate(self.rot_speed)		# Rotate object
		self.draw_poligon()				# Draw object
	
	# Rotates object by angle(-180 to 180)
	def rotate(self, angle):
		self.points = [pygame.math.Vector2(p).rotate(angle) for p in self.points]
	
	def player_direction(self):
		# radians = math.atan2(self.vector_vel.y - self.vector_pos.y, self.vector_vel.x - self.vector_pos.x)
		# self.direction = (math.cos(radians), math.sin(radians))
		self.direction = pygame.math.Vector2(0, 0).angle_to(self.vector_vel - self.vector_pos)
	
	# Executes players inputs
	def player_inputs(self):
		if any(self.keys):
			if self.keys[0]:	# W
				self.vector_vel += pygame.math.Vector2(0, -3)
			if self.keys[1]:	# A
				self.vector_vel += pygame.math.Vector2(-3, 0)
			if self.keys[2]:	# S
				self.vector_vel += pygame.math.Vector2(0, 3)
			if self.keys[3]:	# D
				self.vector_vel += pygame.math.Vector2(3, 0)
		else:
			self.vector_vel -= (self.vector_vel / 20)



def check_events():
	# Check for events
	events = pygame.event.get()
	for event in events:
		
		# Quits game if window is closed
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			# Quit game with ESC
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			if event.key == pygame.K_w:
				p1.keys[0] = True
			if event.key == pygame.K_a:
				p1.keys[1] = True
			if event.key == pygame.K_s:
				p1.keys[2] = True
			if event.key == pygame.K_d:
				p1.keys[3] = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				p1.keys[0] = False
			if event.key == pygame.K_a:
				p1.keys[1] = False
			if event.key == pygame.K_s:
				p1.keys[2] = False
			if event.key == pygame.K_d:
				p1.keys[3] = False


p1 = Triangle(100, 100, 30, 20, 5, (100, 0, 100))

# Game loop
while True:
	# Checks for events
	check_events()

	# Sets amount of updates per second
	time_passed = config.clock.tick(config.GAME_TICK) / 1000.0

	# Set background colour
	config.screen.fill(config.BACKGROUND_COLOR)

	# Update boids, hoiks and obstacles
	# for obj in objects:
	# 	obj.update()
	p1.update()

	# Update display too show new frame
	pygame.display.update()