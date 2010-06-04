import pygame
from pygame.locals import *
from cnst import *
from decoradores import Verbose

import sprite
import capsule

class Bubble(sprite.Sprite3):
    def __init__(self, game, rect, parent, big=False):

        if game.bubble_count >= 3:
            return

        game.bubble_count += 1

        self.big = big
        self.strength = 3 if self.big else 1
        if self.big:
            sprite.Sprite3.__init__(self, game, rect, 'big-bubble',
                (0, 0, 32, 32))
        else:
            sprite.Sprite3.__init__(self, game, rect, 'bubble',
                (0, 0, 14, 14))

        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery
        self.groups.add('solid')
        self.groups.add('bubble')
        self.hit_groups.add('enemy')
        self.game.sprites.append(self)
        self.life = 30
        self.parent = parent

        self.vx = 2
        if parent.facing == 'left':
            self.vx = -2
        self.vy = 0
        self.rect.centerx += self.vx * (6 + self.rect.width / 2)
        self.rect.centery -= 4

        self.game.game.sfx['bubble'].play()

    @Verbose(VERBOSE)
    def deinit(self):
        self.game.bubble_count -= 1

    def loop(self):
        self.rect.x += self.vx * 5
        self.life -= 1
        if self.life == 0:
            self.active = False

    def hit(self, a, b):
        a.active = False

        b.strength -= a.strength
        if b.strength <= 0:
            b.active = False
            code = None
            if hasattr(b, '_code'):
                code = b._code
                delattr(b, '_code')
            Capsule.__init__(self, self.game, b.rect)
            if code != None:
                self._code = code
        else:
            self.game.game.sfx['hit'].play()
