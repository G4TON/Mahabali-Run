from settings import *
from utils import *

import pygame as pg
import random

starting_y = -TRACK_WIDTH
STARTING_POSITIONS = [(x+PADDING/2, starting_y) for x in range(0, WINDOW_WIDTH-TRACK_WIDTH, TRACK_WIDTH)]
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
        self.rect = self.image.get_frect(topleft=(PADDING/2, starting_y))
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


FOOT_POSITIONS = STARTING_POSITIONS[:-1]
class FootObstacle(Obstacle):
    def __init__(self, groups):
        super().__init__(groups)

        self.image = pg.Surface((2*TRACK_WIDTH, 2*TRACK_WIDTH))
        self.rect = self.image.get_frect(topleft = random.choice(FOOT_POSITIONS))
        self.rect.y += -starting_y + (NUMBER_OF_SPRITES - 2) * TRACK_WIDTH - PADDING/2

    def draw(self, screen):
        pg.draw.rect(screen, 'BROWN', self.rect)

    def move(self, dt):
        pass

class ObstacleCreation:
    def __init__(self, groups, delay, rate):
        self.delay = delay
        self.groups = groups
        self.rate = rate
        self.timer = Timer(delay, func=self.create, repeat=True, autostart=True)

    def create(self):
        choice = random.randint(1, 6)
        if choice > 6:
            Obstacle(self.groups)
        elif choice == 9:
            BigObstacle(self.groups)
        else:
            FootObstacle(self.groups)

    def update(self):
        self.timer.update()
