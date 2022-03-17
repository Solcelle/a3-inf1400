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

'''Draw object'''
class Draw_object():
	def draw_poligon(self):
		self.box = pygame.draw.polygon(config.screen, self.color, self.points)

'''Triangle'''
class Triangle(Object, Move_object, Draw_object):
	def __init__(self, x, y, height, width, speed, color):
		super().__init__(x, y, height, width, speed, color)
		self.vector_vel = pygame.math.Vector2(0, 0)
		self.center = (100, 100)
		self.points = ((self.vector_pos.x, self.vector_pos.y), (self.vector_pos.x + self.width / 2, self.vector_pos.y + self.height), (self.vector_pos.x - self.width / 2, self.vector_pos.y + self.height))
	
	def update(self):
		#self.points = ((self.vector_pos.x, self.vector_pos.y), (self.vector_pos.x + self.width / 2, self.vector_pos.y + self.height), (self.vector_pos.x - self.width / 2, self.vector_pos.y + self.height))
		self.points = self.rotate()
		self.draw_poligon()
	
	def rotate(self):
		mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
		angle = pygame.math.Vector2().angle_to(mouse_pos - self.center)
		
		rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in self.points]
		triangle_points = [(self.center + p) for p in rotated_point]
		return triangle_points

		

triangle = Triangle(0, 0, 20, 20, 100, (100, 0, 100))
triangle.vector_vel.x = 10

# Game loop
while True:
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