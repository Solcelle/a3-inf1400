import pygame
pygame.font.init()

# Display
SCREEN_X = 1080
SCREEN_Y = 720
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

# Tickrate
GAME_TICK = 144
clock = pygame.time.Clock()

BACKGROUND_COLOR = (20, 22, 30)

# Block
BLOCK_COLOR = (120, 120, 160)
TILE_SIZE = 40


# Player 2
P1_CONTROLS = 1	# W, A, D, SPACE
P1_COLOR = (200, 150, 0)
P1_SPAWN = pygame.Vector2(140, 200)
P1_TOP_BAR = pygame.Vector2(43, 10)

# Player 2
P2_CONTROLS = 2	# UP, LEFT, RIGHT, L-CTRL
P2_COLOR = (100, 0, 100)
P2_SPAWN = pygame.Vector2(940, 520)
P2_TOP_BAR = pygame.Vector2(764, 10)

# Player general
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 20
PLAYER_SPEED = 300
BREAK_SPEED = 0.98
ACCEL_SPEED = 0.008
CRASH_SPEED = 0.5
ROTATION_SPEED = 200

# Fuel
FUEL_GAUGE_HEIGHT = 20
FUEL_GAUGE_WIDTH = 157
FUEL_DELAY = 10

# Bullet
BULLET_HEIGHT = 4
BULLET_WIDTH = 4
BULLET_SPEED = 500
BULLET_COLOR = (150, 150, 150)
BULLET_DELAY = 1

GRAVITY = 0.014

# Image imports
explosion_img = pygame.image.load("explosion.png").convert_alpha()
explosion_img = pygame.transform.scale(explosion_img, (40, 40))
fuel_can_img = pygame.image.load("fuel_can.png").convert_alpha()
fuel_can_img = pygame.transform.scale(fuel_can_img, (40, 40))
# spaceship_img = pygame.image.load("spaceship.png").convert_alpha()
# spaceship_img = pygame.transform.scale(spaceship_img, (40, 40))

font = pygame.font.SysFont("Impact", 30)
lives_txt = font.render('Lives:', True, (40, 40, 40))