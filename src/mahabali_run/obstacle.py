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

        self.index = 0
        self.sprites = []

    def move(self, dt):
        self.rect.centery += dt * TRACK_SPEED
        if self.rect.top > WINDOW_HEIGHT: del self

    def update(self, dt):
        self.move(dt)
        self.animate(dt)

    def animate(self, dt):
        pass


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


class FootObstacle(Obstacle):
    def __init__(self):
        super().__init__([])

        self.image = pg.Surface((2*TRACK_WIDTH-2*PADDING, 2*TRACK_WIDTH))
        self.original = self.image.copy()
        self.rect = self.image.get_frect(topleft = random.choice(STARTING_POSITIONS))
        self.rect.y += -starting_y + (NUMBER_OF_SPRITES - 2) * TRACK_WIDTH - PADDING/2
        if self.rect.right >= WINDOW_WIDTH:
            self.rect.right -= PADDING/2
        else:
            self.rect.left += PADDING/2

        self.shadow = self.rect.copy().inflate(-self.rect.width, -self.rect.height)
        self.growing = True
        self.passed = False
        self.rate = 175

    def draw(self, screen):
        pg.draw.rect(screen, 'GOLD', self.shadow)
        if not self.growing: pg.draw.rect(screen, 'BROWN', self.rect)

    def move(self, dt):
        if not self.growing:
            self.rect.y += dt * TRACK_SPEED
            if self.rect.top >= WINDOW_HEIGHT: self.passed = True

    def animate(self, dt):
        self.shadow.inflate_ip(dt * self.rate, dt * self.rate)
        if self.shadow.width >= self.rect.width:
            self.shadow.size = self.rect.size
            self.growing = False
        self.shadow.center = self.rect.center

class ObstacleCreation:
    def __init__(self, groups, rate):
        self.groups = groups
        self.rate = rate
        self.delay = 3000
        self.bosstimer = Timer(30000, autostart=True)
        self.timer = Timer(self.delay, func=self.create, repeat=True, autostart=True)
        self.boss = FootObstacle()
        self.dt = 0
        self.createdtimes = 0
        self.bossdelays = Timer(2000)
        self.bossdelay_activated = False

    def create(self):
        choice = random.randint(1, 6)
        if self.bosstimer:
            if choice < 5:
                Obstacle(self.groups)
            else:
                BigObstacle(self.groups)

    def bosscreate(self):
        self.boss.update(self.dt)
        if self.boss.passed:
            if not self.bossdelay_activated and not self.createdtimes:
                self.bossdelay_activated = True
                self.bossdelays.activate()
            elif not self.bossdelays:
                del self.boss
                self.boss = FootObstacle()
                if self.createdtimes >= 1:
                    self.bosstimer.activate()
                    self.createdtimes = 0
                    self.bossdelay_activated = False
                else: self.createdtimes += 1

    def update(self, dt):
        self.dt = dt
        self.bosstimer.update()
        self.bossdelays.update()
        self.timer.update()
        if not self.bosstimer:
            self.bosscreate()
