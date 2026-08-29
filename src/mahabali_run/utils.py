import pygame as pg

def exitPressed(event):
    return (event.type == pg.KEYDOWN and event.key == pg.K_q) or (event.type == pg.QUIT)