from settings import *
from utils import *

import pygame as pg


class Obstacle(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pg.Surface((128, 128))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2, 100))

        self.delay = 3000
        self.timer = Timer(self.delay)

    def move(self, dt):
        self.rect.centery += dt * TRACK_SPEED

    def update(self, dt):
        self.move(dt)
