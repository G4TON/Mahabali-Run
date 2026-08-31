from settings import *
from utils import *

import pygame as pg
import random


STARTING_POSITIONS = [(x+PADDING/2, -TRACK_WIDTH * 3) for x in range(0, WINDOW_WIDTH-TRACK_WIDTH, TRACK_WIDTH)]
class Obstacle(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pg.Surface((SPRITE_SIZE * SPRITE_SCALING, SPRITE_SIZE * SPRITE_SCALING))
        self.rect = self.image.get_frect(topleft=random.choice(STARTING_POSITIONS))

    def move(self, dt):
        self.rect.centery += dt * TRACK_SPEED
        if self.rect.top > WINDOW_HEIGHT: del self

    def update(self, dt):
        self.move(dt)


class BigObstacle(Obstacle):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pg.Surface((SPRITE_SIZE * SPRITE_SCALING * NUMBER_OF_TRACKS + (NUMBER_OF_TRACKS - 1) * PADDING,
                                 SPRITE_SIZE * SPRITE_SCALING))
        self.rect = self.image.get_frect(topleft=(PADDING/2, -TRACK_WIDTH * 3))
        self.rect_left = pg.FRect(self.rect.topleft, (SPRITE_SIZE * SPRITE_SCALING, SPRITE_SIZE * SPRITE_SCALING))
        self.rect_right = pg.FRect(self.rect.move(-(SPRITE_SIZE * SPRITE_SCALING), 0).topright,
                                   (SPRITE_SIZE * SPRITE_SCALING, SPRITE_SIZE * SPRITE_SCALING))

    def draw(self, screen):
        pg.draw.rect(screen, 'cyan', self.rect.inflate(0, -100))
        pg.draw.rect(screen, 'red', self.rect_left, 5)
        pg.draw.rect(screen, 'blue', self.rect_right, 5)

    def move(self, dt):
        self.rect.centery += dt * TRACK_SPEED
        self.rect_left.y = self.rect_right.y = self.rect.y
        if self.rect.top > WINDOW_HEIGHT: del self

    def interaction(self):
        pass


obstacles = [Obstacle, BigObstacle]
class ObstacleCreation:
    def __init__(self, groups, delay, rate):
        self.delay = delay
        self.groups = groups
        self.rate = rate
        self.timer = Timer(delay, func=self.create, repeat=True, autostart=True)

    def create(self):
        obstacle = random.choice(obstacles)
        obstacle(self.groups)

    def update(self):
        self.timer.update()
