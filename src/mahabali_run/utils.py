import pygame as pg


def exitPressed(event):
    return (event.type == pg.KEYDOWN and event.key == pg.K_q) or (event.type == pg.QUIT)


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