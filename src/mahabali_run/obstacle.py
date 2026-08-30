from settings import *
from utils import *

import pygame as pg
import random


head = None
STARTING_POSITIONS = [(x+PADDING/2, -TRACK_WIDTH) for x in range(0, WINDOW_WIDTH-TRACK_WIDTH, TRACK_WIDTH)]
class Obstacle(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pg.Surface((128, 128))
        self.rect = self.image.get_frect(topleft=random.choice(STARTING_POSITIONS))

        self.delay = 2500
        self.timer = Timer(self.delay, autostart=True)

    def move(self, dt):
        self.rect.centery += dt * TRACK_SPEED
        if self.rect.top > WINDOW_HEIGHT: self.kill()

    def update(self, dt):
        self.move(dt)
        self.timer.update()

    @staticmethod
    def spawn(group):
        global head
        if not head: head = Obstacle(group)
        if not head.timer: head = Obstacle(group)


class Collectible(Obstacle):
    def __init__(self, groups):
        super().__init__(groups)

    def interaction(self):
        pass

