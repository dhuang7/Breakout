import pygame, math, random

entity_group = []

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, dim, color, surface):
		pygame.sprite.Sprite.__init__(self)
		self.pos = list([int(elem) for elem in pos])
		self.dim = list([int(elem) for elem in dim])
		self.color = color
		self.surface = surface
		self.still_collided = False
		self.side = False
		self.speed = [0, 0]
		self.direction = [0, 0]
		self.detected = []
		entity_group.append(self)

	def detect(self):
		pass

	def collided(self, other, side):
		pass

	def calc_speed(self):
		pass


class Circle(Entity):
	def __init__(self, pos, dim, color, surface):
		super().__init__(pos, dim, color, surface)
		self.radius = self.dim[0]
		self.speed = [50, 50]
		self.speed[1] = self.speed[1] * self.speed[0]
		self.direction = [1, 1]
		self.initial = True #fix

	def draw(self, event=None, frames=None, size=None):
		self.rect = pygame.Rect([int(elem - self.radius) for elem in self.pos], [self.radius*2]*2)
		pygame.draw.circle(self.surface, self.color, self.pos, self.radius)

		# Update
		self.pos[0] += int(self.direction[0] * (self.speed[0]/frames/54) * size[0])
		self.pos[1] += int(self.direction[1] * (self.speed[1]/self.speed[0]/frames/96) * size[1])

		# Border
		if self.pos[0] < 0 or self.pos[0] > size[0] - self.dim[0]:
			self.direction[0] *= -1
		if self.pos[1] < 0:
			self.direction[1] *= -1
		if self.pos[1] > size[1] - self.dim[1]:
			self.pos = [int(elem/2) for elem in size]

	def collided(self, other, side):
		if pygame.sprite.collide_rect(self, other) and not other.still_collided:
			if other.side:
				if self.direction[0] != other.direction[0]:
					self.direction[0] *= -1 # Bounce
			else:
				self.direction[1] *= -1 # Bounce
			self.calc_speed(other)
			other.still_collided = True
		elif not pygame.sprite.collide_rect(self, other) and other.still_collided:
			other.still_collided = False
		other.side = side


	def calc_speed(self, other):
		self.speed = [.01 + elem for elem in self.speed]
		self.speed[0] += other.direction[0] * self.direction[0] * 10
		if 0 <= int(self.speed[0]) <= 10:
			self.speed[0] = 20
			self.direction[0] = other.direction[0]
		if self.speed[0] > 50:
			self.speed[0] = 50
		elif self.speed[0] < -50:
			self.speed[0] = -50


class Box(Entity):
	def draw(self):
		self.rect = pygame.Rect(self.pos, self.dim)
		pygame.draw.rect(self.surface, self.color, self.rect)


class Platform(Box):
	def __init__(self, pos, dim, color, surface):
		super().__init__(pos, dim, color, surface)
		self.save_pos = [0, 0]

	def draw(self, event=None, frames=None, size=None):
		super().draw()

		# Update
		self.pos[0] = int(pygame.mouse.get_pos()[0])
		self.calc_velocity()

		# Border
		if self.pos[0] < 0:
			self.pos[0] = 0
		if self.pos[0] > size[0] - self.dim[0]:
			self.pos[0] = size[0] - self.dim[0]

	def calc_velocity(self):
		velocity = self.pos[0] - self.save_pos[0]
		self.speed[0] = abs(velocity)
		if velocity < 0:
			self.direction[0] = -1
		elif velocity > 0:
			self.direction[0] = 1
		else:
			self.direction[0] = 0
		self.save_pos[0] = self.pos[0]


class Brick(Box):
	def __init__(self, pos, dim, color, surface):
		super().__init__(pos, dim, color, surface)
		self.life = 1

	def collided(self, other, side):
		if pygame.sprite.collide_rect(self, other):
			if self.life == 0:
				self.pos = [elem - 10000 for elem in self.pos]
			#self.life -= 1