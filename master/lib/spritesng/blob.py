import pygame
from pygame.locals import *

import sprite
import player

from cnst import *

class Blob(sprite.Sprite3):
    def __init__(self, game, rect, name, *args):
        sprite.Sprite3(game, rect, 'blob', (0, 0, 30, 30))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.hit = hit
        self.game.sprites.append(self)

        self.vx = 0
        self.vy = 0

        self.next_jump = 0

        self._prev = pygame.Rect(self.rect)
        self.strength = 3

        self.standing = None

    def loop(self):
        self.apply_gravity()
        self.apply_standing()

        if self.next_jump == 0 and self.standing:
            self.vy = - 12.0
            self.next_jump = FPS * 2
            self.stop_standing()

        if self.next_jump > 0:
            self.next_jump -= 1

        self._prev = pygame.Rect(self.rect)

        self.rect.y += sprite.myinc(self.game.frame, self.vy)

    def hit(self, a, b):
        player.damage(self.game, b)
