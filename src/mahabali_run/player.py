from settings import *
from utils import *

import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, sprites, timer):
        super().__init__()
        self.sprites = [sprites['balifront'], sprites['baliback'], sprites['balirunleft'], sprites['balirunright']]
        self.image = self.sprites[1]
        self.image_rect = self.image.get_frect(bottomleft=(((round(NUMBER_OF_TRACKS/2)) * TRACK_WIDTH) + PADDING/2, WINDOW_HEIGHT - 80))
        self.orig_rect = self.image_rect.copy()
        self.hitbox = self.image_rect.inflate(-self.image_rect.width/2, -self.image_rect.height/2).move(0, +25)
        self.rect = self.hitbox
        self.direction = 0
        self.timer = timer
        self.index = 0
        self.animated_sprites = self.sprites[2:]

        self.state = 0
        self.state_timer = Timer(1700, func=self.state_reset)

    def reset(self):
        self.image_rect.centerx = WINDOW_WIDTH/2
        self.image_rect.centery = self.orig_rect.centery

    def move_right(self):
        self.direction = 1

    def move_left(self):
        self.direction = -1

    def slide(self):
        self.state = -1

    def state_reset(self):
        self.state = 0

    def get_input(self):
        keys = pg.key.get_just_pressed()
        if not IS_ANDROID and not self.timer:
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.state_reset()
                self.direction = -1
            elif keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.state_reset()
                self.direction = 1
            elif keys[pg.K_s] or keys[pg.K_DOWN]:
                self.state = -1
                self.state_timer.activate()

    def move(self, dt):
        if self.timer: self.image_rect.centery += dt * TRACK_SPEED
        temp_pos = self.image_rect.copy()
        self.image_rect.centerx += self.direction * TRACK_WIDTH
        if self.image_rect.right < 0 or self.image_rect.left > WINDOW_WIDTH: self.image_rect = temp_pos
        self.hitbox.centerx = self.image_rect.centerx
        self.direction = 0


    def animate(self, dt):
        if not self.state:
            self.index += dt * 5
            if self.index >= len(self.animated_sprites): self.index = 0
            self.image = self.animated_sprites[int(self.index)]
            self.image_rect = self.image.get_frect(center=self.image_rect.center)
        elif self.state == -1:
            self.image = self.sprites[0]
            self.image_rect = self.image.get_frect(center=self.image_rect.center)
        if self.timer:
            self.image = self.sprites[1]
            self.image_rect = self.image.get_frect(center=self.image_rect.center)

    def update(self, dt):
        self.get_input()
        self.move(dt)
        self.animate(dt)
        self.state_timer.update()