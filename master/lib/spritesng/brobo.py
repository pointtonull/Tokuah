import pygame
from pygame.locals import *

import sprite
import player

from cnst import *

class Brobo(sprite.Sprite3):
    def __init__(self, game, rect, name, facing, *args):
        sprite.Sprite3.__init__(self, game, rect, 'brobo-%s-0' % (facing),
            (0, 0, 60, 74))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.hit = hit
        self.game.sprites.append(self)
        self.loop = loop
        self.facing = facing

        if self.facing == 'left':
            self.vx = - 0.6
        else:
            self.vx = 0.6
        self.vy = 0

        self._prev = None
        self.strength = 6

        self.standing = None
        self.ix = 0

    def loop(self):
        self.apply_gravity()
        self.apply_standing()

        if ((self.ix != 0 and self.rect.x == self._prev.x)
            or self.get_code(sign(s.vx), 0) == CODE_BROBO_TURN):
                self.vx = - self.vx

        self._prev = pygame.Rect(self.rect)

        if self.vx > 0:
            self.facing = 'right'
        elif self.vx < 0:
            self.facing = 'left'

        self.image = 'brobo-%s-%s' % (self.facing, (self.game.frame / 10) % 2)

        self.ix = sprite.myinc(self.game.frame, self.vx)
        self.rect.x += self.ix
        self.rect.y += sprite.myinc(self.game.frame, self.vy)

    def hit(self, a, b):
        player.damage(self.game, b)
