import pygame
from pygame.locals import *

import player
import sprite

class Laser(sprite.Sprite3):
    def __init__(self, game, rect, parent):
        sprite.Sprite3.__init__(game, rect, 'laser', (0, 0, 4, 2))

        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery

        self.groups.add('solid')
        self.groups.add('laser')
        self.hit_groups.add('player')

        self.game.sprites.append(self)
        self.life = 90
        self.strength = 1
        
        self.vx = 1

        if parent.facing == 'left':
            self.vx = -1

        self.vy = 0
        self.rect.centerx += self.vx * (6 + self.rect.width / 2)
        self.rect.centery -= 2
        
    def loop(self):
        self.rect.x += self.vx * 2
        self.life -= 1
        if self.life == 0:
            self.active = False

    def hit(self, a, b): 
        player.damage(self.game, b)
