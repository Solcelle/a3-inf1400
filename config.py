import pygame

# Display
SCREEN_X = 1080
SCREEN_Y = 720
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

# Tickrate
GAME_TICK = 144
clock = pygame.time.Clock()

BACKGROUND_COLOR = (20, 22, 30)

TILE_SIZE = 40

# Block
BLOCK_COLOR = (120, 120, 160)

# Player
P1_CONTROLS = 1	# W, A, D, SPACE
P2_CONTROLS = 2	# UP, LEFT, RIGHT, L-CTRL
PLAYER_SPEED = 300
BREAK_SPEED = 0.98
ACCEL_SPEED = 0.006
CRASH_SPEED = 0.5
ROTATION_SPEED = 400

# Bullet
BULLET_HEIGHT = 4
BULLET_WIDTH = 4
BULLET_SPEED = 400
BULLET_COLOR = (150, 150, 150)
BULLET_DELAY = 1


GRAVITY = 0.014
explosion_img = pygame.image.load("explosion.png").convert_alpha()
explosion_img = pygame.transform.scale(explosion_img, (40, 40))
spaceship_img = pygame.image.load("spaceship.png").convert_alpha()
spaceship_img = pygame.transform.scale(spaceship_img, (40, 40))