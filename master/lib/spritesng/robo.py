import pygame
from pygame.locals import *

import sprite
import player
from cnst import *

class Robo(sprite.Sprite3):
    def __init__(self, game, rect, name, *args):
        sprite.Sprite3.__init__(self, game, rect, 'robo-left', (0, 0, 30, 36))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.game.sprites.append(self)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.vx = 0.0
        self.vy = 0.0

        self._prev = pygame.Rect(-1, -1, 0, 0)
        self.strength = 3

        self.standing = None


    def loop(self):
        self.apply_gravity()
        self.apply_standing()

        if self.game.player.rect.centerx > self.rect.centerx:
            self.vx += 0.2
        elif self.game.player.rect.centerx < self.rect.centerx:
            self.vx -= 0.2

        if self.vx > 0.0:
            self.image = 'robo-right'
        elif s.vx < 0.0:
            self.image = 'robo-left'

        if self.get_code(sign(self.vx),0) == CODE_ROBO_TURN:
            self.vx = 0.0

        self.vx = min(4.0, self.vx)
        self.vx = max(-4.0, self.vx)

        self.rect.x += sprite.myinc(self.game.frame, self.vx)
        self.rect.y += sprite.myinc(self.game.frame, self.vy)

    def hit(self, a,b):
        player.damage(self.game, b)
