import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):  # inherits from Sprite class
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift  # this is to shift the world


class StaticTile(Tile):  # inherits from Tile class
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):  # inherits from StaticTile class
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load(
            './graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size  # need an offset because pygame always draws an image from the top left
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimatedTile(Tile):  # inherits from Tile class
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):  # inherits from AnimatedTile class
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset  # move the offset up so the palm trees can be on the ground
        self.rect.topleft = (x, offset_y)
