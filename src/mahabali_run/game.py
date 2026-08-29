from settings import *
from utils import *

import pygame as pg


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Mahabali Run')

        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        dt = self.clock.tick() / 1000
        while self.running:
            for event in pg.event.get():
                if exitPressed(event):
                    self.running = False

            self.screen.fill('white')
            pg.display.update()
        pg.quit()
