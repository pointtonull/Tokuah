import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

class Parrot(sprite.Sprite3):
    def __init__(self, game, rect, nname, vx, *args):
        sprite.Sprite3(self, game, rect, 'parrot/left-0', (0, 16, 48, 20))
        self.game = game
        self.rect.centery = rect.centery
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.hit = hit
        game.sprites.append(self)
        self.loop = loop
        
        self.vx = vx * 2
        self.vy = 0
        
        self.facing = 'right'
        if self.vx < 0:
            self.facing = 'left'
        
        self._prev = None # pygame.Rect(s.rect)
        self.strength = 3

    def loop(self):
        
        if self._prev != None:
            if (self.rect.x == self._prev.x or sprite.get_code(self.game,
                    self, sign(self.vx), 0) == CODE_PARROT_TURN):
                self.vx = - self.vx

                if self.vx > 0:
                    self.facing = 'right'
                else:
                    self.facing = 'left'

        self._prev = pygame.Rect(self.rect)
        
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        self.image = 'parrot/%s-%d' % (self.facing, (self.game.frame /
            (FPS / 8)) % 4)
        
    def hit(self, a, b):
        player.damage(self.game, b)
