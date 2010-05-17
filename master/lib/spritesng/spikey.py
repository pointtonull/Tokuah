import pygame
from pygame.locals import *

import sprite
import player

class Spikey(sprite.Sprite3):
    def init(self, game, rect, name, *args):
        sprite.Sprite3(self, game, rect, 3, (0, 0, 32, 32))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.hit_groups.add('player')
        self.hit = hit
        game.sprites.append(s)
#        self.loop = loop
        self.vx = 1
        self.vy = 1

        self._prev = pygame.Rect(self.rect)
        self.strength = 3

        self.standing = None

    def loop(self, game):
        self.apply_gravity()
        self.apply_standing()

        if self.rect.x == self._prev.x:
            self.vx = -self.vx
        self._prev = pygame.Rect(self.rect)

        self.rect.x += self.vx
        self.rect.y += self.vy

    def hit(self, game, a, b):
        self. player.damage(g, b)
