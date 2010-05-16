import pygame
from pygame.locals import *

from cnst import *

import sprite

class Platform(sprite.Sprite3):
    def init(self, game, rect, name, vx, vy):

        x = rect.centerx / TW
        y = rect.centery / TH
        code = game.data[2][y][x]
        min_x = x
        max_x = x

        for dx in xrange(1, 4):
            if g.data[2][y][x + dx] != code:
                break
            max_x = x + dx

        for dx in xrange(-1, -4, -1):
            if g.data[2][y][x + dx] != code:
                break
            min_x = x + dx

        iy = y
        for ix in xrange(min_x, max_x + 1):
            if (ix, iy) in g.codes:
                return

        w = (max_x - min_x + 1) * TW
        h = TH
        r = pygame.Rect(min_x * TW, iy * TH, w, h)

        sprite.Sprite3(self, game, rect, 'platform/%d' % (max_x - min_x + 1),
            (0, 0, w, h))
        self.groups.add('solid')
        self.hit_groups.add('player')
        self.hit = hit
        game.sprites.append(self)
        self.loop = loop

        self.vx = vx * 2
        self.vy = vy * 2

        self._prev = None
        self.carrying = []


    def loop(self, game):
        #check if we hit a wall...
        if s._prev != None:
            if (self.rect.x == self._prev.x or sprite.get_code(game, 
                    self, sign(self.vx), 0) == CODE_PLATFORM_TURN):
                self.vx = - self.vx
            if (self.rect.y == self._prev.y or sprite.get_code(game,
                    self, 0, sign(self.vy)) == CODE_PLATFORM_TURN):
                self.vy = - self.vy

        self._prev = pygame.Rect(self.rect)

        self.rect.x += self.vx
        self.rect.y += self.vy

        for b in self.carrying:
            b.rect.x += self.vx
            b.rect.y += self.vy


    def hit(self, game, a, b):
        if not hasattr(b, 'standing'):
            return

        rect = a.rect
        aprev = a.prev
        cur = b.rect
        prev = b.prev

        if prev.bottom <= aprev.top and cur.bottom > rect.top:
            cur.bottom = rect.top
            b.standing = a

            if b not in a.carrying:
                a.carrying.append(b)
