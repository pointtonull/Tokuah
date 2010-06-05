import pygame
from pygame.locals import *

from cnst import *
from decoradores import Deprecated

import sprite
import player

class Points(sprite.Sprite2):
    def __init__(self, game, rect, points):
        sprite.Sprite2.__init__(self, game, rect, 'points/%d' % points)
        self.rect.centery = rect.centery
        self.rect.centerx = rect.centerx
        self.game.sprites.append(self)
        self.points = points
        self.frame = 0

    def loop(self):
        self.frame += 1
        if self.frame == FPS:
            self.active = False
