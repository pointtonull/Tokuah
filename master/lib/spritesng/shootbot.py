import pygame
from pygame.locals import *

import sprite
import player
from laser import Laser

from cnst import *

class Shootbot(sprite.Sprite3):
    def __init__(self, game, rect, name, facing='left', *args):
        sprite.Sprite3.__init__(self, game, rect, 'shootbot-%s-0' % (facing),
            (0, 0, 18, 24))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.game.sprites.append(self)
        self.facing = facing

        self.shoot = 120
        self.shooting = 0

        if self.facing == 'left':
            self.vx = -1.0
        else:
            self.vx = 1.0
        self.vy = 0

        self._prev = pygame.Rect(-1, -1, 0, 0)
        self.strength = 3

        self.standing = None

    def loop(self):
        self.apply_gravity()
        self.apply_standing()

        self._prev = pygame.Rect(self.rect)

        if self.game.player.rect.centerx > self.rect.centerx:
            self.vx += 0.02
        elif self.game.player.rect.centerx < self.rect.centerx:
            self.vx -= 0.02

        if self.vx > 0.0:
            self.facing = 'right'
        elif self.vx < 0.0:
            self.facing = 'left'
        self.image = 'shootbot-%s-%s' % (self.facing,
            (self.game.frame / 10) % 4)

        if self.get_code(sign(self.vx), 0) == CODE_SHOOTBOT_TURN:
            self.vx = 0.0

        self.vx = min(1.0, self.vx)
        self.vx = max(-1.0, self.vx)

        if self.shoot == 0:
            shot = Laser(self.game, self.rect, self)
            self.shoot = 120
            self.shooting = 10

        if self.shooting > 0:
            self.image = 'shootbot-%s-shoot' % (self.facing)
            self.shooting -= 1

        self.shoot -= 1

        self.rect.x += sprite.myinc(self.game.frame, self.vx)
        self.rect.y += sprite.myinc(self.game.frame, self.vy)

    def hit(self, a, b):
        player.damage(self.game, b)
