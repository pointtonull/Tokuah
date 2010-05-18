import pygame
from pygame.locals import *
import sprite

class Capsule(sprite.Sprite3):
    def __init__(self, game, rect):
        sprite.Sprite3.__init__(self, game, rect, 'captured-generic',
            (0, 0, 32, 32))

        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery
        self.hit_groups.add('player')
        self.groups.add('capsule')
        self.game.sprites.append(self)

        self.life = 300

        self.vx = (self.game.game.random % 10) / 5.0 - 0.5
        self.vy = - 1.0
        self.x = float(self.rect.x)

        self.carrying = []
        self.prev = pygame.Rect(self.rect)

        self.game.game.sfx['capsule'].play()

    def loop(self):
        self.vx += (self.game.game.random % 100) / 1000.0 - 0.05
        self.vx = max(-0.25, min(0.25, self.vx))
        self.x += self.vx

        dx = int(self.x - self.rect.x)

        dy = sprite.myinc(self.game.frame, self.vy)

        self.rect.x += dx
        self.rect.y += dy

        if self.life == 0:
            self.die()
        self.life -= 1

        for b in self.carrying:
            b.rect.x += dx
            b.rect.y += dy


    def die(self):
        self.game.game.sfx['pop'].play()
        self.active = False

        for b in self.carrying:
            self.stop_standing()


    def hit(self, a, b):

#        if not hasattr(b, 'standing'):
#            return

        rect = a.rect
        aprev = a.prev
        cur = b.rect
        prev = b.prev

        if prev.bottom <= aprev.top and cur.bottom > rect.top:
            cur.bottom = rect.top
            b.standing = a
            if b not in a.carrying:
                a.carrying.append(b)
