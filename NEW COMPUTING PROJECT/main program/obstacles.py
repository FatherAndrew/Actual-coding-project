import pygame as pg

from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # init sprite
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # draw wall
        self.image = pg.Surface((32, 32))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        # set position
        self.x = x
        self.y = y
        self.rect.x = x*32
        self.rect.y = y*32

    def update(self):
        pass