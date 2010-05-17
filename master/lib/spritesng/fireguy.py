import pygame
from pygame.locals import *

import sprite
import player
from cnst import *

import random

class Fireguy(sprite.Sprite3):
    def __init__(self, game, rect, name, *args):
        sprite.Sprite3.__init__(game, rect, 'fireguy-right-0', (0, 0, 28, 46))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.hit = hit
        self.game.sprites.append(self)

        self.moving = 0
        self.idling = random.randint(120, 240)

        self.frame = 0

        self.facing = 'right'

        self.vx = 0
        self.vy = 0

        self._prev = pygame.Rect(self.rect)
        self.strength = 3

        self.standing = None

    def loop(self):
        self.apply_gravity()
        self.apply_standing()

        if (self.moving and self.rect.x == self._prev.x
            or (sprite.get_code(self.game, self, sign(self.vx), 0)
            == CODE_FIREGUY_TURN)):
            self.vx = - self.vx

            if self.vx < 0:
                self.facing = 'left'
            else:
                self.facing = 'right'
        s._prev = pygame.Rect(s.rect)

        s.rect.x += s.vx
        s.rect.y += s.vy

        if s.idling > 0:
            if s.idling % 120 > 60:
                s.facing = 'left'
            else:
                s.facing = 'right'
            s.idling -= 1
            if s.idling == 0:
                s.moving = 90
                #if g.game.random % 2 == 0:
                if random.randint(0,1):
                    s.vx = -2
                    s.facing = 'left'
                else:
                    s.vx = 2
                    s.facing = 'right'
        elif s.moving > 0:
            s.moving -= 1
            if s.moving == 0:
                s.idling = 240
                s.vx = 0
        else:
            s.idling = 240

        s.image = 'fireguy-%s-%s' % (s.facing, (s.frame / 5) % 2)
        s.frame += 1

    def hit(g, a, b):
        player.damage(g, b)
