import vector
import config
import random
import pygame

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
		self.vector_pos.x += self.vector_vel.x * self.speed * time_passed
		self.vector_pos.y += self.vector_vel.y * self.speed * time_passed
	def move_dist(self):
		return pygame.math.Vector2(self.vector_vel * self.speed * time_passed)

'''Draw object'''
class Draw_object():
	def draw_poligon(self):
		pygame.draw.polygon(config.screen, self.color, self.points)

'''Triangle'''
class Triangle(Object, Move_object, Draw_object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, speed, color)
		self.vector_vel = pygame.math.Vector2(0, 0)
		self.center = pygame.math.Vector2(x, y + (self.height * 0.75))
		self.points = (pygame.math.Vector2(self.vector_pos.x, self.vector_pos.y), pygame.math.Vector2(self.vector_pos.x + self.width / 2, self.vector_pos.y + self.height), pygame.math.Vector2(self.vector_pos.x - self.width / 2, self.vector_pos.y + self.height))
		self.rot_speed = 4

	def update(self):
		# Move object
		self.move_points(self.move_dist())
		# Rotate object
		self.points = self.rotate(self.rot_speed)
		# Draw object
		self.draw_poligon()
	
	def rotate(self, angle):
		rotated_points = []
		for p in self.points:
			p -= self.center							# Set points around origin
			p = pygame.math.Vector2(p).rotate(angle)	# Rotate points
			p += self.center							# Set rotated points around original position
			rotated_points.append(p)
		return rotated_points
	
	def move_points(self, dist):
		self.points = [p + dist for p in self.points]
		self.center += dist

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


triangle = Triangle(100, 100, 20, 20, 5, (100, 0, 100))
triangle.vector_vel.x = 10

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
	triangle.update()

	# Update display too show new frame
	pygame.display.update()