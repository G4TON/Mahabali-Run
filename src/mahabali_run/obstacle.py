from utils import *
from settings import *

import pygame as pg
import random

starting_y = -TRACK_WIDTH
STARTING_POSITIONS = [(x+PADDING/2, starting_y) for x in range(0, WINDOW_WIDTH-TRACK_WIDTH, TRACK_WIDTH)]
COCONUT_SPRITES = []
class Obstacle(pg.sprite.Sprite):
    def __init__(self, groups, sprites):
        super().__init__(groups)

        self.sprite = random.choice([sprites['coconut'], sprites['puddle'], sprites['rock']])
        self.image = self.sprite
        self.image_rect = self.image.get_frect(topleft=random.choice(STARTING_POSITIONS))
        self.hitbox = self.image_rect.copy()
        self.rect = self.hitbox
        self.index = 0

        global SPRITES
        self.sprites = []
        if self.sprite == sprites['coconut']:
            if not COCONUT_SPRITES:
                for i in range(20, 360, 20):
                    rotated = pg.transform.rotate(self.sprite, i)
                    COCONUT_SPRITES.append(rotated)
            self.sprites = COCONUT_SPRITES


    def move(self, dt):
        self.image_rect.centery += dt * TRACK_SPEED
        self.hitbox.center = self.image_rect.center
        if self.image_rect.top > WINDOW_HEIGHT: self.kill()

    def update(self, dt):
        self.move(dt)
        self.animate(dt)

    def animate(self, dt):
        if not self.sprites: return
        self.index += dt * 10
        if self.index >= len(self.sprites): self.index = 0
        self.image = self.sprites[int(self.index)]
        self.image_rect = self.image.get_frect(center = self.image_rect.center)


class BigObstacle(Obstacle):
    def __init__(self, groups, sprites):
        super().__init__(groups, sprites)
        self.sprites = [sprites['womantug'], sprites['rope'], sprites['mantug']]
        self.sprites[1] = pg.transform.scale_by(self.sprites[1], 0.35)

        self.image = pg.Surface((SPRITE_SIZE * SPRITE_SCALING * NUMBER_OF_TRACKS + (NUMBER_OF_TRACKS - 1) * PADDING,
                                 SPRITE_SIZE * SPRITE_SCALING))
        self.rect = self.image.get_frect(topleft=(PADDING/2, starting_y))
        self.rect_left = pg.FRect(self.rect.topleft, (SPRITE_SIZE * SPRITE_SCALING, SPRITE_SIZE * SPRITE_SCALING))
        self.rect_right = pg.FRect(self.rect.move(-(SPRITE_SIZE * SPRITE_SCALING), 0).topright,
                                   (SPRITE_SIZE * SPRITE_SCALING, SPRITE_SIZE * SPRITE_SCALING))
        self.image = self.sprites[1]
        self.rect = self.image.get_frect(topleft=self.rect_left.topright+pg.Vector2(-100, 37))


    def draw(self, screen):
        screen.blits(((self.image, self.rect_left.topright+pg.Vector2(-100, 37)),
                      (self.sprites[0], self.rect_left),
                      (self.sprites[2], self.rect_right)))

    def move(self, dt):
        self.rect.centery += dt * TRACK_SPEED
        self.rect_left.y = self.rect_right.y = self.rect.y
        if self.rect.top > WINDOW_HEIGHT: self.kill()

    def animate(self, dt):
        pass

    def interaction(self):
        pass


class FootObstacle(Obstacle):
    def __init__(self,sprites, sounds):
        super().__init__(([],), sprites)
        self.sounds = sounds
        self.sprites = [sprites['shadow'], sprites['feetleft'], sprites['feetright']]
        self.image = pg.Surface((2*TRACK_WIDTH-2*PADDING, 2*TRACK_WIDTH))
        self.rect = self.image.get_frect(topleft = random.choice(STARTING_POSITIONS))
        if self.rect.centerx < WINDOW_WIDTH/2: self.image = self.sprites[1]
        else: self.image = self.sprites[2]
        self.rect.y += -starting_y + (NUMBER_OF_SPRITES - 2) * TRACK_WIDTH - PADDING/2
        if self.rect.right >= WINDOW_WIDTH:
            self.rect.right -= PADDING/2
        else:
            self.rect.left += PADDING/2


        self.shadow = self.rect.copy().inflate(-self.rect.width, -self.rect.height)
        self.shadowsprite = self.sprites[0]
        self.growing = True
        self.passed = False
        self.soundplayed = False
        self.rate = 175

    def draw(self, screen):
        screen.blit(self.shadowsprite, self.shadow)
        if not self.growing: screen.blit(self.image, self.rect)

    def move(self, dt):
        if not self.growing:
            if not self.soundplayed:
                self.sounds['stomp'].play()
                self.sounds['stomp'].set_volume(0.7)
                self.soundplayed = True
            self.rect.y += dt * TRACK_SPEED
            if self.rect.top >= WINDOW_HEIGHT:
                self.passed = True
                del self


    def animate(self, dt):
        self.shadow.inflate_ip(dt * self.rate, dt * self.rate)
        self.shadowsprite = pg.transform.scale(self.sprites[0], self.shadow.size)
        if self.shadow.width >= self.rect.width:
            self.shadow.size = self.rect.size
            self.growing = False
        self.shadow.center = self.rect.center


class ObstacleCreation:
    def __init__(self, groups, sprites, sounds):
        self.groups = groups
        self.delay = 3000
        self.bosstimer = Timer(25000, autostart=True)
        self.timer = Timer(self.delay, func=self.create, repeat=True)
        self.sprites = sprites
        self.sounds = sounds
        self.boss = FootObstacle(sprites, self.sounds)
        self.dt = 0
        self.createdtimes = 0
        self.bossdelays = Timer(1500)
        self.bossdelay_activated = False

    def create(self):
        choice = random.randint(1, 6)
        self.timer.duration *= 99/100
        global TRACK_SPEED
        TRACK_SPEED += TRACK_SPEED * 0.01
        if self.bosstimer:
            if choice < 5:
                Obstacle(self.groups, self.sprites)
            else:
                BigObstacle(self.groups, self.sprites)

    def bosscreate(self):
        self.boss.update(self.dt)
        if self.boss.passed:
            if not self.bossdelay_activated and not self.createdtimes:
                self.bossdelay_activated = True
                self.bossdelays.activate()
            elif not self.bossdelays:
                del self.boss
                self.boss = FootObstacle(self.sprites, self.sounds)
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
