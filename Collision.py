import pygame
from Entity import Circle


def detection(entity, other):
	if isinstance(entity, Circle):
		adjust = entity.radius
	else:
		adjust = 0
	if entity.pos[0] + entity.dim[0] < other.pos[0] - entity.speed[0]/2 or entity.pos[0] > other.pos[0] + other.dim[0]:
		if entity.pos[0] + entity.dim[0] > other.pos[0] - entity.speed[0] or entity.pos[0] < other.pos[0] + other.dim[0] + entity.speed[0]:
			if other.pos[1] - other.dim[1]/2 < entity.pos[1] + entity.dim[1] + adjust and entity.pos[1] < other.pos[1] + other.dim[1] + other.dim[1]/2:
				return True
	return False

def collision_rect(rect_entities):
	for entity in rect_entities:
		for other in rect_entities[rect_entities.index(entity) + 1:]:
			detected = detection(entity, other)
			entity.collided(other, detected)
			other.collided(entity, detected)