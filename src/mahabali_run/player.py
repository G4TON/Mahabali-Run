from settings import *
from utils import *

import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((80, 80))
        self.rect = self.image.get_frect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 16))
        self.direction = 0

        self.image.fill('black')

    def get_input(self):
        keys = pg.key.get_just_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.direction = -1
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.direction = 1

    def move(self):
        self.rect.centerx += self.direction * TRACK_WIDTH

    def update(self):
        self.get_input()
        self.move()