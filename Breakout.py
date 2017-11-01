import pygame, sys, os

from Entity import *
from Collision import *


def main():
	pygame.init()

	# Window
	size = width, height = 960, 540
	surface = pygame.display.set_mode(size, pygame.DOUBLEBUF)# | pygame.FULLSCREEN)

	# Timer
	clock = pygame.time.Clock()
	def_fps = 200
	max_fps = def_fps*2
	min_fps = def_fps/2

	# Mouse
	pygame.mouse.set_visible(False)
	pygame.event.set_grab(True)

	# Init
	initial = [True, 0]
	ball = Circle([pygame.mouse.get_pos()[0], (49/54)*height], ((1/54)*height, 0), (0,255,0), surface)
	platform = Platform([pygame.mouse.get_pos()[0], (50/54)*height], [(12/96)*width, (15/540)*height], (255, 0, 0), surface)
	for i in range(1, 10, 5):
		globals()['brick' + str(i)] = Brick([(7/96)*width*i, (10/54)*height], [(7/96)*width, (100/540)*height], (i*20, 200 + 55/i, i*20), surface)

	# Game Loop
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
				sys.exit()

		# Frames
		clock.tick(def_fps)
		fps = def_fps
		if 0 != clock.get_fps() < min_fps:
			fps = clock.get_fps()

		# Draw
		ball.draw(frames=fps, size=size)
		platform.draw(frames=fps, size=size)
		for i in range(1, 10, 5):
			globals()['brick' + str(i)].draw()

		pygame.display.flip()
		surface.fill((0,0,0))

		# Collision
		collision_rect(entity_group)


if __name__ == "__main__":
	main()