import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, './graphics/enemy/run')
        # move the enemy to touch the ground
        # self.image.get_size() returns the x,y dimension, but [1] will only give us the y dimension
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1, 2)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    # overriding the update method from the AnimatedTile class
    def update(self, shift):
        self.rect.x += shift
        self.animate()  # comes from inherited AnimatedTile class
        self.move()
        self.reverse_image()
