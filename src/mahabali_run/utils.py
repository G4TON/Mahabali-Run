import pygame as pg
from pathlib import Path
from settings import *
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

BASE_DIR = get_base_dir()

def asset_path(*parts):
    return BASE_DIR.joinpath(*parts)


def load_svgs(directory):
    sprites = {}

    for file in Path(directory).iterdir():
        if file.suffix.lower() in {".svg", ".png"}:
            image = pg.image.load(file).convert_alpha()
            if file.stem == 'balifront': image = pg.transform.flip(image, False, True)
            sprites[file.stem] = pg.transform.scale_by(image, SPRITE_SCALING)

    return sprites


def load_sounds(directory):
    sounds = {}

    for file in Path(directory).glob("*.mp3"):
        sounds[file.stem] = pg.mixer.Sound(str(file))

    return sounds


def exitPressed(event):
    return (event.type == pg.KEYDOWN and event.key == pg.K_q) or (event.type == pg.QUIT)


'''
Timer class was copied from YouTuber ClearCode's YT tutorial on PyGame
Credits to ClearCode, check out his YouTube channel.
'''
class Timer:
    """Class for handling timed events"""
    def __init__(self, duration, func=None, autostart=False, repeat=False):
        # base setup
        self.active = False
        self.duration = duration
        self.start_time = 0
        self.func = func
        self.repeat = repeat
        if autostart: self.activate()

    def __bool__(self):
        """Boolean representation of Timer for use in conditional statements"""
        return self.active

    def activate(self):
        """Activates the timer"""
        self.active = True
        self.start_time = pg.time.get_ticks()

    def deactivate(self):
        """Deactivates the timer"""
        self.active = False
        self.start_time = 0
        if self.repeat: self.activate()

    def update(self):
        """Updates timer state"""
        if pg.time.get_ticks() - self.start_time >= self.duration:
            if self.func and self.start_time: self.func()   # only calls function if timer has been started
            self.deactivate()


class Button:
    def __init__(self, image, pos, func):
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.func = func

    def update(self):
        mousepos = pg.mouse.get_pos()

        if pg.mouse.get_just_pressed()[0] and self.rect.collidepoint(mousepos):
            self.func()


class Text:
    def __init__(self, message, color, font, pos):
        self.font = font
        self.text = self.font.render(message, True, color)
        self.color = color
        self.rect = self.text.get_frect(center=pos)
        self.pos = pos

    def update(self, message):
        self.text = self.font.render(message, True, self.color)
        self.rect.center = self.pos
