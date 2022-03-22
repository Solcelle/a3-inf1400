import pygame

# Display
SCREEN_X = 1000
SCREEN_Y = 700
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y), 0, 32)

# Tickrate
GAME_TICK = 144
clock = pygame.time.Clock()

# Color
BACKGROUND_COLOR = (20, 22, 30)