''' This module porvides variables for the Mayhem game '''

import pygame
pygame.font.init()

# Display
SCREEN_X = 1080
SCREEN_Y = 720
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)


# General
GAME_TICK = 144
clock = pygame.time.Clock()
BACKGROUND_COLOR = (20, 22, 30)
GRAVITY = 0.014
SCORE_AMOUNT = 100


# Player General
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 20
PLAYER_SPEED = 300
BREAK_SPEED = 0.98
ACCEL_SPEED = 0.008
CRASH_SPEED = 0.5
ROTATION_SPEED = 250

# Player 1
P1_CONTROLS = 1	# W, A, D, SPACE
P1_COLOR = (200, 150, 0)
P1_SPAWN = pygame.Vector2(140, 200)
P1_TOP_HUD = pygame.Vector2(43, 10)

# Player 2
P2_CONTROLS = 2	# UP, LEFT, RIGHT, L-CTRL (or L-SHIFT)
P2_COLOR = (100, 0, 100)
P2_SPAWN = pygame.Vector2(940, 520)
P2_TOP_HUD = pygame.Vector2(720, 10)


# Block
BLOCK_COLOR = (120, 120, 160)
BLOCK_SIZE = 40


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


# Image imports
explosion_img = pygame.image.load("explosion.png").convert_alpha()
explosion_img = pygame.transform.scale(explosion_img, (40, 40))
fuel_can_img = pygame.image.load("fuel_can.png").convert_alpha()
fuel_can_img = pygame.transform.scale(fuel_can_img, (40, 40))

# Text
font = pygame.font.SysFont("Impact", 30)
score_txt = font.render('Score:', True, (40, 40, 40))