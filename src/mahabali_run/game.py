from settings import *
from utils import *
from player import Player
from obstacle import BigObstacle, ObstacleCreation, FootObstacle

import pygame as pg


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Mahabali Run')

        self.clock = pg.time.Clock()
        self.running = True

        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.creator = ObstacleCreation(self.all_sprites, 0, 9)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pg.event.get():
                if exitPressed(event):
                    self.running = False

            self.screen.fill('white')
            for sprite in self.all_sprites:
                if isinstance(sprite, BigObstacle) or isinstance(sprite, FootObstacle): sprite.draw(self.screen)
                else: self.screen.blit(sprite.image, sprite.rect)
            self.screen.blit(self.player.image, self.player.rect)

            self.creator.update()
            self.all_sprites.update(dt)
            self.player.update(dt)
            pg.display.update()
        pg.quit()
