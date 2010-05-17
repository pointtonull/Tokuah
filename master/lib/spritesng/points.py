import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

class Points(sprite.Sprite2):
    def __init__(self, game, rect, v):
        sprite.Sprite2.__init__(game, rect, 'points/%d' % v) #3
        self.rect.centery = r.centery
        self.rect.centerx = r.centerx
        self.sprites.append(self)

        self.frame = 0

    def loop(self):
        self.frame += 1
        if self.frame == FPS:
            self.active = False
