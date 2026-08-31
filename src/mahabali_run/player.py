from settings import *
from utils import *

import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pg.Surface((SPRITE_SIZE * SPRITE_SCALING, SPRITE_SIZE * SPRITE_SCALING))
        self.rect = self.image.get_frect(bottomleft=(((round(NUMBER_OF_TRACKS/2)) * TRACK_WIDTH) + PADDING/2, WINDOW_HEIGHT - 80))
        self.direction = 0

        self.image.fill('black')

    def get_input(self):
        keys = pg.key.get_just_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.direction = -1
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.direction = 1

    def move(self, dt):
        temp_pos = self.rect.copy()
        self.rect.centerx += self.direction * TRACK_WIDTH
        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH: self.rect = temp_pos
        self.direction = 0


    def update(self, dt):
        self.get_input()
        self.move(dt)