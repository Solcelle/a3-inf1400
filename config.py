import pygame

# Display
SCREEN_X = 1080
SCREEN_Y = 720
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

# Tickrate
GAME_TICK = 144
clock = pygame.time.Clock()

# Color
BACKGROUND_COLOR = (20, 22, 30)


# Block
BLOCK_COLOR = (120, 120, 160)

# Player
P1_CONTROLS = 1	# W, A, S, D
P2_CONTROLS = 2	# UP, LEFT, DOWN, RIGHT