import pygame
from pygame.locals import *

import sprite
import capsule

class Bubble(sprite.Sprite3):
    def __init__(self, game, rect, p, big=False):
        if not hasattr(game, 'bubble_count'):
            game.bubble_count = 0

        if game.bubble_count >= 3:
            return None

        game.bubble_count += 1
        #print 'new bubble', g.bubble_count
        if big:
            sprite.Sprite3.__init__(self, game, rect, 'big-bubble',
                (0, 0, 32, 32))
        else:
            sprite.Sprite3.__init__(self, game, rect, 'bubble',
                (0, 0, 14, 14))
        self.big = big
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery
        self.groups.add('solid')
        self.groups.add('bubble')
        self.hit_groups.add('enemy')
        self.game.sprites.append(self)
        self.life = 30
        self.strength = 1
        if big:
            s.strength = 3

        self.vx = 2
        if p.facing == 'left':
            self.vx = -2
        self.vy = 0
        self.rect.centerx += self.vx * (6 + self.rect.width / 2)
        self.rect.centery -= 4

        self.game.game.sfx['bubble'].play()

    def deinit(self):
        #print "bubble deinit"
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
