import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

class Door(sprite.Sprite3):
    def __init__(self, game, rect, name, hidden=False, *args):
        sprite.Sprite3.__init__(self, game, rect, 'door-1', (0, 0, 32, 48))
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery - (48 - 32) / 2
        self.hit = sprite_hit
        self.frame = 0
        self.open = None
        self.hit_groups.add('player')
        self.hidden = hidden
        if hidden:
            self.image = None
        self.game.sprites.insert(0, self)

    def loop(self):
        if self.hidden:
            self.image = None
            return
        if self.open > 0:
            self.image = 'door-open'
            self.open -= 1
            return
        elif (self.frame % 256) > 192:
            self.image = 'door-2'
        else:
            self.image = 'door-1'
        self.open = None
        self.frame += 1

    def sprite_hit(self, a, b):
        b.current_door = a
            
    def hit(self, pos, b):
        
        cx, cy = pos
        
        dx = 1
        while self.game.data[2][cy][cx + dx] in DOOR_CODES:
            dx += 1
        n_code = g.data[2][cy][cx + dx]
        
        if n_code == 0:
            return
        
        layer = self.game.data[2]
        
        w, h = self.game.size
        xx = cx
        yy = cy

        for y in xrange(h):
            for x in xrange(w):
                if layer[y][x] in DOOR_CODES and layer[y][x - 1] == n_code:
                    xx = x
                    yy = y
        
        #t = g.layer[yy][xx]
        self.rect = pygame.Rect(xx * TW, yy * TH, TW, TH)
        self = b
        self.rect.centerx = rect.centerx
        s.rect.bottom = rect.bottom
        if s.standing != None:
            sprite.stop_standing(g, s)
        
        sprite.init_bounds(g, s)
        sprite.init_view(g, s)
        sprite.init_codes(g, s)
        s.prev = pygame.Rect(s.rect)
        s._prev = pygame.Rect(s.rect)
        
        g.status = 'transition'
        
        g.game.sfx['door'].play()
