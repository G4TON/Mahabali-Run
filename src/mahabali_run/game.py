from settings import *
from utils import *
from player import Player
from obstacle import Obstacle

import pygame as pg


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Mahabali Run')

        self.clock = pg.time.Clock()
        self.running = True

        self.all_sprites = pg.sprite.Group()
        self.player = Player((self.all_sprites,))
        self.obstacle = Obstacle((self.all_sprites,))

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pg.event.get():
                if exitPressed(event):
                    self.running = False

            self.screen.fill('white')
            self.all_sprites.draw(self.screen)

            self.all_sprites.update(dt)
            pg.display.update()
        pg.quit()
