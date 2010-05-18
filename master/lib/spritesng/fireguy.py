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

        self._prev = pygame.Rect(s.rect)

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.idling > 0:
            if self.idling % 120 > 60:
                self.facing = 'left'
            else:
                self.facing = 'right'
            self.idling -= 1

            if self.idling == 0:
                self.moving = 90

                if random.randint(0, 1):
                    self.vx = -2
                    self.facing = 'left'
                else:
                    self.vx = 2
                    self.facing = 'right'

        elif self.moving > 0:
            self.moving -= 1
            if self.moving == 0:
                self.idling = 240
                self.vx = 0

        else:
            self.idling = 240

        self.image = 'fireguy-%s-%s' % (self.facing, (self.frame / 5) % 2)
        self.frame += 1

    def hit(self, a, b):
        player.damage(self.game, b)
