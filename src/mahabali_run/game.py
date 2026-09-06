from utils import *
from player import Player
from obstacle import BigObstacle, ObstacleCreation, FootObstacle, Obstacle
from settings import *

import pygame as pg


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()

        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.game_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption('Mahabali Run')

        self.clock = pg.time.Clock()
        self.running = True
        self.sprites = load_svgs(asset_path('graphics'))
        self.sounds = load_sounds(asset_path('sounds'))

        pg.display.set_icon(self.sprites['icon'])

        self.obstacle_sprites = pg.sprite.Group()
        self.creator = ObstacleCreation(self.obstacle_sprites, self.sprites, self.sounds)

        self.gameover = True
        self.playbutton = Button(self.sprites['button'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.start_run)
        self.score = Text('0', 'gold', pg.Font(None, 100), (WINDOW_WIDTH / 2, 100))
        self.gameovertimer = Timer(1000, func=self.homescreen)
        self.player = Player(self.sprites, self.gameovertimer)

        self.sounds['bgm'].play(-1)
        self.sounds['bgm'].set_volume(0.5)

    def start_run(self):
        TRACK_SPEED = TRACK_WIDTH * 1.5
        self.sounds['gamestart'].play()
        self.player.reset()
        self.obstacle_sprites.empty()
        self.creator.timer.activate()
        self.creator.bosstimer.activate()
        self.creator.timer.duration = self.creator.delay
        self.gameovertimer.deactivate()
        self.SCORE = 0
        self.gameover = False

    def homescreen(self):
        self.gameover = True

    def collision(self):
        collided = pg.sprite.spritecollide(self.player, self.obstacle_sprites, False)
        if collided:
            sprite = collided[-1]
            if isinstance(sprite, BigObstacle):
                if self.player.rect.centerx == WINDOW_WIDTH / 2 and self.player.state == -1:
                    return
                elif sprite.rect_left.colliderect(self.player.rect) or sprite.rect_right.colliderect(self.player.rect):
                    self.sounds['gameover'].play()
                    self.sounds['gameover'].set_volume(0.5)
                    self.gameovertimer.activate()
                else:
                    self.sounds['gameover'].play()
                    self.sounds['gameover'].set_volume(0.5)
                    self.gameovertimer.activate()
            else:
                self.sounds['gameover'].play()
                self.sounds['gameover'].set_volume(0.5)
                self.gameovertimer.activate()

        bosscollided = self.creator.boss.rect.colliderect(self.player.rect) and not self.creator.boss.growing
        if bosscollided and not self.gameovertimer:
            self.sounds['gameover'].play()
            self.sounds['gameover'].set_volume(0.5)
            self.gameovertimer.activate()

    def run(self):
        self.SCORE = 0
        touch_start = None
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pg.event.get():

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False

                if self.gameover:
                    if event.type in (pg.FINGERDOWN, pg.MOUSEBUTTONDOWN):
                        self.start_run()

                elif event.type == pg.FINGERDOWN:
                    touch_start = pg.Vector2(event.x, event.y)

                elif event.type == pg.FINGERUP and touch_start is not None:
                    touch_end = pg.Vector2(event.x, event.y)
                    swipe = touch_end - touch_start
                    if abs(swipe.x) > abs(swipe.y):
                        if abs(swipe.x) > 0.1:
                            if swipe.x > 0:
                                self.player.move_right()
                            else:
                                self.player.move_left()
                    else:
                        if abs(swipe.y) > 0.1:
                            if swipe.y > 0:
                                self.player.slide()  # swipe down

                    touch_start = None

            self.game_surface.fill('#C2B280')
            if not self.gameover:
                for sprite in self.obstacle_sprites:
                    if isinstance(sprite, Obstacle) and not isinstance(sprite, BigObstacle):
                        self.game_surface.blit(sprite.image, sprite.image_rect)
                if self.player.state == -1: self.game_surface.blit(self.player.image, self.player.image_rect)
                for sprite in self.obstacle_sprites:
                    if isinstance(sprite, BigObstacle):
                        sprite.draw(self.game_surface)
                    elif isinstance(sprite, Obstacle):
                        continue
                    else:
                        self.game_surface.blit(sprite.image, sprite.image_rect)
                if self.player.state != -1: self.game_surface.blit(self.player.image, self.player.image_rect)
                if not self.creator.bosstimer: self.creator.boss.draw(self.game_surface)

                self.creator.update(dt)
                self.obstacle_sprites.update(dt)
                self.player.update(dt)
                self.SCORE += dt * 2
                self.score.update(f'{int(self.SCORE)}')
                self.collision()
                self.gameovertimer.update()
            else:
                self.playbutton.update()
                self.game_surface.blit(self.playbutton.image, self.playbutton.rect)
                self.game_surface.blit(self.player.sprites[1], self.player.image_rect)
            self.game_surface.blit(self.score.text, self.score.rect)
            # scaled = pg.transform.scale(self.game_surface, self.screen.get_size())
            # self.screen.blit(scaled, (0, 0))
            pg.display.update()
        pg.quit()
