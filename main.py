import config
import pygame
import classes
pygame.init()

def main():
	# Game loop
	while main:
		# Checks for events
		check_events()

		# Set amount of updates per second
		config.time_passed = config.clock.tick(config.GAME_TICK) / 1000.0

		# Set background colour
		config.screen.fill(config.BACKGROUND_COLOR)

		# Draw map
		classes.map1.draw()

		# Update players
		for player in classes.players: player.update()

		# Update items
		for item in classes.items: item.update()

		# Update display too show new frame
		pygame.display.update()

def check_events():
	'''Checks for game events and executes accordingly'''
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
				classes.players[0].keys[0] = True
			if event.key == pygame.K_a:
				classes.players[0].keys[1] = True
			if event.key == pygame.K_SPACE:
				classes.players[0].keys[2] = True
			if event.key == pygame.K_d:
				classes.players[0].keys[3] = True
			
			# Player2 keys
			if event.key == pygame.K_UP:
				classes.players[1].keys[0] = True
			if event.key == pygame.K_LEFT:
				classes.players[1].keys[1] = True
			if event.key == pygame.K_RCTRL:
				classes.players[1].keys[2] = True
			if event.key == pygame.K_RIGHT:
				classes.players[1].keys[3] = True

		# Check if a key is relesed
		if event.type == pygame.KEYUP:
			# Player1 keys
			if event.key == pygame.K_w:
				classes.players[0].keys[0] = False
			if event.key == pygame.K_a:
				classes.players[0].keys[1] = False
			if event.key == pygame.K_SPACE:
				classes.players[0].keys[2] = False
			if event.key == pygame.K_d:
				classes.players[0].keys[3] = False
			
			# Player2 keys
			if event.key == pygame.K_UP:
				classes.players[1].keys[0] = False
			if event.key == pygame.K_LEFT:
				classes.players[1].keys[1] = False
			if event.key == pygame.K_RCTRL:
				classes.players[1].keys[2] = False
			if event.key == pygame.K_RIGHT:
				classes.players[1].keys[3] = False

if __name__ == '__main__':
	main()